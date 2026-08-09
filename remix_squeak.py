import os
import json
import subprocess
import asyncio
import edge_tts

UID = "ebe01c71e1fe46aaaca62c39ae336d2a"
BASE_DIR = "/Users/ckaplan/dev/neuralon/hamster/frontend/public"
TRAILERS_DIR = os.path.join(BASE_DIR, "trailers")
VEO_DIR = os.path.join(TRAILERS_DIR, f"veo_scenes_{UID}")
VOICEOVERS_DIR = os.path.join(BASE_DIR, "voiceovers")

FINAL_TRAILER = os.path.join(TRAILERS_DIR, f"trailer_{UID}.mp4")

# Recreate the voiceover explicitly using fluid dialogue
# We will NOT use the concatenation with 1.5s silence gap, because that breaks the flow of the sentences!
# Instead, we will generate the voices and concat them closely so the conversation feels connected and real.

print("Generating fluid, connected multi-character dialogue for Squeak...")
dialogue = [
  {"voice": "en-GB-RyanNeural", "text": "You think you're different, little one? We all run the wheel. We all gather seeds. That's the way it is."},
  {"voice": "en-US-JennyNeural", "text": "But... what if there's another way? To... to talk to them?"},
  {"voice": "en-US-AriaNeural", "text": "What are you doing, little fuzzball? Trying to herd that broccoli?"},
  {"voice": "en-US-JennyNeural", "text": "I'm trying to understand! To be useful! Like... like a friend!"},
  {"voice": "en-GB-RyanNeural", "text": "He's got a spirit, that one. A voice, even if it's just a... squeak."},
  {"voice": "en-US-AnaNeural", "text": "Look, mommy! Squeak is making them listen!"},
  {"voice": "en-US-JennyNeural", "text": "I just... told them where the tastiest greens were. It's about listening, not just running."},
  {"voice": "en-GB-SoniaNeural", "text": "This year, a tiny voice will make the biggest difference. Some stories are just too big for their cage."}
]

async def gen_audio():
    audio_files = []
    for idx, line in enumerate(dialogue):
        out_path = os.path.join(VOICEOVERS_DIR, f"{UID}_squeak_{idx}.mp3")
        communicate = edge_tts.Communicate(line['text'], line['voice'], rate="+5%")
        await communicate.save(out_path)
        audio_files.append(out_path)
    return audio_files

audio_files = asyncio.run(gen_audio())

# Concat with VERY tight gaps so the conversation flows seamlessly
concat_txt = os.path.join(VOICEOVERS_DIR, f"{UID}_voice_concat.txt")
with open(concat_txt, "w") as f:
    for af in audio_files:
        f.write(f"file '{af}'\n")
        f.write(f"file '/tmp/short_silence.mp3'\n")

# Create a 0.4s short silence file for natural conversational pauses
subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-t", "0.4", "-q:a", "9", "-acodec", "libmp3lame", "/tmp/short_silence.mp3"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

mixed_vo = os.path.join(VOICEOVERS_DIR, f"{UID}_final_vo.mp3")
subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_txt, "-c", "copy", mixed_vo], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("Synthesizing whimsical, bouncy, playful 'Babe' style music...")
custom_music = os.path.join(TRAILERS_DIR, f"bgm_{UID}_custom.mp3")
music_cmd = [
    "ffmpeg", "-y", "-f", "lavfi",
    # Playful bouncy bells/flute tone
    "-i", "aevalsrc='0.8*sin(2*PI*600*t)*exp(-4*(t-floor(t*2)/2))':duration=75[bop]; aevalsrc='0.3*sin(2*PI*880*t)*exp(-4*(t-floor(t*2)/2))':duration=75[ping]; [bop][ping]amix=inputs=2,vibrato=f=3:d=0.2,tremolo=f=4:d=0.5,volume=1.5",
    "-c:a", "libmp3lame", "-q:a", "2", custom_music
]
subprocess.run(music_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("Mixing final trailer with new music and connected dialogue...")
clean_vid = os.path.join(TRAILERS_DIR, f"temp_{UID}.mp4")
concat_vid_txt = os.path.join(VEO_DIR, "concat.txt")
subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_vid_txt, "-c:v", "libx264", "-crf", "23", "-preset", "fast", clean_vid], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

cmd_mix = [
    "ffmpeg", "-y", "-i", clean_vid, "-i", mixed_vo, "-stream_loop", "-1", "-i", custom_music,
    "-filter_complex", "[2:a]volume=1.20[bg];[1:a]volume=2.5[vo];[vo][bg]amix=inputs=2:duration=longest:dropout_transition=2[a_out]",
    "-map", "0:v", "-map", "[a_out]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", FINAL_TRAILER
]
subprocess.run(cmd_mix, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

os.remove(clean_vid)
print("COMPLETED SQUEAK!")
