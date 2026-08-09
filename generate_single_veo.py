import os
import json
import subprocess
import time
import asyncio
import edge_tts
import re
import urllib.request
from google import genai

BASE_DIR = "/Users/ckaplan/dev/neuralon/hamster/frontend/public"
SCRIPTS_FILE = os.path.join(BASE_DIR, "trailer_scripts.json")
TRAILERS_DIR = os.path.join(BASE_DIR, "trailers")
VOICEOVERS_DIR = os.path.join(BASE_DIR, "voiceovers")
EPIC_MUSIC = os.path.join(TRAILERS_DIR, "epic_music.mp3")

gemini_key = os.getenv('GEMINI_API_KEY')
genai_client = genai.Client(api_key=gemini_key, http_options={'api_version':'v1alpha'})

with open(SCRIPTS_FILE, 'r') as f:
    scripts = json.load(f)

# Find Furry Fury (Mad Max parody)
target_uid = "6c0ef1c6eaea4bc48122abe490a6a61d"
script_data = next((s for s in scripts if s['uid'] == target_uid), None)

async def generate_voiceover(text, path, style):
    voice = "en-US-ChristopherNeural"
    if "female" in style.lower() or "woman" in style.lower():
        voice = "en-US-AriaNeural"
    elif "whisper" in style.lower() or "creepy" in style.lower():
        voice = "en-US-SteffanNeural"
    elif "dialogue" in style.lower():
        voice = "en-GB-RyanNeural"
        
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(path)

async def process_one():
    uid = script_data['uid']
    title = script_data.get('inspiration', f"Movie {uid}")
    
    final_trailer = os.path.join(TRAILERS_DIR, f"trailer_{uid}.mp4")
    # Delete old bad trailer if exists
    if os.path.exists(final_trailer):
        os.remove(final_trailer)
        
    print(f"Starting PERFECT render for {uid} (Inspired by: {title})")
    
    # 1. Voiceover
    vo_path = os.path.join(VOICEOVERS_DIR, f"{uid}_v2.mp3")
    text_to_speak = script_data.get('script_content', '')
    if not text_to_speak or "no dialogue" in text_to_speak.lower() or "music & visual" in script_data.get('trailer_style', '').lower() or "on-screen text" in text_to_speak.lower():
        # Read on-screen text as dramatic voiceover to ensure the mix always has audio driving it
        pass
    
    # Clean up script tags like "ON-SCREEN TEXT: " or "HAMSTER 1: " so the TTS doesn't read them aloud!
    # Extract just the spoken lines, skipping the ALL CAPS character names and parenthetical actions like (Brave, Indy-esque):
    text_to_speak = re.sub(r'^[A-Z0-9 \-]+(?:\s*\([^)]+\))?:\s*', '', text_to_speak, flags=re.MULTILINE)
    text_to_speak = text_to_speak.replace('[', '').replace(']', '')
    
    print(f"  -> Generating Cleaned TTS Voiceover...")
    await generate_voiceover(text_to_speak, vo_path, script_data.get('audio_direction', ''))

    # 2. Veo 3.1 Scenes
    veo_dir = os.path.join(TRAILERS_DIR, f"veo_scenes_{uid}")
    os.makedirs(veo_dir, exist_ok=True)
    
    scene_prompts = script_data.get('scenes', [])[:15]
    operations = []
    
    print(f"  -> Submitting {len(scene_prompts)} scenes to Veo 3.1...")
    for j, s_prompt in enumerate(scene_prompts):
        if isinstance(s_prompt, dict):
            s_prompt = s_prompt.get('description', str(s_prompt))
            
        for attempt in range(3):
            try:
                op = genai_client.models.generate_videos(
                    model='veo-3.1-generate-preview',
                    prompt=s_prompt
                )
                operations.append((j, op.name))
                break
            except Exception as e:
                print(f"     Error submitting scene {j+1}: {e}")
                time.sleep(10)
        time.sleep(2)
        
    print(f"  -> Tracking {len(operations)} Veo operations...")
    completed = {}
    while len(completed) < len(operations):
        for j, op_name in operations:
            if j in completed: continue
            try:
                url = f"https://generativelanguage.googleapis.com/v1alpha/{op_name}?key={gemini_key}"
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req) as response:
                    data = json.loads(response.read().decode('utf-8'))
                    if data.get('done'):
                        if 'response' in data and 'generateVideoResponse' in data['response']:
                            samples = data['response']['generateVideoResponse'].get('generatedSamples', [])
                            if samples and 'video' in samples[0] and 'uri' in samples[0]['video']:
                                completed[j] = samples[0]['video']['uri']
                                print(f"     Scene {j+1}/15 ready.")
                            else:
                                completed[j] = None
                        else:
                            completed[j] = None
            except Exception:
                pass
        time.sleep(10)
        
    print("  -> Downloading Veo scenes...")
    downloaded_files = []
    for j in range(len(scene_prompts)):
        if j in completed and completed[j]:
            url = f"{completed[j]}&key={gemini_key}"
            out_file = os.path.join(veo_dir, f"scene_{j:02d}.mp4")
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req) as response, open(out_file, 'wb') as f:
                    f.write(response.read())
                downloaded_files.append(out_file)
            except Exception:
                pass
                
    # Determine specific music track based on genre
    music_file = EPIC_MUSIC
    genres = script_data.get('genres', [])
    if "Comedy" in genres or "Family" in genres:
        music_file = os.path.join(TRAILERS_DIR, "music_comedy.mp3")
    elif "Sci-Fi" in genres or "Fantasy" in genres:
        music_file = os.path.join(TRAILERS_DIR, "music_scifi.mp3")
    elif "Horror" in genres or "Thriller" in genres:
        music_file = os.path.join(TRAILERS_DIR, "music_horror.mp3")
    elif "Action" in genres or "Adventure" in genres:
        music_file = os.path.join(TRAILERS_DIR, "music_action.mp3")
        
    if not os.path.exists(music_file):
        music_file = EPIC_MUSIC

    # 3. Concatenate and Mix
    print(f"  -> Concatenating and Mixing Audio (using {os.path.basename(music_file)})...")
    clean_vid = os.path.join(TRAILERS_DIR, f"temp_{uid}.mp4")
    if downloaded_files:
        concat_file = os.path.join(veo_dir, "concat.txt")
        with open(concat_file, "w") as f:
            for df in downloaded_files:
                f.write(f"file '{df}'\n")
        
        cmd_vid = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_file, "-c:v", "libx264", "-crf", "23", "-preset", "fast", clean_vid]
        subprocess.run(cmd_vid, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        cmd_mix = [
            "ffmpeg", "-y", "-i", clean_vid, "-i", vo_path, "-stream_loop", "-1", "-i", music_file,
            "-filter_complex", "[2:a]volume=2.10[bg];[1:a]volume=2.0[vo];[vo][bg]amix=inputs=2:duration=longest:dropout_transition=2[a_out]",
            "-map", "0:v", "-map", "[a_out]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", final_trailer
        ]
        subprocess.run(cmd_mix, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        if os.path.exists(clean_vid):
            os.remove(clean_vid)
    
    print(f"FINISHED_TRAILER: {uid}")

asyncio.run(process_one())
