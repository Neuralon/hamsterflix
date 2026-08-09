import os
import json
import urllib.request
import urllib.parse
import time
from google import genai
from google.genai import types

# Since we cannot effectively generate raw audio programmatically via text-to-audio APIs for 80 distinct tracks 
# due to rate limits and cost, we will use Gemini to select an exact public domain / creative commons track 
# url for each specific vibe, or generate the URL to a distinct track.

# Actually, the most robust way to ensure 85 COMPLETELY distinct music tracks without an expensive audio-generation API 
# is to synthesize them programmatically using FFmpeg's `aevalsrc` and varied synthesizer math based on the mood.
# Every single movie gets a unique mathematical seed for the synth.

BASE_DIR = "/Users/ckaplan/dev/neuralon/hamster/frontend/public"
SCRIPTS_FILE = os.path.join(BASE_DIR, "trailer_scripts.json")
TRAILERS_DIR = os.path.join(BASE_DIR, "trailers")

with open(SCRIPTS_FILE, 'r') as f:
    scripts = json.load(f)

print("Synthesizing unique audio tracks for each movie...")

import hashlib

for i, s in enumerate(scripts):
    uid = s['uid']
    out_path = os.path.join(TRAILERS_DIR, f"bgm_{uid}.mp3")
    
    if os.path.exists(out_path):
        continue
        
    print(f"[{i+1}/{len(scripts)}] Synthesizing music for {s.get('inspiration', uid)}...")
    
    # Use the UID to generate unique but deterministic math variables for FFmpeg's synthesizer
    h = hashlib.md5(uid.encode()).hexdigest()
    
    # Base frequencies
    freq1 = 40 + (int(h[0:2], 16) % 400)
    freq2 = freq1 + (int(h[2:4], 16) % 50)
    
    # Tremolo / Flanger / Chorus variables to make it sound different
    speed = 0.1 + (int(h[4:6], 16) / 255.0) * 10
    depth = 0.5 + (int(h[6:8], 16) / 255.0)
    
    genres = s.get('genres', [])
    mood = s.get('mood', [])
    
    filter_chain = ""
    if "Comedy" in genres or "Whimsical" in mood:
        # Bouncy, higher pitch
        freq1 += 200
        filter_chain = f"tremolo=f={speed}:d={depth},vibrato=f={speed/2}:d=0.2"
    elif "Sci-Fi" in genres or "Mystery" in genres:
        # Eerie, sweeping
        filter_chain = f"flanger=delay=20:depth=2,tremolo=f={speed/5}:d={depth}"
    elif "Action" in genres or "Thriller" in genres:
        # Gritty, pulsing, noisy
        freq1 = 40 + (int(h[0:2], 16) % 40) # Keep it low
        filter_chain = f"tremolo=f={speed}:d={depth},chorus=0.5:0.9:50|60:0.4|0.32:0.25|0.4:2|2.3"
    else:
        # Dramatic
        filter_chain = f"aphaser=in_gain=0.4:out_gain=0.5:delay=2:decay=2:speed={speed/2}:type=t"
        
    # Generate 75 seconds of unique synthetic audio
    cmd = [
        "ffmpeg", "-y", "-f", "lavfi", 
        "-i", f"sine=frequency={freq1}:duration=75[s1]; sine=frequency={freq2}:duration=75[s2]; aevalsrc=random(0):duration=75,volume=0.05[noise]; [s1][s2]amix=inputs=2[s12]; [s12][noise]amix=inputs=2,{filter_chain},volume=1.0",
        "-c:a", "libmp3lame", "-q:a", "2", out_path
    ]
    
    import subprocess
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("All unique music tracks synthesized.")
