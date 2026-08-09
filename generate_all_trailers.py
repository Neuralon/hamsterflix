import os
import sqlite3
import subprocess
import asyncio
import edge_tts

db_path = "/Users/ckaplan/dev/neuralon/hamster/hamsterflix.db"
trailers_dir = "/Users/ckaplan/dev/neuralon/hamster/frontend/public/trailers"
voiceovers_dir = "/Users/ckaplan/dev/neuralon/hamster/frontend/public/voiceovers"
posters_ai_dir = "/Users/ckaplan/dev/neuralon/hamster/frontend/public/posters_ai"
posters_real_dir = "/Users/ckaplan/dev/neuralon/hamster/frontend/public/posters_real"
epic_music = os.path.join(trailers_dir, "epic_music.mp3")

conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute("SELECT id, uid, title, synopsis FROM movies")
fake_movies = c.fetchall()

c.execute("SELECT id, uid, title, synopsis, poster_filename FROM real_movies")
real_movies = c.fetchall()
conn.close()

movies = []
for m in fake_movies:
    movies.append({
        'uid': m[1],
        'title': m[2],
        'synopsis': m[3],
        'poster': os.path.join(posters_ai_dir, f"poster_{m[0]}.png")
    })
for m in real_movies:
    movies.append({
        'uid': m[1],
        'title': m[2],
        'synopsis': m[3],
        'poster': os.path.join(posters_real_dir, m[4])
    })

print(f"Total movies to process: {len(movies)}")

async def generate_all():
    for i, m in enumerate(movies):
        uid = m['uid']
        title = m['title']
        poster_path = m['poster']
        
        mixed_trailer = os.path.join(trailers_dir, f"trailer_{uid}.mp4")
        if os.path.exists(mixed_trailer):
            print(f"[{i+1}/{len(movies)}] Skipper {title}")
            continue
            
        print(f"[{i+1}/{len(movies)}] Generating trailer for: {title}")
        
        # 1. Generate TTS
        vo_path = os.path.join(voiceovers_dir, f"{uid}.mp3")
        if not os.path.exists(vo_path):
            script = f"In a world where the wheel has stopped turning... {m['synopsis']} {title}. Coming soon."
            communicate = edge_tts.Communicate(script, "en-US-ChristopherNeural")
            await communicate.save(vo_path)

        clean_vid = os.path.join(trailers_dir, f"temp_{uid}.mp4")
        
        if os.path.exists(poster_path):
            # Create a 15-second Ken Burns zoom video from the poster
            cmd_vid = [
                "ffmpeg", "-y", "-loop", "1", "-i", poster_path,
                "-vf", "zoompan=z='min(zoom+0.0015,1.5)':d=360:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'",
                "-c:v", "libx264", "-t", "15", "-s", "1280x720", "-pix_fmt", "yuv420p", clean_vid
            ]
            subprocess.run(cmd_vid, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Mix Epic Music
            cmd_mix = [
                "ffmpeg", "-y", "-i", clean_vid, "-i", vo_path, "-i", epic_music,
                "-filter_complex", "[2:a]volume=2.10[bg];[1:a]volume=2.0[vo];[bg][vo]amix=inputs=2:duration=first:dropout_transition=2[a_out]",
                "-map", "0:v", "-map", "[a_out]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", mixed_trailer
            ]
            subprocess.run(cmd_mix, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            if os.path.exists(clean_vid):
                os.remove(clean_vid)

asyncio.run(generate_all())
print("Done generating all trailers.")
