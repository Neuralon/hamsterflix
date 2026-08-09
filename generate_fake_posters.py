import os
import re
import urllib.request
import urllib.parse
import time

app_path = "/Users/ckaplan/dev/neuralon/hamster/frontend/src/App.jsx"
output_dir = "/Users/ckaplan/dev/neuralon/hamster/frontend/public/posters_ai"
os.makedirs(output_dir, exist_ok=True)

with open(app_path, "r") as f:
    content = f.read()

movies = []
for match in re.finditer(r'\{\s*id:\s*(\d+),\s*title:\s*"([^"]+)",\s*img:\s*"/posters/poster_(\d+)\.png"\s*\}', content):
    movies.append({'id': int(match.group(1)), 'title': match.group(2)})

# deduplicate
unique_movies = list({m['id']: m for m in movies}.values())
unique_movies.sort(key=lambda x: x['id'])

print(f"Generating posters for {len(unique_movies)} titles...")

for m in unique_movies:
    mid = m['id']
    title = m['title']
    output_path = os.path.join(output_dir, f"poster_{mid}.png")
    
    if os.path.exists(output_path):
        print(f"Skipping {title}, already exists.")
        continue
        
    print(f"Generating poster for: {title}")
    prompt = f"A highly detailed, cinematic movie poster for a hamster movie titled '{title}'. Beautiful typography, Pixar style, 4k resolution, highly detailed."
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=800&height=1200&nologo=true"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(output_path, 'wb') as out_file:
            out_file.write(response.read())
    except Exception as e:
        print(f"Failed to generate {title}: {e}")
    
    time.sleep(1) # Be polite

print("Finished generating AI posters for fake titles.")
