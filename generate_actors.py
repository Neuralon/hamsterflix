import os
import json
import sqlite3
import urllib.request
import urllib.parse
import time

db_path = "/Users/ckaplan/dev/neuralon/hamster/hamsterflix.db"
actors_dir = "/Users/ckaplan/dev/neuralon/hamster/frontend/public/actors"
os.makedirs(actors_dir, exist_ok=True)

conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute("SELECT uid, \"cast\", title FROM movies")
fake_movies = c.fetchall()

c.execute("SELECT uid, \"cast\", title FROM real_movies")
real_movies = c.fetchall()
conn.close()

all_movies = fake_movies + real_movies

# Flatten into a list of tasks
tasks = []
for m in all_movies:
    uid, cast_json, title = m
    if cast_json:
        try:
            cast = json.loads(cast_json)
            for c_member in cast:
                tasks.append({
                    "uid": uid,
                    "title": title,
                    "real_actor": c_member.get('real_actor', 'Actor'),
                    "character": c_member.get('character', 'Character'),
                    "img_path": os.path.join("/Users/ckaplan/dev/neuralon/hamster/frontend/public", c_member['img'].lstrip('/'))
                })
        except:
            pass

print(f"Total actor images to generate: {len(tasks)}")

for i, task in enumerate(tasks):
    out_path = task['img_path']
    if os.path.exists(out_path):
        continue
        
    real_actor = task['real_actor']
    character = task['character']
    title = task['title']
    
    print(f"[{i+1}/{len(tasks)}] Generating photo for {real_actor} as {character} in {title}")
    
    prompt = f"A photorealistic, highly detailed headshot of a REAL HAMSTER. The animal is 100% a furry rodent hamster, not a human. The hamster is playfully dressed in a tiny, cinematic {character} costume from the movie {title}, and its facial features faintly resemble the actor {real_actor}. It MUST have a hamster snout, hamster whiskers, and hamster paws. ABSOLUTELY NO human faces, NO human skin, NO people wearing ears. Must be a literal animal. 8k resolution, cinematic studio lighting, extreme realism."
    
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=400&height=400&nologo=true&model=flux"
    
    # Use a rotating list of standard web browsers to bypass simple blocks
    import random
    user_agents = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/121.0'
    ]
    
    success = False
    for attempt in range(10):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': random.choice(user_agents)})
            with urllib.request.urlopen(req, timeout=30) as response:
                img_data = response.read()
                # Ensure we actually got an image back, not an HTML error page or short text
                if len(img_data) < 1000:
                    raise Exception("Downloaded file is too small to be a valid image")
                with open(out_path, 'wb') as out_file:
                    out_file.write(img_data)
            success = True
            break
        except Exception as e:
            wait_time = (attempt + 1) * 5
            print(f"  -> Attempt {attempt+1} Failed: {e}. Waiting {wait_time}s...")
            time.sleep(wait_time)
            
    if not success:
        print(f"Failed to generate {real_actor} after 10 attempts.")
    else:
        print(f"  -> Successfully generated {real_actor}!")
        
    time.sleep(3) # Global cooldown to avoid 429
