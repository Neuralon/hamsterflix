#!/bin/bash
# Automation Pipe to finalize all cast images as literal hamsters

echo "Starting Hamster Cast Image Generation Pipe..."
cd /Users/ckaplan/dev/neuralon/hamster

# Run the fast, highly specific prompt generation script
python3 generate_actors_fast.py

# Sync to R2 CDN
echo "Syncing newly generated cast images to Cloudflare R2..."
ACCOUNT_ID="90170865e52d8ddca0d0aa864fabae66"
BUCKET="hamsterflix-media"
aws s3 sync frontend/public/actors s3://$BUCKET/actors --endpoint-url https://$ACCOUNT_ID.r2.cloudflarestorage.com --profile r2

echo "Hamster Cast Pipeline Complete!"
