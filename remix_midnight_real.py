import os
import subprocess

TRAILERS_DIR = "/Users/ckaplan/dev/neuralon/hamster/frontend/public/trailers"
UID = "c4cd6d2e32aa453c8ca055e166eef8ee"

vo_path = os.path.join(TRAILERS_DIR, f"../voiceovers/{UID}_final_midnight_vo.mp3")
vid_path = os.path.join(TRAILERS_DIR, f"temp_{UID}.mp4")
final_path = os.path.join(TRAILERS_DIR, f"trailer_{UID}.mp4")
bgm_path = os.path.join(TRAILERS_DIR, "real_midnight.mp3")
concat_txt = os.path.join(TRAILERS_DIR, f"veo_scenes_{UID}", "concat.txt")

print("Mixing REAL Midnight Express Soundtrack...")
subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_txt, "-c:v", "libx264", "-crf", "23", "-preset", "fast", vid_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Skip the slow 1-minute intro to get right into the driving synth chase theme, drop volume so it doesn't kill the VO, fade out at end.
subprocess.run([
    "ffmpeg", "-y", "-i", vid_path, "-i", vo_path, "-stream_loop", "-1", "-ss", "00:01:00", "-i", bgm_path,
    "-filter_complex", "[2:a]volume=0.55,afade=t=out:st=70:d=5[bg];[1:a]volume=3.0[vo];[vo][bg]amix=inputs=2:duration=longest:dropout_transition=2[a_out]",
    "-map", "0:v", "-map", "[a_out]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", final_path
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if os.path.exists(vid_path):
    os.remove(vid_path)

print("COMPLETED MIDNIGHT EXPRESS REAL MIX!")
