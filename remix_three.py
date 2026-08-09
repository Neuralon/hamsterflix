import os
import json
import subprocess
import asyncio
import edge_tts
from google import genai

BASE_DIR = "/Users/ckaplan/dev/neuralon/hamster/frontend/public"
TRAILERS_DIR = os.path.join(BASE_DIR, "trailers")
VOICEOVERS_DIR = os.path.join(BASE_DIR, "voiceovers")

gemini_key = os.getenv('GEMINI_API_KEY')
client = genai.Client(api_key=gemini_key, http_options={'api_version':'v1alpha'})

async def extract_and_analyze(uid, prompt_text):
    veo_dir = os.path.join(TRAILERS_DIR, f"veo_scenes_{uid}")
    frames_dir = os.path.join(veo_dir, "frames")
    os.makedirs(frames_dir, exist_ok=True)
    
    for i in range(15):
        vid = os.path.join(veo_dir, f"scene_{i:02d}.mp4")
        frame = os.path.join(frames_dir, f"frame_{i:02d}.jpg")
        if not os.path.exists(frame) and os.path.exists(vid):
            subprocess.run(["ffmpeg", "-y", "-i", vid, "-ss", "00:00:02", "-vframes", "1", frame], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    uploaded_files = []
    for i in range(15):
        frame = os.path.join(frames_dir, f"frame_{i:02d}.jpg")
        if os.path.exists(frame):
            uploaded_files.append(client.files.upload(file=frame))
            
    print(f"Analyzing footage for {uid}...")
    resp = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[*uploaded_files, prompt_text]
    )
    raw = resp.text.replace('```json', '').replace('```', '').strip()
    return json.loads(raw)

async def gen_vo(text, path, voice="en-US-ChristopherNeural", rate="+0%"):
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(path)

async def mix_trailer(uid, vo_path, bgm_path):
    final_trailer = os.path.join(TRAILERS_DIR, f"trailer_{uid}.mp4")
    clean_vid = os.path.join(TRAILERS_DIR, f"temp_{uid}.mp4")
    concat_vid_txt = os.path.join(TRAILERS_DIR, f"veo_scenes_{uid}", "concat.txt")
    
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_vid_txt, "-c:v", "libx264", "-crf", "23", "-preset", "fast", clean_vid], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    cmd_mix = [
        "ffmpeg", "-y", "-i", clean_vid, "-i", vo_path, "-stream_loop", "-1", "-i", bgm_path,
        "-filter_complex", "[2:a]volume=1.8[bg];[1:a]volume=2.2[vo];[vo][bg]amix=inputs=2:duration=longest:dropout_transition=2[a_out]",
        "-map", "0:v", "-map", "[a_out]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", final_trailer
    ]
    subprocess.run(cmd_mix, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(clean_vid)

async def main():
    # 1. Cheek Pouches (c99b8b0489f84fbea28b69b1f9194b85) - Indiana Jones
    print("Starting Cheek Pouches (Indiana Jones)...")
    uid_indy = "c99b8b0489f84fbea28b69b1f9194b85"
    prompt_indy = """These are 15 sequential frames from an AI-generated movie trailer for 'Cheek Pouches' (Indiana Jones parody).
Write an adventurous voiceover script matching the visuals exactly.
REQUIREMENTS: Output ONLY a JSON array: [{"text": "sentence 1"}, {"text": "sentence 2"}]. Write exactly 8 heroic, adventurous sentences."""
    indy_script = await extract_and_analyze(uid_indy, prompt_indy)
    vo_indy = os.path.join(VOICEOVERS_DIR, f"{uid_indy}_indy.mp3")
    await gen_vo(" ".join([x['text'] for x in indy_script]), vo_indy, "en-US-ChristopherNeural")
    
    bgm_indy = os.path.join(TRAILERS_DIR, f"bgm_{uid_indy}_custom.mp3")
    subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "aevalsrc='0.8*sin(2*PI*440*t)*exp(-2*(t-floor(t)))+0.5*sin(2*PI*660*t)*exp(-2*(t-floor(t)))':duration=75,flanger,tremolo=f=4:d=0.5", "-c:a", "libmp3lame", "-q:a", "2", bgm_indy], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    await mix_trailer(uid_indy, vo_indy, bgm_indy)

    # 2. Cage Break (b6881111fcfa4e84af5ff0bcaf6c5a82) - Oz
    print("Starting Cage Break (Oz)...")
    uid_oz = "b6881111fcfa4e84af5ff0bcaf6c5a82"
    with open(os.path.join(BASE_DIR, "trailer_scripts.json"), "r") as f:
        scripts = json.load(f)
    script_oz = next(s['script_content'] for s in scripts if s['uid'] == uid_oz)
    import re
    text_oz = re.sub(r'^[A-Z0-9 \-]+(?:\s*\([^)]+\))?:\s*', '', script_oz, flags=re.MULTILINE).replace('[', '').replace(']', '')
    
    vo_oz = os.path.join(VOICEOVERS_DIR, f"{uid_oz}_oz.mp3")
    await gen_vo(text_oz, vo_oz, "en-US-BrianNeural", rate="-5%") # Brian is very deep/real sounding
    
    bgm_oz = os.path.join(TRAILERS_DIR, f"bgm_{uid_oz}_custom.mp3")
    subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "aevalsrc='random(0)*0.5*exp(-10*(t-floor(t))) + 0.3*sin(2*PI*50*t)':duration=75,tremolo=f=1:d=0.9", "-c:a", "libmp3lame", "-q:a", "2", bgm_oz], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    await mix_trailer(uid_oz, vo_oz, bgm_oz)

    # 3. Fuzz Ball (4414013171c34f51b576ba9f98590880) - Forrest Gump
    print("Starting Fuzz Ball (Forrest Gump)...")
    uid_gump = "4414013171c34f51b576ba9f98590880"
    prompt_gump = """These are 15 sequential frames from an AI-generated movie trailer for 'Fuzz Ball' (Forrest Gump parody).
Write a heartwarming narration from the perspective of a simple, sweet hamster matching these visuals. Start with "My mama always said..."
REQUIREMENTS: Output ONLY a JSON array: [{"text": "sentence 1"}, {"text": "sentence 2"}]. Write exactly 8 sweet sentences."""
    gump_script = await extract_and_analyze(uid_gump, prompt_gump)
    vo_gump = os.path.join(VOICEOVERS_DIR, f"{uid_gump}_gump.mp3")
    await gen_vo(" ".join([x['text'] for x in gump_script]), vo_gump, "en-US-GuyNeural", rate="-10%") # Slower, innocent
    
    bgm_gump = os.path.join(TRAILERS_DIR, f"bgm_{uid_gump}_custom.mp3")
    subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "aevalsrc='0.4*sin(2*PI*440*t)*exp(-0.5*(t-floor(t/4)*4)) + 0.2*sin(2*PI*554*t)':duration=75,vibrato=f=4:d=0.2", "-c:a", "libmp3lame", "-q:a", "2", bgm_gump], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    await mix_trailer(uid_gump, vo_gump, bgm_gump)

if __name__ == "__main__":
    asyncio.run(main())
