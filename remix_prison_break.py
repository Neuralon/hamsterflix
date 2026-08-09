import os
import subprocess

TRAILERS_DIR = "/Users/ckaplan/dev/neuralon/hamster/frontend/public/trailers"
UID = "b6881111fcfa4e84af5ff0bcaf6c5a82"

vo_path = os.path.join(TRAILERS_DIR, f"../voiceovers/{UID}_oz.mp3")
vid_path = os.path.join(TRAILERS_DIR, f"temp_{UID}.mp4")
final_path = os.path.join(TRAILERS_DIR, f"trailer_{UID}.mp4")
bgm_path = os.path.join(TRAILERS_DIR, "real_prison_break.mp3")
concat_txt = os.path.join(TRAILERS_DIR, f"veo_scenes_{UID}", "concat.txt")

print("Mixing Real Prison Break Soundtrack...")
subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_txt, "-c:v", "libx264", "-crf", "23", "-preset", "fast", vid_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# We are omitting the fast-forward/seek so we get the iconic buildup, and adding stream_loop to ensure it covers 75 seconds!
subprocess.run([
    "ffmpeg", "-y", "-i", vid_path, "-i", vo_path, "-stream_loop", "-1", "-i", bgm_path,
    "-filter_complex", "[2:a]volume=1.3[bg];[1:a]volume=2.5[vo];[vo][bg]amix=inputs=2:duration=longest:dropout_transition=2[a_out]",
    "-map", "0:v", "-map", "[a_out]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", final_path
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if os.path.exists(vid_path):
    os.remove(vid_path)

print("COMPLETED CAGE BREAK (PRISON BREAK EDITION)!")
