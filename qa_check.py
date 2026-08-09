import os
import subprocess
import time
from google import genai
from google.genai import types

UID = "b6881111fcfa4e84af5ff0bcaf6c5a82"
VEO_DIR = f"/Users/ckaplan/dev/neuralon/hamster/frontend/public/trailers/veo_scenes_{UID}"

gemini_key = os.getenv('GEMINI_API_KEY')
client = genai.Client(api_key=gemini_key, http_options={'api_version':'v1alpha'})

bad_scenes = []

for i in range(15):
    vid = os.path.join(VEO_DIR, f"scene_{i:02d}.mp4")
    if not os.path.exists(vid): continue
    
    frame = os.path.join(VEO_DIR, f"qa_frame_{i:02d}.jpg")
    subprocess.run(["ffmpeg", "-y", "-i", vid, "-ss", "00:00:02", "-vframes", "1", frame], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    uploaded_file = client.files.upload(file=frame)
    resp = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[uploaded_file, "Analyze this image. Does it contain any humans, people, human hands, or human faces? Is it just a hamster/animal? Reply with exactly 'HUMAN' if there is a person/human part, or 'CLEAN' if it is only hamsters/animals/objects."]
    )
    result = resp.text.strip().upper()
    print(f"Scene {i:02d}: {result}")
    if "HUMAN" in result:
        bad_scenes.append(i)

print(f"Bad scenes found: {bad_scenes}")
