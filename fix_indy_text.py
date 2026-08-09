import os
import subprocess
import time
import urllib.request
from google import genai

UID = "c99b8b0489f84fbea28b69b1f9194b85"
BASE_DIR = "/Users/ckaplan/dev/neuralon/hamster/frontend/public"
TRAILERS_DIR = os.path.join(BASE_DIR, "trailers")
VEO_DIR = os.path.join(TRAILERS_DIR, f"veo_scenes_{UID}")

gemini_key = os.getenv('GEMINI_API_KEY')
client = genai.Client(api_key=gemini_key, http_options={'api_version':'v1alpha'})

# 27 seconds is in Scene 5 (since each scene is ~5 seconds: 0-5s is scene 0, 5-10 is scene 1, 10-15s is scene 2, 15-20 is scene 3, 20-25 is scene 4, 25-30 is scene 5)
bad_index = 5

print("Re-generating Scene 5 without text...")

strict_prompt = "[Medium Shot] A massive, perfectly spherical sunflower seed begins to roll down the tunnel towards Professor Cheeks and his sidekick. They turn and run frantically towards the camera. CRITICAL CONSTRAINT: Featuring ONLY literal furry animal hamsters. ABSOLUTELY NO TEXT. NO WORDS. NO LETTERS. NO SUBTITLES. NO WATERMARKS. NO GIBBERISH ON SCREEN."

op = client.models.generate_videos(
    model='veo-3.1-generate-preview',
    prompt=strict_prompt
)

print(f"Tracking operation {op.name}...")
completed_url = None
while not completed_url:
    try:
        url = f"https://generativelanguage.googleapis.com/v1alpha/{op.name}?key={gemini_key}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            if data.get('done'):
                samples = data.get('response', {}).get('generateVideoResponse', {}).get('generatedSamples', [])
                if samples and 'video' in samples[0]:
                    completed_url = samples[0]['video']['uri']
                    print(f"Scene 5 ready.")
                else:
                    break
    except Exception:
        pass
    time.sleep(10)

if completed_url:
    print("Downloading fixed scene...")
    url = f"{completed_url}&key={gemini_key}"
    out_file = os.path.join(VEO_DIR, f"scene_{bad_index:02d}.mp4")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response, open(out_file, 'wb') as f:
        f.write(response.read())

print("Re-mixing final Indiana Jones trailer...")
vo_indy = os.path.join(TRAILERS_DIR, f"../voiceovers/{UID}_indy.mp3")
vid_indy = os.path.join(TRAILERS_DIR, f"temp_{UID}.mp4")
final_indy = os.path.join(TRAILERS_DIR, f"trailer_{UID}.mp4")
bgm_indy = os.path.join(TRAILERS_DIR, "real_indy.mp3")

concat_txt_indy = os.path.join(VEO_DIR, "concat.txt")
subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_txt_indy, "-c:v", "libx264", "-crf", "23", "-preset", "fast", vid_indy], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

subprocess.run([
    "ffmpeg", "-y", "-i", vid_indy, "-i", vo_indy, "-ss", "00:00:15", "-i", bgm_indy,
    "-filter_complex", "[2:a]volume=0.45[bg];[1:a]volume=2.5[vo];[vo][bg]amix=inputs=2:duration=longest:dropout_transition=2[a_out]",
    "-map", "0:v", "-map", "[a_out]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", final_indy
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

os.remove(vid_indy)
print("COMPLETED INDY TEXT FIX!")
