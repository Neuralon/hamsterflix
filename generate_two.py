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

async def process_all():
    target_uids = ["1cda3e6346d04a4d97c30ebbc09481be", "6c0ef1c6eaea4bc48122abe490a6a61d"]
    for target_uid in target_uids:
        script_data = next((s for s in scripts if s['uid'] == target_uid), None)
        uid = script_data['uid']
        title = script_data.get('inspiration', f"Movie {uid}")
        
        final_trailer = os.path.join(TRAILERS_DIR, f"trailer_{uid}.mp4")
        if os.path.exists(final_trailer):
            os.remove(final_trailer)
            
        print(f"\n=======================================================")
        print(f"Starting STRICT render for {uid} (Inspired by: {title})")
        print(f"=======================================================")
        
        # 1. Voiceover
        vo_path = os.path.join(VOICEOVERS_DIR, f"{uid}_v2.mp3")
        text_to_speak = script_data.get('script_content', '')
        
        # SUPER AGGRESSIVE Regex for parsing out stage directions:
        # Match anything in parentheses (e.g. "(Ominous, low primal growl.)")
        text_to_speak = re.sub(r'\(.*?\)', '', text_to_speak, flags=re.DOTALL)
        
        # Strip all ALL-CAPS headers (e.g. "ON-SCREEN TEXT" or "HAMSTER 1")
        text_to_speak = re.sub(r'^[A-Z0-9 \-]+(?:\s*\([^)]+\))?:\s*', '', text_to_speak, flags=re.MULTILINE)
        
        # Strip out any remaining quotes or brackets
        text_to_speak = text_to_speak.replace('"', '').replace('[', '').replace(']', '').strip()
        
        if not text_to_speak or "no dialogue" in text_to_speak.lower() or "music & visual" in script_data.get('trailer_style', '').lower():
            text_to_speak = "In a world where everything is scarce... Survival is a daily struggle. One hamster will drive for freedom. Furry Fury. The chase is on."
            
        print(f"  -> Generating Cleaned TTS Voiceover: {text_to_speak}")
        await generate_voiceover(text_to_speak, vo_path, script_data.get('audio_direction', ''))

        # Skip Veo rendering because we already successfully generated the MP4s for these 2 trailers
        # Just use the existing temp.mp4 file or the actual trailer_uid.mp4 file!
        veo_dir = os.path.join(TRAILERS_DIR, f"veo_scenes_{uid}")
        clean_vid = os.path.join(TRAILERS_DIR, f"temp_{uid}.mp4")
        
        # Use exactly the unique background track we generated for this specific movie
        music_file = os.path.join(TRAILERS_DIR, f"bgm_{uid}.mp3")
        if not os.path.exists(music_file):
            music_file = EPIC_MUSIC

        # 3. Concatenate and Mix
        print(f"  -> Concatenating and Mixing Audio (using {os.path.basename(music_file)})...")
        
        # Since we skipped Veo download block, we need to rebuild the file list from the directory
        downloaded_files = []
        if os.path.exists(veo_dir):
            import glob
            downloaded_files = sorted(glob.glob(os.path.join(veo_dir, "*.mp4")))
            
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

asyncio.run(process_all())
