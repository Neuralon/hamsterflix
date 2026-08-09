import os
import subprocess

TRAILERS_DIR = "/Users/ckaplan/dev/neuralon/hamster/frontend/public/trailers"
uid_gump = "4414013171c34f51b576ba9f98590880"
vo_gump = os.path.join(TRAILERS_DIR, f"../voiceovers/{uid_gump}_gump.mp3")
vid_gump = os.path.join(TRAILERS_DIR, f"temp_{uid_gump}.mp4")
final_gump = os.path.join(TRAILERS_DIR, f"trailer_{uid_gump}.mp4")
bgm_gump = os.path.join(TRAILERS_DIR, "gump.mp3")

print("Mixing Real Forrest Gump Soundtrack...")
concat_txt_gump = os.path.join(TRAILERS_DIR, f"veo_scenes_{uid_gump}", "concat.txt")
subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_txt_gump, "-c:v", "libx264", "-crf", "23", "-preset", "fast", vid_gump], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

subprocess.run([
    "ffmpeg", "-y", "-i", vid_gump, "-i", vo_gump, "-ss", "00:00:00", "-i", bgm_gump,
    "-filter_complex", "[2:a]volume=1.5[bg];[1:a]volume=2.5[vo];[vo][bg]amix=inputs=2:duration=longest:dropout_transition=2[a_out]",
    "-map", "0:v", "-map", "[a_out]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", final_gump
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if os.path.exists(vid_gump): os.remove(vid_gump)
print("COMPLETED GUMP!")
