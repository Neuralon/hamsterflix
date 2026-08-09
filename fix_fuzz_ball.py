import os
import json
import subprocess
import time
import urllib.request
from google import genai
from google.genai import types

UID = "4414013171c34f51b576ba9f98590880"
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

bad_indices = [2, 3, 4, 10, 12, 14] # Adding 14 as user mentioned "in the end" just to be safe if it was missed, but wait, scene 14 might be missing or I didn't test it?
# Let's check if 14 exists. The QA check went up to 13.
# Let's re-read the array. Actually `range(15)` goes 0 to 14.
# Scene 14 might not have existed or was CLEAN. But user said "in the end". Let's regenerate 14 just in case.

operations = []

print("Re-generating bad scenes with STRICT anti-human/anti-dog constraints...")
for j in bad_indices:
    s_prompt = ""
    if j < len(scene_prompts):
        s_prompt = scene_prompts[j]
        if isinstance(s_prompt, dict):
            s_prompt = s_prompt.get('description', str(s_prompt))
    else:
        s_prompt = "A hamster sitting on a park bench."
        
    strict_prompt = f"{s_prompt} CRITICAL CONSTRAINT: Featuring ONLY literal furry animal hamsters. ABSOLUTELY NO HUMANS, NO PEOPLE, NO HUMAN HANDS, NO DOGS, NO CATS, NO OTHER ANIMALS. Entirely populated by literal rodent hamsters."
    
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

print("Re-mixing final trailer with REAL Forrest Gump music...")
vo_gump = os.path.join(TRAILERS_DIR, f"../voiceovers/{UID}_gump.mp3")
vid_gump = os.path.join(TRAILERS_DIR, f"temp_{UID}.mp4")
final_gump = os.path.join(TRAILERS_DIR, f"trailer_{UID}.mp4")
bgm_gump = os.path.join(TRAILERS_DIR, "gump.mp3")

concat_txt_gump = os.path.join(VEO_DIR, "concat.txt")
subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_txt_gump, "-c:v", "libx264", "-crf", "23", "-preset", "fast", vid_gump], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run([
    "ffmpeg", "-y", "-i", vid_gump, "-i", vo_gump, "-ss", "00:00:00", "-i", bgm_gump,
    "-filter_complex", "[2:a]volume=1.5[bg];[1:a]volume=2.5[vo];[vo][bg]amix=inputs=2:duration=longest:dropout_transition=2[a_out]",
    "-map", "0:v", "-map", "[a_out]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", final_gump
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if os.path.exists(vid_gump): os.remove(vid_gump)
print("COMPLETED FUZZ BALL FIX!")
