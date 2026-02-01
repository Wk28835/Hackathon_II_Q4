#!/usr/bin/env bash
set -euo pipefail

# Developer quick-start script (tasks.md T047)
# Usage: ./scripts/setup_dev.sh

if [ ! -f "requirements.txt" ]; then
  echo "Run this script from the backend/ directory." >&2
  exit 1
fi

python -m venv venv

# shellcheck disable=SC1091
source "venv/bin/activate" 2>/dev/null || source "venv/Scripts/activate"

pip install -r requirements.txt

echo "\nNext steps:"
echo "1) Copy .env.example to .env and set DATABASE_URL + BETTER_AUTH_SECRET"
echo "2) Run: uvicorn app.main:app --reload"
echo "3) Run tests: pytest -v"
