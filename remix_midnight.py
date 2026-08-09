import os
import json
import subprocess
import asyncio
import edge_tts
from google import genai

UID = "c4cd6d2e32aa453c8ca055e166eef8ee"
BASE_DIR = "/Users/ckaplan/dev/neuralon/hamster/frontend/public"
TRAILERS_DIR = os.path.join(BASE_DIR, "trailers")
VOICEOVERS_DIR = os.path.join(BASE_DIR, "voiceovers")
VEO_DIR = os.path.join(TRAILERS_DIR, f"veo_scenes_{UID}")

FINAL_TRAILER = os.path.join(TRAILERS_DIR, f"trailer_{UID}.mp4")
vo_path = os.path.join(VOICEOVERS_DIR, f"{UID}_midnight.mp3")

async def gen_vo(text, path, voice):
    communicate = edge_tts.Communicate(text, voice, rate="+0%")
    await communicate.save(path)

# Let's write a proper, intense Midnight Express style voiceover
# Parody of the famous Billy Hayes monologue/trailer style
script = "I didn't plan on smuggling the seeds. It was a mistake. One little mistake. Now I'm in the deepest, darkest cage in the house. Turkish Prison? No. The basement terrarium. The wheel never stops turning here. The water bottle always drips. They call it the Midnight Express... because if you don't get out by midnight, the cat wakes up. And nobody escapes the cat. My name is Billy Hamster. And this... is my escape."

print("Generating desperate, gritty monologue for Midnight Runner...")
asyncio.run(gen_vo(script, vo_path, "en-US-BrianNeural"))

print("Synthesizing Giorgio Moroder-style 70s Synth thriller music...")
bgm_midnight = os.path.join(TRAILERS_DIR, f"bgm_{UID}_moroder.mp3")
# Create a pulsing 70s arpeggiator / synth wave baseline (Giorgio Moroder style Chase theme)
subprocess.run([
    "ffmpeg", "-y", "-f", "lavfi",
    "-i", "aevalsrc='0.6*sin(2*PI*50*t)*exp(-5*(t-floor(t*4)/4)) + 0.4*sin(2*PI*200*t)*exp(-5*(t-floor(t*8)/8))':duration=75",
    "-c:a", "libmp3lame", "-q:a", "2", bgm_midnight
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

clean_vid = os.path.join(TRAILERS_DIR, f"temp_{UID}.mp4")
concat_vid_txt = os.path.join(VEO_DIR, "concat.txt")
subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_vid_txt, "-c:v", "libx264", "-crf", "23", "-preset", "fast", clean_vid], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("Mixing final trailer...")
cmd_mix = [
    "ffmpeg", "-y", "-i", clean_vid, "-i", vo_path, "-stream_loop", "-1", "-i", bgm_midnight,
    "-filter_complex", "[2:a]volume=1.5[bg];[1:a]volume=2.5[vo];[vo][bg]amix=inputs=2:duration=longest:dropout_transition=2[a_out]",
    "-map", "0:v", "-map", "[a_out]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", FINAL_TRAILER
]
subprocess.run(cmd_mix, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
os.remove(clean_vid)

print("MIDNIGHT RUNNER COMPLETE")
