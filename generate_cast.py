import os
import json
import sqlite3
import time
from google import genai

key = os.getenv('GEMINI_API_KEY')
client = genai.Client(api_key=key, http_options={'api_version':'v1alpha'})

db_path = "/Users/ckaplan/dev/neuralon/hamster/hamsterflix.db"
conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute("SELECT id, uid, title FROM movies")
fake_movies = c.fetchall()

c.execute("SELECT id, uid, title FROM real_movies")
real_movies = c.fetchall()

# Load scripts to get inspirations
scripts_path = "/Users/ckaplan/dev/neuralon/hamster/frontend/public/trailer_scripts.json"
with open(scripts_path, 'r') as f:
    scripts = json.load(f)

uid_to_inspiration = {s['uid']: s.get('inspiration', 'a famous Hollywood movie') for s in scripts}

all_movies = []
for m in fake_movies:
    all_movies.append({"table": "movies", "id": m[0], "uid": m[1], "title": m[2], "inspiration": uid_to_inspiration.get(m[1], "Hollywood blockbuster")})
for m in real_movies:
    all_movies.append({"table": "real_movies", "id": m[0], "uid": m[1], "title": m[2], "inspiration": uid_to_inspiration.get(m[1], "Hollywood blockbuster")})

print(f"Generating 20-person cast lists for {len(all_movies)} movies...")

batch_size = 5
for i in range(0, len(all_movies), batch_size):
    batch = all_movies[i:i+batch_size]
    print(f"Processing batch {i//batch_size + 1}/{(len(all_movies)+batch_size-1)//batch_size}...")
    
    prompt = f"""You are a brilliant comedy writer. For EACH of the {len(batch)} movies below, I need a list of exactly 20 cast members.
The movies are parodies of real Hollywood blockbusters.
For EACH cast member, provide:
1. "actor_name": A funny, hamster-pun version of the REAL actor's name who starred in the original movie (e.g., "Leonardo DiCapybara", "Tom Squeaks", "Brad Pit-bull", "Hamson Ford", "Meryl Squeep").
2. "character_name": A hamster-themed version of the actual character name from the original movie (e.g., "Luke Squeakwalker", "Indiana Bones", "James Blond").
3. "real_actor": The actual real-world actor name (e.g. "Leonardo DiCaprio"), so we can use it to generate the image later.

Here are the movies:
{json.dumps([{'uid': m['uid'], 'title': m['title'], 'inspiration': m['inspiration']} for m in batch], indent=2)}

Return ONLY a JSON array of objects, one for each movie, matching exactly this schema:
[
  {{
    "uid": "movie_uid_here",
    "cast": [
      {{"actor_name": "...", "character_name": "...", "real_actor": "..."}},
      ... exactly 20 cast members total
    ]
  }}
]
"""
    for attempt in range(3):
        try:
            resp = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            raw = resp.text.replace('```json', '').replace('```', '').strip()
            parsed = json.loads(raw)
            
            for item in parsed:
                uid = item['uid']
                cast = item['cast']
                # find which table to update
                movie_info = next(m for m in all_movies if m['uid'] == uid)
                
                # Format for the frontend (which expects 'name', 'character', 'img')
                # We will point the image to a path that a background worker will download later
                formatted_cast = []
                for idx, c_member in enumerate(cast):
                    safe_actor = c_member['real_actor'].replace(' ', '_').lower()
                    img_path = f"/actors/{uid}_{idx}_{safe_actor}.png"
                    formatted_cast.append({
                        "name": c_member['actor_name'],
                        "character": c_member['character_name'],
                        "img": img_path,
                        "real_actor": c_member['real_actor']
                    })
                
                c.execute(f"UPDATE {movie_info['table']} SET \"cast\" = ? WHERE uid = ?", (json.dumps(formatted_cast), uid))
            conn.commit()
            break
        except Exception as e:
            print(f"Error on batch: {e}")
            time.sleep(5)
    time.sleep(2)

conn.close()
print("All cast data populated in DB!")
