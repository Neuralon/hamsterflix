import os
import json
import subprocess
import time
import urllib.request
from google import genai
from google.genai import types

UID = "b6881111fcfa4e84af5ff0bcaf6c5a82"
BASE_DIR = "/Users/ckaplan/dev/neuralon/hamster/frontend/public"
SCRIPTS_FILE = os.path.join(BASE_DIR, "trailer_scripts.json")
TRAILERS_DIR = os.path.join(BASE_DIR, "trailers")
VEO_DIR = os.path.join(TRAILERS_DIR, f"veo_scenes_{UID}")

gemini_key = os.getenv('GEMINI_API_KEY')
client = genai.Client(api_key=gemini_key, http_options={'api_version':'v1alpha'})

with open(SCRIPTS_FILE, 'r') as f:
    scripts = json.load(f)
script_data = next(s for s in scripts if s['uid'] == UID)
scene_prompts = script_data.get('scenes', [])[:15]

bad_indices = [6, 7, 11, 12, 13]
operations = []

print("Re-generating bad scenes with STRICT anti-human constraints...")
for j in bad_indices:
    s_prompt = scene_prompts[j]
    if isinstance(s_prompt, dict):
        s_prompt = s_prompt.get('description', str(s_prompt))
    
    strict_prompt = f"{s_prompt} CRITICAL CONSTRAINT: Featuring ONLY literal furry animal hamsters. ABSOLUTELY NO HUMANS, NO PEOPLE, NO HUMAN HANDS, NO HUMAN FACES. Entirely populated by literal rodent hamsters."
    
    for attempt in range(3):
        try:
            op = client.models.generate_videos(
                model='veo-3.1-generate-preview',
                prompt=strict_prompt
            )
            operations.append((j, op.name))
            break
        except Exception as e:
            print(f"Error submitting {j}: {e}")
            time.sleep(10)
    time.sleep(2)

print("Waiting for Veo...")
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
                    samples = data.get('response', {}).get('generateVideoResponse', {}).get('generatedSamples', [])
                    if samples and 'video' in samples[0]:
                        completed[j] = samples[0]['video']['uri']
                        print(f"Scene {j} ready.")
                    else:
                        completed[j] = None
        except Exception:
            pass
    time.sleep(10)

print("Downloading fixed scenes...")
for j in bad_indices:
    if j in completed and completed[j]:
        url = f"{completed[j]}&key={gemini_key}"
        out_file = os.path.join(VEO_DIR, f"scene_{j:02d}.mp4")
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(out_file, 'wb') as f:
            f.write(response.read())

print("Re-mixing final trailer with REAL Oz music...")
vo_oz = os.path.join(TRAILERS_DIR, f"../voiceovers/{UID}_oz.mp3")
vid_oz = os.path.join(TRAILERS_DIR, f"temp_{UID}.mp4")
final_oz = os.path.join(TRAILERS_DIR, f"trailer_{UID}.mp4")
bgm_oz = os.path.join(TRAILERS_DIR, "real_oz.mp3")

concat_txt_oz = os.path.join(VEO_DIR, "concat.txt")
subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_txt_oz, "-c:v", "libx264", "-crf", "23", "-preset", "fast", vid_oz], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run([
    "ffmpeg", "-y", "-i", vid_oz, "-i", vo_oz, "-ss", "00:00:05", "-i", bgm_oz,
    "-filter_complex", "[2:a]volume=1.4[bg];[1:a]volume=2.2[vo];[vo][bg]amix=inputs=2:duration=longest:dropout_transition=2[a_out]",
    "-map", "0:v", "-map", "[a_out]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", final_oz
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

os.remove(vid_oz)
print("COMPLETED CAGE BREAK FIX!")
