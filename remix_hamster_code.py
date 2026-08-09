import os
import json
import subprocess
import time
import asyncio
import edge_tts
from google import genai
from google.genai import types

UID = "1cda3e6346d04a4d97c30ebbc09481be"
BASE_DIR = "/Users/ckaplan/dev/neuralon/hamster/frontend/public"
TRAILERS_DIR = os.path.join(BASE_DIR, "trailers")
VEO_DIR = os.path.join(TRAILERS_DIR, f"veo_scenes_{UID}")
FRAMES_DIR = os.path.join(VEO_DIR, "frames")
VOICEOVERS_DIR = os.path.join(BASE_DIR, "voiceovers")
os.makedirs(FRAMES_DIR, exist_ok=True)

FINAL_TRAILER = os.path.join(TRAILERS_DIR, f"trailer_{UID}.mp4")

# Extract 1 frame per scene
for i in range(15):
    vid = os.path.join(VEO_DIR, f"scene_{i:02d}.mp4")
    frame = os.path.join(FRAMES_DIR, f"frame_{i:02d}.jpg")
    if not os.path.exists(frame) and os.path.exists(vid):
        subprocess.run(["ffmpeg", "-y", "-i", vid, "-ss", "00:00:02", "-vframes", "1", frame], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

gemini_key = os.getenv('GEMINI_API_KEY')
client = genai.Client(api_key=gemini_key, http_options={'api_version':'v1alpha'})

# Upload files to Gemini
uploaded_files = []
for i in range(15):
    frame = os.path.join(FRAMES_DIR, f"frame_{i:02d}.jpg")
    if os.path.exists(frame):
        uploaded_files.append(client.files.upload(file=frame))

prompt = """
These are 15 sequential frames from an AI-generated movie trailer for 'The Hamster Code' (a parody of The Da Vinci Code starring hamsters).
I need you to write the audio script for this exact 75-second trailer. 

REQUIREMENTS:
1. The script MUST feature a British Woman as the NARRATOR.
2. It MUST feature real dialogue between two male characters: ROBERT (American male hamster) and LEIGH (British male hamster).
3. The pacing must stretch across 75 seconds. Match the vibe of the images (suspenseful, mystery, looking at clues, running from danger).
4. Output ONLY a valid JSON array of dialogue objects. 

Format exactly like this:
[
  {"character": "NARRATOR", "text": "For centuries, a secret has been buried in the shavings..."},
  {"character": "ROBERT", "text": "Look at this sunflower seed. The markings... it's a map."},
  {"character": "LEIGH", "text": "Good heavens... the sacred wheel!"}
]
"""

print("Analyzing footage with Gemini...")
resp = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[*uploaded_files, prompt]
)
raw = resp.text.replace('```json', '').replace('```', '').strip()
dialogue_plan = json.loads(raw)

async def generate_all_audio(plan):
    audio_files = []
    for idx, line in enumerate(plan):
        char = line['character'].upper()
        text = line['text']
        out_path = os.path.join(VOICEOVERS_DIR, f"{UID}_line_{idx}.mp3")
        
        # Voice mapping
        voice = "en-GB-SoniaNeural" # Default NARRATOR (British Woman)
        if "ROBERT" in char:
            voice = "en-US-GuyNeural" # American Male
        elif "LEIGH" in char:
            voice = "en-GB-RyanNeural" # British Male
            
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(out_path)
        audio_files.append(out_path)
    return audio_files

print("Generating dynamic dialogue voices...")
audio_files = asyncio.run(generate_all_audio(dialogue_plan))

# Concat voices with silence spacing to fill ~70 seconds
print("Spacing and mixing dialogue...")
concat_txt = os.path.join(VOICEOVERS_DIR, f"{UID}_voice_concat.txt")
with open(concat_txt, "w") as f:
    for af in audio_files:
        f.write(f"file '{af}'\n")
        # Add 1.5 seconds of silence between lines
        f.write(f"file '/tmp/silence.mp3'\n")

# Create a 1.5s silence file
subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-t", "1.5", "-q:a", "9", "-acodec", "libmp3lame", "/tmp/silence.mp3"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

mixed_vo = os.path.join(VOICEOVERS_DIR, f"{UID}_final_vo.mp3")
subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_txt, "-c", "copy", mixed_vo], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Generate ENTIRELY NEW custom suspense music using FFmpeg synthesizers!
print("Synthesizing custom suspense ticking-clock music...")
custom_music = os.path.join(TRAILERS_DIR, f"bgm_{UID}_custom.mp3")
music_cmd = [
    "ffmpeg", "-y", "-f", "lavfi",
    # Drone + Ticking clock
    "-i", "aevalsrc='0.2*sin(2*PI*50*t) + 0.1*sin(2*PI*300*t)':duration=75[drone]; aevalsrc='0.6*sin(2*PI*800*t)*exp(-15*(t-floor(t)))':duration=75[tick]; [drone][tick]amix=inputs=2,volume=1.5",
    "-c:a", "libmp3lame", "-q:a", "2", custom_music
]
subprocess.run(music_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("Mixing final trailer...")
clean_vid = os.path.join(TRAILERS_DIR, f"temp_{UID}.mp4")
concat_vid_txt = os.path.join(VEO_DIR, "concat.txt")
subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_vid_txt, "-c:v", "libx264", "-crf", "23", "-preset", "fast", clean_vid], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

cmd_mix = [
    "ffmpeg", "-y", "-i", clean_vid, "-i", mixed_vo, "-stream_loop", "-1", "-i", custom_music,
    "-filter_complex", "[2:a]volume=2.10[bg];[1:a]volume=2.0[vo];[vo][bg]amix=inputs=2:duration=longest:dropout_transition=2[a_out]",
    "-map", "0:v", "-map", "[a_out]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", FINAL_TRAILER
]
subprocess.run(cmd_mix, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

os.remove(clean_vid)
print("COMPLETED!")
