import os
import subprocess
import time
from google import genai

UID = "4414013171c34f51b576ba9f98590880"
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
        contents=[uploaded_file, "Analyze this image. Does it contain any humans, people, human hands, human faces, dogs, or cats? Is it just a hamster/rodent? Reply with exactly 'BAD' if there is a person/human part or a dog/cat, or 'CLEAN' if it is only hamsters/rodents/insects/objects."]
    )
    result = resp.text.strip().upper()
    print(f"Scene {i:02d}: {result}")
    if "BAD" in result:
        bad_scenes.append(i)

print(f"Bad scenes found: {bad_scenes}")
