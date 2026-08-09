#!/bin/bash
cd /Users/ckaplan/dev/neuralon/hamster/frontend/public/trailers

# We want 3 seconds per frame (12 frames = 36 seconds total)
ffmpeg -y -framerate 1/3 -i trailer_2_frame_%02d.png -c:v libx264 -r 24 -pix_fmt yuv420p trailer_2.mp4
echo "Video compiled!"
