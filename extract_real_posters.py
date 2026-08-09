import os
import glob
import sqlite3
import json
import shutil
from google import genai

key = os.getenv('GEMINI_API_KEY')
client = genai.Client(api_key=key, http_options={'api_version':'v1alpha'})

desktop_img_dir = "/Users/ckaplan/Desktop/images"
real_posters_dir = "/Users/ckaplan/dev/neuralon/hamster/frontend/public/posters_real"
os.makedirs(real_posters_dir, exist_ok=True)

db_path = "/Users/ckaplan/dev/neuralon/hamster/hamsterflix.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create a table for real movies
cursor.execute('''
CREATE TABLE IF NOT EXISTS real_movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    director TEXT,
    synopsis TEXT,
    genres TEXT,
    mood TEXT,
    poster_filename TEXT
)
''')
conn.commit()

# Check if we already populated this to avoid duplicates
cursor.execute("SELECT COUNT(*) FROM real_movies")
if cursor.fetchone()[0] > 0:
    print("Real movies table already populated. Dropping and recreating to ensure fresh extraction...")
    cursor.execute("DROP TABLE real_movies")
    cursor.execute('''
    CREATE TABLE real_movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        director TEXT,
        synopsis TEXT,
        genres TEXT,
        mood TEXT,
        poster_filename TEXT
    )
    ''')
    conn.commit()

images = glob.glob(os.path.join(desktop_img_dir, "*.png"))
print(f"Found {len(images)} images on Desktop.")

prompt = """
You are a movie metadata extractor. Look at this movie poster and extract the title written on it.
If you cannot read the title or there is none, invent a fitting hamster movie title based on the imagery.
Also, invent the following matching metadata for this movie:
- A one sentence synopsis
- A director name
- A list of 2 genres (e.g. Action, Comedy)
- A list of 2 moods (e.g. Heartwarming, Exciting)

Respond ONLY with a valid JSON object matching this schema:
{
    "title": "Movie Title",
    "synopsis": "...",
    "director": "...",
    "genres": ["...", "..."],
    "mood": ["...", "..."]
}
"""

for i, img_path in enumerate(images):
    print(f"Processing {i+1}/{len(images)}: {os.path.basename(img_path)}")
    try:
        from google.genai import types
        with open(img_path, 'rb') as f:
            img_bytes = f.read()
            
        resp = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                prompt, 
                types.Part.from_bytes(data=img_bytes, mime_type='image/png')
            ]
        )
        
        raw_json = resp.text.replace('```json', '').replace('```', '').strip()
        data = json.loads(raw_json)
        
        # Insert into DB
        cursor.execute('''
        INSERT INTO real_movies (title, director, synopsis, genres, mood, poster_filename)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            data['title'],
            data['director'],
            data['synopsis'],
            json.dumps(data['genres']),
            json.dumps(data['mood']),
            "" # placeholder, will update with ID
        ))
        
        new_id = cursor.lastrowid
        new_filename = f"poster_real_{new_id}.png"
        
        cursor.execute("UPDATE real_movies SET poster_filename = ? WHERE id = ?", (new_filename, new_id))
        conn.commit()
        
        # Copy file
        shutil.copy(img_path, os.path.join(real_posters_dir, new_filename))
        print(f"  -> Extracted Title: {data['title']} (Saved as {new_filename})")
        
    except Exception as e:
        print(f"  -> Failed: {e}")

conn.close()
print("Finished extracting real poster data.")
