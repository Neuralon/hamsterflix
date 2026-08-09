#!/bin/bash
export $(grep -v '^#' /Users/ckaplan/.hermes-neuralon/.env | xargs)
/Users/ckaplan/dev/neuralon/carego/backend/.venv/bin/python3 /Users/ckaplan/dev/neuralon/hamster/generate_final_trailers.py
