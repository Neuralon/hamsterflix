import sqlite3
import json
import os
import time
from google import genai

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
# We are completely overwriting the old scripts to ensure deep, high-quality generation
results = []

# Reduced batch size to 5 to give the LLM plenty of output tokens to be highly detailed
batch_size = 5

for i in range(0, len(movies_data), batch_size):
    batch = movies_data[i:i+batch_size]
    print(f"Processing batch {i//batch_size + 1}/{(len(movies_data)+batch_size-1)//batch_size}...")
    
    prompt = f"""You are a Master Trailer Editor, Cinematographer, and Film Historian. I am giving you a list of {len(batch)} hamster movie parodies.
For EACH movie, I want you to create a deeply immersive, highly detailed, and varied trailer script that pays direct homage to its real-world Hollywood inspiration.

CRITICAL INSTRUCTIONS FOR DEPTH & AUTHENTICITY:
1. Identify the Inspiration: Figure out what real Hollywood blockbuster this is parodying based on the title/synopsis (e.g. "Hamsternator: Judgment Day" = "Terminator 2", "The Hamster of Wall Street" = "The Wolf of Wall Street", "Hamster at the Museum" = "Night at the Museum").
2. Visual Depth & Homage: The 15 scenes MUST be highly descriptive. Include specific camera angles (e.g., Extreme Close-Up, Low Angle Dutch Tilt, Sweeping Drone Shot), lighting/color grading (e.g., Neon Cyberpunk Pinks, Gritty Desaturated Green, Warm Golden Hour), and action. You MUST recreate iconic shots from the real movie, but with hamsters (e.g., a cyborg hamster stepping on a crushed sunflower seed, a hamster recreating the Titanic bow scene).
3. Audio & Sound Design: Describe the music and foley sound effects vividly. Example: "Inception-style BRAAAMs", "80s synthwave arpeggiator", "Dead silence interrupted by heavy hamster breathing and a ticking clock."
4. Format Variety: Do not make them all the same! 
   - 30% Pure Music & Visuals (On-screen text only, driven by heavy music).
   - 30% Character Dialogue (Hamsters talking to each other, spoofing famous movie lines).
   - 40% Voiceovers (Specify the exact vocal tone: "Gritty 90s action guy", "Soft eerie whisper", "Attenborough documentary voice").

Here are the movies:
{json.dumps(batch, indent=2)}

Return ONLY a JSON array of objects with the exact following schema:
[
  {{
    "uid": "movie_uid_here",
    "inspiration": "The real Hollywood movie this parodies",
    "trailer_style": "Music & Scenes | Character Dialogue | Voiceover",
    "audio_direction": "Rich description of music, foley sound design, and vocal tone.",
    "script_content": "The actual text of the dialogue, voiceover, or on-screen text. Parody famous lines if applicable. Make it fit the mood perfectly.",
    "scenes": [
      "[Wide Shot, Cold Blue Lighting] Detailed description of the action, paying homage to the original film's opening.",
      "[Extreme Close Up] ...",
      ... exactly 15 highly detailed scenes
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
            results.extend(parsed)
            
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2)
            break
        except Exception as e:
            print(f"Error on batch (Attempt {attempt+1}): {e}")
            time.sleep(5)
    time.sleep(2)

print("All deep cinematic scripts generated!")
