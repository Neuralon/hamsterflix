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

# Find Sunflower Seeds (Dune parody)
target_uid = "1911e0baa13b46708b5569b2c3cf63d5"
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
    if not text_to_speak or "no dialogue" in text_to_speak.lower() or "music & scenes" in script_data.get('trailer_style', '').lower():
        text_to_speak = "Coming soon to Hamsterflix."
    
    # Clean up script tags like "VOICEOVER: " or "HAMSTER 1: " so the TTS doesn't read them aloud!
    text_to_speak = re.sub(r'^[A-Z0-9 ]+:\s*', '', text_to_speak, flags=re.MULTILINE)
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
                
    # 3. Concatenate and Mix
    print("  -> Concatenating and Mixing Audio (Looped Music)...")
    clean_vid = os.path.join(TRAILERS_DIR, f"temp_{uid}.mp4")
    if downloaded_files:
        concat_file = os.path.join(veo_dir, "concat.txt")
        with open(concat_file, "w") as f:
            for df in downloaded_files:
                f.write(f"file '{df}'\n")
        
        cmd_vid = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_file, "-c:v", "libx264", "-crf", "23", "-preset", "fast", clean_vid]
        subprocess.run(cmd_vid, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # We add -stream_loop -1 to the music to ensure it covers the whole 75s video!
        # We use duration=longest in amix, and -shortest on the output to cut exactly when the video ends.
        cmd_mix = [
            "ffmpeg", "-y", "-i", clean_vid, "-i", vo_path, "-stream_loop", "-1", "-i", EPIC_MUSIC,
            "-filter_complex", "[2:a]volume=2.10[bg];[1:a]volume=2.0[vo];[vo][bg]amix=inputs=2:duration=longest:dropout_transition=2[a_out]",
            "-map", "0:v", "-map", "[a_out]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", final_trailer
        ]
        subprocess.run(cmd_mix, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        if os.path.exists(clean_vid):
            os.remove(clean_vid)
    
    print(f"FINISHED_TRAILER: {uid}")

asyncio.run(process_one())
