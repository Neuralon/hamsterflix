import os
import subprocess

TRAILERS_DIR = "/Users/ckaplan/dev/neuralon/hamster/frontend/public/trailers"

uid_indy = "c99b8b0489f84fbea28b69b1f9194b85"
vo_indy = os.path.join(TRAILERS_DIR, f"../voiceovers/{uid_indy}_indy.mp3")
vid_indy = os.path.join(TRAILERS_DIR, f"temp_{uid_indy}.mp4")
final_indy = os.path.join(TRAILERS_DIR, f"trailer_{uid_indy}.mp4")

uid_oz = "b6881111fcfa4e84af5ff0bcaf6c5a82"
vo_oz = os.path.join(TRAILERS_DIR, f"../voiceovers/{uid_oz}_oz.mp3")
vid_oz = os.path.join(TRAILERS_DIR, f"temp_{uid_oz}.mp4")
final_oz = os.path.join(TRAILERS_DIR, f"trailer_{uid_oz}.mp4")

bgm_indy = os.path.join(TRAILERS_DIR, "real_indy.mp3")
bgm_oz = os.path.join(TRAILERS_DIR, "real_oz.mp3")

# Mix Indy
print("Mixing Real Indiana Jones Soundtrack...")
concat_txt_indy = os.path.join(TRAILERS_DIR, f"veo_scenes_{uid_indy}", "concat.txt")
subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_txt_indy, "-c:v", "libx264", "-crf", "23", "-preset", "fast", vid_indy], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run([
    "ffmpeg", "-y", "-i", vid_indy, "-i", vo_indy, "-ss", "00:00:15", "-i", bgm_indy,
    "-filter_complex", "[2:a]volume=1.8[bg];[1:a]volume=2.2[vo];[vo][bg]amix=inputs=2:duration=longest:dropout_transition=2[a_out]",
    "-map", "0:v", "-map", "[a_out]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", final_indy
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Mix Oz
print("Mixing Real HBO Oz Soundtrack...")
concat_txt_oz = os.path.join(TRAILERS_DIR, f"veo_scenes_{uid_oz}", "concat.txt")
subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_txt_oz, "-c:v", "libx264", "-crf", "23", "-preset", "fast", vid_oz], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run([
    "ffmpeg", "-y", "-i", vid_oz, "-i", vo_oz, "-ss", "00:00:10", "-i", bgm_oz,
    "-filter_complex", "[2:a]volume=1.5[bg];[1:a]volume=2.2[vo];[vo][bg]amix=inputs=2:duration=longest:dropout_transition=2[a_out]",
    "-map", "0:v", "-map", "[a_out]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", final_oz
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if os.path.exists(vid_indy): os.remove(vid_indy)
if os.path.exists(vid_oz): os.remove(vid_oz)
print("COMPLETED!")
