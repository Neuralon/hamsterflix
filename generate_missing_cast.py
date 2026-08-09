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

c.execute("SELECT uid, title FROM real_movies WHERE \"cast\" IS NULL OR \"cast\" = '[]'")
missing_movies = c.fetchall()

# Load scripts to get inspirations
scripts_path = "/Users/ckaplan/dev/neuralon/hamster/frontend/public/trailer_scripts.json"
with open(scripts_path, 'r') as f:
    scripts = json.load(f)
uid_to_inspiration = {s['uid']: s.get('inspiration', 'a famous Hollywood movie') for s in scripts}

all_movies = []
for m in missing_movies:
    all_movies.append({"table": "real_movies", "uid": m[0], "title": m[1], "inspiration": uid_to_inspiration.get(m[0], "Hollywood blockbuster")})

print(f"Generating 20-person cast lists for {len(all_movies)} missing movies...")

for movie_info in all_movies:
    print(f"Processing missing movie: {movie_info['title']}...")
    
    prompt = f"""You are a brilliant comedy writer. For the movie below, I need a list of exactly 20 cast members.
The movie is a parody of a real Hollywood blockbuster.
For EACH cast member, provide:
1. "actor_name": A funny, hamster-pun version of the REAL actor's name who starred in the original movie (e.g., "Leonardo DiCapybara").
2. "character_name": A hamster-themed version of the actual character name from the original movie (e.g., "Luke Squeakwalker").
3. "real_actor": The actual real-world actor name (e.g. "Leonardo DiCaprio"), so we can use it to generate the image later.

Here is the movie:
{json.dumps([{'uid': movie_info['uid'], 'title': movie_info['title'], 'inspiration': movie_info['inspiration']}], indent=2)}

Return ONLY a JSON array of objects, one for the movie, matching exactly this schema:
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
            print(f"Success for {movie_info['title']}!")
            break
        except Exception as e:
            print(f"Error on {movie_info['title']}: {e}")
            time.sleep(5)
    time.sleep(2)

conn.close()
print("All missing cast data populated in DB!")
