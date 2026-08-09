#!/bin/bash
# Upload all videos to Cloudflare R2 using AWS CLI (Recommended)
# Before running, set up AWS CLI with R2 credentials:
# aws configure --profile r2
# (Get Access Key and Secret Key from Cloudflare Dashboard -> R2 -> Manage R2 API Tokens)

ACCOUNT_ID="90170865e52d8ddca0d0aa864fabae66"
BUCKET="hamsterflix-media"

echo "Syncing trailers to R2..."
aws s3 sync frontend/public/trailers s3://$BUCKET/trailers --endpoint-url https://$ACCOUNT_ID.r2.cloudflarestorage.com --profile r2

echo "Syncing voiceovers to R2..."
aws s3 sync frontend/public/voiceovers s3://$BUCKET/voiceovers --endpoint-url https://$ACCOUNT_ID.r2.cloudflarestorage.com --profile r2

echo "Syncing posters to R2..."
aws s3 sync frontend/public/posters s3://$BUCKET/posters --endpoint-url https://$ACCOUNT_ID.r2.cloudflarestorage.com --profile r2
aws s3 sync frontend/public/posters_real s3://$BUCKET/posters_real --endpoint-url https://$ACCOUNT_ID.r2.cloudflarestorage.com --profile r2
aws s3 sync frontend/public/posters_ai s3://$BUCKET/posters_ai --endpoint-url https://$ACCOUNT_ID.r2.cloudflarestorage.com --profile r2

echo "Upload Complete!"
