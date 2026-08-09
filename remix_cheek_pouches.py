import os
import subprocess

TRAILERS_DIR = "/Users/ckaplan/dev/neuralon/hamster/frontend/public/trailers"
UID = "c99b8b0489f84fbea28b69b1f9194b85"

vo_path = os.path.join(TRAILERS_DIR, f"../voiceovers/{UID}_indy.mp3")
vid_path = os.path.join(TRAILERS_DIR, f"temp_{UID}.mp4")
final_path = os.path.join(TRAILERS_DIR, f"trailer_{UID}.mp4")
bgm_path = os.path.join(TRAILERS_DIR, "real_indy.mp3")
concat_txt = os.path.join(TRAILERS_DIR, f"veo_scenes_{UID}", "concat.txt")

print("Mixing Real Indiana Jones Soundtrack (Quarter Volume)...")
subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_txt, "-c:v", "libx264", "-crf", "23", "-preset", "fast", vid_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Dropped the background music volume from 0.9 to 0.45 (half again), kept voice at 2.5
subprocess.run([
    "ffmpeg", "-y", "-i", vid_path, "-i", vo_path, "-ss", "00:00:15", "-i", bgm_path,
    "-filter_complex", "[2:a]volume=0.45[bg];[1:a]volume=2.5[vo];[vo][bg]amix=inputs=2:duration=longest:dropout_transition=2[a_out]",
    "-map", "0:v", "-map", "[a_out]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", final_path
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if os.path.exists(vid_path):
    os.remove(vid_path)

print("COMPLETED CHEEK POUCHES MIX!")
