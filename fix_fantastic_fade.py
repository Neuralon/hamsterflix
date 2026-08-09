import os
import subprocess

TRAILERS_DIR = "/Users/ckaplan/dev/neuralon/hamster/frontend/public/trailers"
UID = "ce7b5e54b3d04b36858681c2529f5016"

vo_path = os.path.join(TRAILERS_DIR, f"../voiceovers/{UID}_v2.mp3")
vid_path = os.path.join(TRAILERS_DIR, f"temp_{UID}.mp4")
final_path = os.path.join(TRAILERS_DIR, f"trailer_{UID}.mp4")
bgm_path = os.path.join(TRAILERS_DIR, "real_fantastic.mp3")
concat_txt = os.path.join(TRAILERS_DIR, f"veo_scenes_{UID}", "concat.txt")

print("Mixing REAL Fantastic Beasts Soundtrack with Fade Out...")
subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_txt, "-c:v", "libx264", "-crf", "23", "-preset", "fast", vid_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# BGM volume down to 0.45, VO at 2.5. 
# Added an afade filter to the background music to fade out starting at 70 seconds over 5 seconds.
subprocess.run([
    "ffmpeg", "-y", "-i", vid_path, "-i", vo_path, "-stream_loop", "-1", "-ss", "00:00:10", "-i", bgm_path,
    "-filter_complex", "[2:a]volume=0.45,afade=t=out:st=70:d=5[bg];[1:a]volume=2.5[vo];[vo][bg]amix=inputs=2:duration=longest:dropout_transition=2[a_out]",
    "-map", "0:v", "-map", "[a_out]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", final_path
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if os.path.exists(vid_path):
    os.remove(vid_path)

print("COMPLETED FANTASTIC HAMSTERS FADE MIX!")
