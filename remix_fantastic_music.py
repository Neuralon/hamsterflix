import os
import subprocess

UID = "ce7b5e54b3d04b36858681c2529f5016"
BASE_DIR = "/Users/ckaplan/dev/neuralon/hamster/frontend/public"
TRAILERS_DIR = os.path.join(BASE_DIR, "trailers")
VEO_DIR = os.path.join(TRAILERS_DIR, f"veo_scenes_{UID}")
VOICEOVERS_DIR = os.path.join(BASE_DIR, "voiceovers")

FINAL_TRAILER = os.path.join(TRAILERS_DIR, f"trailer_{UID}.mp4")
VO_PATH = os.path.join(VOICEOVERS_DIR, f"{UID}_v2.mp3")

print("Synthesizing magical/whimsical fantasy music for Fantastic Hamsters...")
# Generate completely unique magical fantasy music using FFmpeg
# High pitched bells, sweeping chimes, whimsical theremin vibe
custom_music = os.path.join(TRAILERS_DIR, f"bgm_{UID}_custom.mp3")
music_cmd = [
    "ffmpeg", "-y", "-f", "lavfi",
    "-i", "sine=frequency=880:duration=75[s1]; sine=frequency=1100:duration=75[s2]; aevalsrc='0.3*sin(2*PI*1500*t)*exp(-3*(t-floor(t)))':duration=75[chimes]; [s1][s2]amix=inputs=2,tremolo=f=5:d=0.8,vibrato=f=4:d=0.3[melody]; [melody][chimes]amix=inputs=2,flanger=delay=15:depth=3:regen=50:width=80,volume=1.2",
    "-c:a", "libmp3lame", "-q:a", "2", custom_music
]
subprocess.run(music_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("Mixing final trailer with new music...")
clean_vid = os.path.join(TRAILERS_DIR, f"temp_{UID}.mp4")
concat_vid_txt = os.path.join(VEO_DIR, "concat.txt")
subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_vid_txt, "-c:v", "libx264", "-crf", "23", "-preset", "fast", clean_vid], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

cmd_mix = [
    "ffmpeg", "-y", "-i", clean_vid, "-i", VO_PATH, "-stream_loop", "-1", "-i", custom_music,
    "-filter_complex", "[2:a]volume=2.10[bg];[1:a]volume=2.0[vo];[vo][bg]amix=inputs=2:duration=longest:dropout_transition=2[a_out]",
    "-map", "0:v", "-map", "[a_out]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", FINAL_TRAILER
]
subprocess.run(cmd_mix, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

os.remove(clean_vid)
print("COMPLETED REMIX!")
