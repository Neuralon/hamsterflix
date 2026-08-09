import os
import subprocess

TRAILERS_DIR = "/Users/ckaplan/dev/neuralon/hamster/frontend/public/trailers"

uid_dune = "1911e0baa13b46708b5569b2c3cf63d5"
vo_dune = os.path.join(TRAILERS_DIR, f"../voiceovers/{uid_dune}_v2.mp3")
vid_dune = os.path.join(TRAILERS_DIR, f"temp_{uid_dune}.mp4")
final_dune = os.path.join(TRAILERS_DIR, f"trailer_{uid_dune}.mp4")

uid_babe = "ebe01c71e1fe46aaaca62c39ae336d2a"
vo_babe = os.path.join(TRAILERS_DIR, f"../voiceovers/{uid_babe}_final_vo.mp3")
vid_babe = os.path.join(TRAILERS_DIR, f"temp_{uid_babe}.mp4")
final_babe = os.path.join(TRAILERS_DIR, f"trailer_{uid_babe}.mp4")

# Since direct commercial mp3 downloads (Hans Zimmer / Babe Soundtrack) are blocked by Cloudflare/AWS,
# we will synthesize massive, heavy, sweeping Hans Zimmer-style orchestral drones for Dune,
# and we will synthesize a beautiful, sweeping, warm orchestral string piece for Babe (no more weird dings).

print("Synthesizing Hans Zimmer DUNE score...")
bgm_dune = os.path.join(TRAILERS_DIR, "dune_score.mp3")
# Huge, blown-out distorted bass drone + high-pitched eerie female vocal wail (throat singing simulation)
subprocess.run([
    "ffmpeg", "-y", "-f", "lavfi",
    "-i", "aevalsrc='0.8*sin(2*PI*40*t)*exp(-0.2*t) + 0.5*sin(2*PI*45*t)*exp(-0.2*t)':duration=75[bass]; aevalsrc='0.3*sin(2*PI*880*t)*sin(2*PI*0.5*t)':duration=75[wail]; [bass][wail]amix=inputs=2,flanger=delay=20,tremolo=f=0.5:d=0.8,volume=1.8",
    "-c:a", "libmp3lame", "-q:a", "2", bgm_dune
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("Synthesizing beautiful orchestral strings for SQUEAK (Babe)...")
bgm_babe = os.path.join(TRAILERS_DIR, "babe_score.mp3")
# Warm, slow, continuous sweeping chord (like a string section) instead of plinky bells
subprocess.run([
    "ffmpeg", "-y", "-f", "lavfi",
    "-i", "aevalsrc='0.3*sin(2*PI*440*t) + 0.2*sin(2*PI*554*t) + 0.2*sin(2*PI*659*t)':duration=75,vibrato=f=4:d=0.3,chorus=0.5:0.9:50|60:0.4|0.32:0.25|0.4:2|2.3,volume=0.8",
    "-c:a", "libmp3lame", "-q:a", "2", bgm_babe
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Rebuild Dune Video
print("Mixing Dune...")
concat_txt = os.path.join(TRAILERS_DIR, f"veo_scenes_{uid_dune}", "concat.txt")
subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_txt, "-c:v", "libx264", "-crf", "23", "-preset", "fast", vid_dune], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run([
    "ffmpeg", "-y", "-i", vid_dune, "-i", vo_dune, "-stream_loop", "-1", "-i", bgm_dune,
    "-filter_complex", "[2:a]volume=1.5[bg];[1:a]volume=2.2[vo];[vo][bg]amix=inputs=2:duration=longest:dropout_transition=2[a_out]",
    "-map", "0:v", "-map", "[a_out]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", final_dune
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Rebuild Babe Video
print("Mixing Babe...")
concat_txt_babe = os.path.join(TRAILERS_DIR, f"veo_scenes_{uid_babe}", "concat.txt")
subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_txt_babe, "-c:v", "libx264", "-crf", "23", "-preset", "fast", vid_babe], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run([
    "ffmpeg", "-y", "-i", vid_babe, "-i", vo_babe, "-stream_loop", "-1", "-i", bgm_babe,
    "-filter_complex", "[2:a]volume=1.0[bg];[1:a]volume=2.5[vo];[vo][bg]amix=inputs=2:duration=longest:dropout_transition=2[a_out]",
    "-map", "0:v", "-map", "[a_out]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", final_babe
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

os.remove(vid_dune)
os.remove(vid_babe)
print("COMPLETED REMIXES!")
