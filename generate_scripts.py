import sqlite3
import json
import os
import time
from google import genai
from pydantic import BaseModel, Field

key = os.getenv('GEMINI_API_KEY')
client = genai.Client(api_key=key, http_options={'api_version':'v1alpha'})

db_path = "/Users/ckaplan/dev/neuralon/hamster/hamsterflix.db"
conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute("SELECT uid, title, synopsis, genres, mood FROM movies")
fake_movies = c.fetchall()

c.execute("SELECT uid, title, synopsis, genres, mood FROM real_movies")
real_movies = c.fetchall()
conn.close()

all_movies = fake_movies + real_movies
# Convert to dict for prompt
movies_data = []
for m in all_movies:
    movies_data.append({
        "uid": m[0],
        "title": m[1],
        "synopsis": m[2],
        "genres": m[3],
        "mood": m[4]
    })

print(f"Total movies to script: {len(movies_data)}")

output_file = "/Users/ckaplan/dev/neuralon/hamster/frontend/public/trailer_scripts.json"
existing_scripts = []
if os.path.exists(output_file):
    try:
        with open(output_file, 'r') as f:
            existing_scripts = json.load(f)
    except:
        pass

existing_uids = {s['uid'] for s in existing_scripts}
movies_to_process = [m for m in movies_data if m['uid'] not in existing_uids]

print(f"Movies remaining to script: {len(movies_to_process)}")

batch_size = 10
results = existing_scripts

for i in range(0, len(movies_to_process), batch_size):
    batch = movies_to_process[i:i+batch_size]
    print(f"Processing batch {i//batch_size + 1}...")
    
    prompt = f"""You are a master movie trailer director. I will give you a list of {len(batch)} hamster movies.
For EACH movie, I want you to create a highly varied, unique trailer script.

CRITICAL INSTRUCTIONS FOR VARIETY:
- Do NOT use the same voiceover style for every movie.
- 30% of trailers should have NO VOICEOVER (just "Music & Scenes" with on-screen text).
- 30% should use Character Dialogue (e.g., two hamsters talking).
- 40% should use Voiceovers, but vary the voice (e.g., "Deep gritty male", "Energetic female", "Creepy whisper", "Documentary narrator").
- Describe the exact Music Style (e.g., "Heavy Synthwave", "Orchestral Sweep", "Quirky Jazz", "Dead Silence then Jump Scare").
- Provide exactly 15 visual scene prompts.

Here are the movies:
{json.dumps(batch, indent=2)}

Return ONLY a JSON array of objects with the exact following schema:
[
  {{
    "uid": "movie_uid_here",
    "trailer_style": "Music & Scenes | Character Dialogue | Voiceover",
    "audio_direction": "Describe the music style and voice/dialogue direction in detail.",
    "script_content": "The actual text of the dialogue, voiceover, or on-screen text.",
    "scenes": ["Scene 1", "Scene 2", ..., "Scene 15"]
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
            results.extend(parsed)
            
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2)
            break
        except Exception as e:
            print(f"Error on batch: {e}")
            time.sleep(5)
    time.sleep(2)

print("All scripts generated!")