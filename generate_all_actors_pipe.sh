#!/bin/bash
# Automation Pipe to finalize all cast images as literal hamsters

echo "Starting Hamster Cast Image Generation Pipe..."
cd /Users/ckaplan/dev/neuralon/hamster

# Run the fast, highly specific prompt generation script
python3 generate_actors_fast.py

# Fill any missing images (due to API rate limits) with randomly selected successfully generated hamsters
cat << 'PYEOF' > fill_missing.py
import os, json, sqlite3, random, shutil
db_path = "/Users/ckaplan/dev/neuralon/hamster/hamsterflix.db"
actors_dir = "/Users/ckaplan/dev/neuralon/hamster/frontend/public/actors"
conn = sqlite3.connect(db_path)
c = conn.cursor()
all_movies = c.execute("SELECT uid, \"cast\" FROM movies").fetchall() + c.execute("SELECT uid, \"cast\" FROM real_movies").fetchall()
existing = [os.path.join(actors_dir, f) for f in os.listdir(actors_dir) if f.endswith('.png')]
if existing:
    for m in all_movies:
        if m[1]:
            try:
                for cm in json.loads(m[1]):
                    p = os.path.join(actors_dir, os.path.basename(cm['img']))
                    if not os.path.exists(p): shutil.copy(random.choice(existing), p)
            except: pass
PYEOF
python3 fill_missing.py && rm fill_missing.py

# Sync to R2 CDN
echo "Syncing newly generated cast images to Cloudflare R2..."
ACCOUNT_ID="90170865e52d8ddca0d0aa864fabae66"
BUCKET="hamsterflix-media"
aws s3 sync frontend/public/actors s3://$BUCKET/actors --endpoint-url https://$ACCOUNT_ID.r2.cloudflarestorage.com --profile r2

echo "Hamster Cast Pipeline Complete!"
