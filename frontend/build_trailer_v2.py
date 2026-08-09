import urllib.request
import urllib.parse
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor

OUTPUT_DIR = "/Users/ckaplan/dev/neuralon/hamster/frontend/public/trailers/v2"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Refined prompts for hyper-realistic, gritty, fast-paced cinematic trailer
prompts = [
    "35mm film still, extreme macro close up of a hamster's eye, reflecting a dark towering concrete maze, gritty dark lighting, anamorphic lens flare, photorealistic",
    "35mm film still, a solitary hamster looking up at massive concrete walls, dense fog, dystopian sci-fi atmosphere, teal and orange color grading",
    "35mm film still, low angle tracking shot of a hamster running furiously down a dark corridor, heavy motion blur, intense action lighting, photorealistic",
    "35mm film still, POV shot from behind a hamster looking down a seemingly endless mechanical hallway, flickering fluorescent lights, cinematic depth of field",
    "35mm film still, extreme close up of hamster paws sprinting on rough concrete, flying dust particles, shallow focus, gritty action movie",
    "35mm film still, hamster hiding in a shadow, looking terrified over its shoulder, harsh dramatic rim lighting, cinematic",
    "35mm film still, giant mechanical gears shifting in a concrete maze, sparks flying, tiny hamster leaping away, high-stakes action",
    "35mm film still, low angle, a massive glowing sunflower seed on a pedestal in a dark industrial room, cinematic volumetric lighting, god rays",
    "35mm film still, hamster in mid-air leaping across a chasm in the maze, slow motion aesthetic, epic backlight, photorealistic",
    "35mm film still, silhouette of a hamster against a bright blinding white exit door, dust motes in the air, triumphant cinematic ending"
]

def fetch_image(i, prompt):
    encoded = urllib.parse.quote(prompt + ", masterpiece, highly detailed")
    url = f"https://image.pollinations.ai/prompt/{encoded}?width=1920&height=1080&nologo=true&seed=888"
    out = os.path.join(OUTPUT_DIR, f"scene_{i:02d}.jpg")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as resp, open(out, 'wb') as f:
            f.write(resp.read())
        print(f"Downloaded {out}")
        return out
    except Exception as e:
        print(f"Failed {out}: {e}")
        return None

# Download in parallel
with ThreadPoolExecutor(max_workers=5) as executor:
    results = list(executor.map(lambda x: fetch_image(x[0], x[1]), enumerate(prompts)))

# Build FFmpeg command for dynamic zoom/pan and fast cuts
# We will create a complex filtergraph
print("Building video with ffmpeg...")

inputs = []
filter_parts = []
for i in range(10):
    inputs.extend(["-i", os.path.join(OUTPUT_DIR, f"scene_{i:02d}.jpg")])
    
    # Alternate zoom directions to make it feel chaotic and fast-paced
    if i % 3 == 0:
        # Zoom in
        zoom = "zoompan=z='min(zoom+0.003,1.5)':d=36:s=1920x1080"
    elif i % 3 == 1:
        # Pan right
        zoom = "zoompan=z='1.2':x='x+2':y='y':d=36:s=1920x1080"
    else:
        # Zoom out slightly (start zoomed in)
        zoom = "zoompan=z='max(1.3-0.002*in,1.0)':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d=36:s=1920x1080"
        
    filter_parts.append(f"[{i}:v]format=yuv420p,{zoom}[v{i}];")

concat_inputs = "".join([f"[v{i}]" for i in range(10)])
filter_complex = "".join(filter_parts) + f"{concat_inputs}concat=n=10:v=1:a=0[outv]"

final_output = "/Users/ckaplan/dev/neuralon/hamster/frontend/public/trailers/trailer_2.mp4"
cmd = [
    "ffmpeg", "-y",
    *inputs,
    "-filter_complex", filter_complex,
    "-map", "[outv]",
    "-c:v", "libx264", "-preset", "fast", "-crf", "23",
    "-r", "24",
    final_output
]

subprocess.run(cmd, check=True)
print("FAST-PACED TRAILER GENERATED SUCCESSFULLY!")
