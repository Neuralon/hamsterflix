#!/bin/bash
# Start the full Hamsterflix App locally
cd "$(dirname "$0")"

# Build the frontend if not built yet
if [ ! -d "dist" ]; then
  npm run build
fi

# Run the node server (serves the static frontend + API)
PORT=3000 node server.js
