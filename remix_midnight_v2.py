import os
import subprocess
import asyncio
import edge_tts

UID = "c4cd6d2e32aa453c8ca055e166eef8ee"
BASE_DIR = "/Users/ckaplan/dev/neuralon/hamster/frontend/public"
TRAILERS_DIR = os.path.join(BASE_DIR, "trailers")
VOICEOVERS_DIR = os.path.join(BASE_DIR, "voiceovers")
VEO_DIR = os.path.join(TRAILERS_DIR, f"veo_scenes_{UID}")
FINAL_TRAILER = os.path.join(TRAILERS_DIR, f"trailer_{UID}.mp4")

# Re-record Midnight Express with much longer, spaced-out pacing so it lasts 75 seconds.
# We will use short silences to space the dialogue out.
dialogue = [
    "I didn't plan on smuggling the seeds.",
    "It was a mistake.",
    "One little mistake.",
    "Now I'm in the deepest, darkest cage in the house.",
    "Turkish Prison? No.",
    "The basement terrarium.",
    "The wheel never stops turning here.",
    "The water bottle always drips.",
    "They call it the Midnight Express...",
    "...because if you don't get out by midnight, the cat wakes up.",
    "And nobody escapes the cat.",
    "My name is Billy Hamster.",
    "And this... is my escape."
]

async def gen_audio():
    audio_files = []
    for idx, text in enumerate(dialogue):
        out_path = os.path.join(VOICEOVERS_DIR, f"{UID}_midnight_line_{idx}.mp3")
        communicate = edge_tts.Communicate(text, "en-US-BrianNeural", rate="-15%") # Slower pacing
        await communicate.save(out_path)
        audio_files.append(out_path)
    return audio_files

print("Generating spaced-out monologue for Midnight Runner...")
audio_files = asyncio.run(gen_audio())

# Concat with 3 seconds of silence between each line to stretch it over 75 seconds
concat_txt = os.path.join(VOICEOVERS_DIR, f"{UID}_midnight_concat.txt")
with open(concat_txt, "w") as f:
    for af in audio_files:
        f.write(f"file '{af}'\n")
        f.write(f"file '/tmp/silence_3s.mp3'\n")

# Create a 3s silence file
subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-t", "3", "-q:a", "9", "-acodec", "libmp3lame", "/tmp/silence_3s.mp3"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
mixed_vo = os.path.join(VOICEOVERS_DIR, f"{UID}_final_midnight_vo.mp3")
subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_txt, "-c", "copy", mixed_vo], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


print("Synthesizing Giorgio Moroder 'Chase' music...")
bgm_midnight = os.path.join(TRAILERS_DIR, f"bgm_{UID}_moroder.mp3")
# The previous synth was too quiet/ambient. We need a driving, fast-paced electronic pulse.
subprocess.run([
    "ffmpeg", "-y", "-f", "lavfi",
    # Fast 16th note synth arpeggiator on a minor chord (C minor) to sound exactly like Giorgio Moroder
    "-i", "aevalsrc='0.8*sin(2*PI*261.63*t)*exp(-10*(t-floor(t*8)/8)) + 0.8*sin(2*PI*311.13*t)*exp(-10*(t-floor(t*8+1)/8)) + 0.8*sin(2*PI*392.00*t)*exp(-10*(t-floor(t*8+2)/8))':duration=75",
    "-c:a", "libmp3lame", "-q:a", "2", bgm_midnight
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

clean_vid = os.path.join(TRAILERS_DIR, f"temp_{UID}.mp4")
concat_vid_txt = os.path.join(VEO_DIR, "concat.txt")
subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_vid_txt, "-c:v", "libx264", "-crf", "23", "-preset", "fast", clean_vid], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("Mixing final Midnight Runner trailer...")
cmd_mix = [
    "ffmpeg", "-y", "-i", clean_vid, "-i", mixed_vo, "-stream_loop", "-1", "-i", bgm_midnight,
    "-filter_complex", "[2:a]volume=2.5[bg];[1:a]volume=2.5[vo];[vo][bg]amix=inputs=2:duration=longest:dropout_transition=2[a_out]",
    "-map", "0:v", "-map", "[a_out]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", FINAL_TRAILER
]
subprocess.run(cmd_mix, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

os.remove(clean_vid)
print("COMPLETED MIDNIGHT RUNNER!")
