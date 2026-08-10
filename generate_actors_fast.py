import os
import json
import sqlite3
import urllib.request
import urllib.parse
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

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
                    "img_path": os.path.join(actors_dir, os.path.basename(c_member['img']))
                })
        except:
            pass

print(f"Total actor images to generate: {len(tasks)}")

user_agents = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/121.0'
]

def generate_image(task):
    out_path = task['img_path']
    
    # Skip if already downloaded
    if os.path.exists(out_path):
        return True, task['real_actor']

    character = task['character']
    title = task['title']
    
    prompt = f"A photorealistic, extreme close-up headshot of a literal CUTE FURRY HAMSTER dressed in a tiny, cinematic {character} costume from the movie {title}. The subject is 100% a hamster, a small rodent animal with furry hamster cheeks, a cute little pink snout, and prominent hamster whiskers. NO HUMAN FACES, NO HUMAN SKIN, NO PEOPLE. Just a tiny animal dressed up. Cinematic studio portrait lighting, 8k resolution, hyper-detailed animal photography."
    
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=400&height=400&nologo=true&model=flux"
    
    for attempt in range(5):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': random.choice(user_agents)})
            with urllib.request.urlopen(req, timeout=30) as response:
                img_data = response.read()
                if len(img_data) < 1000:
                    raise Exception("File too small")
                with open(out_path, 'wb') as out_file:
                    out_file.write(img_data)
            time.sleep(2) # delay to avoid 429
            return True, task['real_actor']
        except Exception as e:
            time.sleep(1 + attempt)
            
    return False, task['real_actor']

# Use thread pool to speed up generation
print("Starting generation...")
success_count = 0
with ThreadPoolExecutor(max_workers=2) as executor:
    futures = [executor.submit(generate_image, task) for task in tasks]
    for i, future in enumerate(as_completed(futures)):
        success, actor_name = future.result()
        if success:
            success_count += 1
            if (i+1) % 20 == 0:
                print(f"Progress: {i+1}/{len(tasks)} done.")
            time.sleep(1) # Add slight delay to prevent 429 rate limit
        else:
            print(f"Failed to generate for {actor_name}")

print(f"Finished! Successfully generated {success_count}/{len(tasks)} hamsters.")
