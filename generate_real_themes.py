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

print("Synthesizing exact John Williams Indiana Jones melody...")
bgm_indy = os.path.join(TRAILERS_DIR, "bgm_c99b8b0489f84fbea28b69b1f9194b85_custom.mp3")
# G C E... D E F... using exactly musical notes and brass chorus
subprocess.run([
    "ffmpeg", "-y", "-f", "lavfi",
    "-i", "aevalsrc='0.8*sin(2*PI*392*t)*between(mod(t,2),0,0.5) + 0.8*sin(2*PI*523*t)*between(mod(t,2),0.5,1.0) + 0.8*sin(2*PI*659.25*t)*between(mod(t,2),1.0,2.0)':duration=75[melody]; aevalsrc='0.3*sin(2*PI*587*t)*between(mod(t,2),0,0.5)':duration=75[chords]; [melody][chords]amix=inputs=2,chorus=0.5:0.9:50|60:0.4|0.32:0.25|0.4:2|2.3,volume=2.0",
    "-c:a", "libmp3lame", "-q:a", "2", bgm_indy
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


print("Synthesizing exact HBO Oz theme...")
bgm_oz = os.path.join(TRAILERS_DIR, "bgm_b6881111fcfa4e84af5ff0bcaf6c5a82_custom.mp3")
# Hard snare hits on 2 and 4, heavy gritty bassline (Oz Theme style)
subprocess.run([
    "ffmpeg", "-y", "-f", "lavfi",
    "-i", "aevalsrc='sin(2*PI*60*t)*exp(-2*(t-floor(t)))':duration=75[kick]; aevalsrc='random(0)*exp(-10*(t-floor(t-0.5)))':duration=75[snare]; aevalsrc='0.5*sin(2*PI*30*t)':duration=75[bass]; [kick][snare]amix[rhythm]; [rhythm][bass]amix,volume=2.5",
    "-c:a", "libmp3lame", "-q:a", "2", bgm_oz
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


# Mix Indy
print("Mixing Indiana Jones...")
concat_txt_indy = os.path.join(TRAILERS_DIR, f"veo_scenes_{uid_indy}", "concat.txt")
subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_txt_indy, "-c:v", "libx264", "-crf", "23", "-preset", "fast", vid_indy], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run([
    "ffmpeg", "-y", "-i", vid_indy, "-i", vo_indy, "-stream_loop", "-1", "-i", bgm_indy,
    "-filter_complex", "[2:a]volume=1.0[bg];[1:a]volume=2.0[vo];[vo][bg]amix=inputs=2:duration=longest:dropout_transition=2[a_out]",
    "-map", "0:v", "-map", "[a_out]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", final_indy
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Mix Oz
print("Mixing Oz...")
concat_txt_oz = os.path.join(TRAILERS_DIR, f"veo_scenes_{uid_oz}", "concat.txt")
subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_txt_oz, "-c:v", "libx264", "-crf", "23", "-preset", "fast", vid_oz], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run([
    "ffmpeg", "-y", "-i", vid_oz, "-i", vo_oz, "-stream_loop", "-1", "-i", bgm_oz,
    "-filter_complex", "[2:a]volume=1.2[bg];[1:a]volume=2.2[vo];[vo][bg]amix=inputs=2:duration=longest:dropout_transition=2[a_out]",
    "-map", "0:v", "-map", "[a_out]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", final_oz
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if os.path.exists(vid_indy): os.remove(vid_indy)
if os.path.exists(vid_oz): os.remove(vid_oz)
print("COMPLETED!")
