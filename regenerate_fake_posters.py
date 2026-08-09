import os
import sqlite3
import json
import urllib.request
import urllib.parse
import time

BASE_DIR = "/Users/ckaplan/dev/neuralon/hamster/frontend/public"
POSTERS_AI_DIR = os.path.join(BASE_DIR, "posters_ai")
SCRIPTS_FILE = os.path.join(BASE_DIR, "trailer_scripts.json")
DB_PATH = "/Users/ckaplan/dev/neuralon/hamster/hamsterflix.db"

with open(SCRIPTS_FILE, 'r') as f:
    scripts = json.load(f)

uid_to_inspiration = {s['uid']: s.get('inspiration', 'a famous Hollywood movie') for s in scripts}

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute("SELECT id, uid, title FROM movies")
fake_movies = c.fetchall()
conn.close()

print(f"Regenerating {len(fake_movies)} fake posters...")

for m_id, uid, title in fake_movies:
    inspiration = uid_to_inspiration.get(uid, 'a famous Hollywood blockbuster')
    print(f"\nGenerating realistic poster for: {title} (Parody of: {inspiration})")
    
    # Aggressively force photorealism and explicitly ban 3D/Pixar styles
    prompt = f"Official live-action movie poster for '{title}'. A dark, gritty, ultra-realistic Hollywood blockbuster parody of '{inspiration}'. Featuring a REAL, photorealistic live-action hamster actor. Shot on 35mm film, dramatic cinematic lighting, extreme photographic realism, highly detailed fur and textures. Epic movie poster typography with the title '{title}'. ABSOLUTELY NO 3D rendering, NO Pixar, NO cartoon, NO animation, NO CGI look. Pure gritty cinematic photography."
    
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=800&height=1200&nologo=true&model=flux"
    
    output_path = os.path.join(POSTERS_AI_DIR, f"poster_{m_id}.png")
    
    # We need an aggressive retry loop with exponential backoff to fight the 429s
    success = False
    for attempt in range(5):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'})
            with urllib.request.urlopen(req) as response, open(output_path, 'wb') as out_file:
                out_file.write(response.read())
            print(f"  -> Success: {title}")
            success = True
            break
        except Exception as e:
            wait_time = (attempt + 1) * 30
            print(f"  -> Attempt {attempt+1} Failed: {e}. Waiting {wait_time}s...")
            time.sleep(wait_time)
            
    if not success:
        print(f"Completely failed to generate {title} after 5 attempts.")
    
    # 30 second global cooldown
    time.sleep(30)

print("Finished regenerating all AI posters!")