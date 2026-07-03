#!/usr/bin/env bash
# Start the Cyber Hygiene Awareness Training Platform

set -euo pipefail
cd "$(dirname "$0")"

PYTHON=python3

if [ ! -d "venv" ]; then
  $PYTHON -m venv venv 2>/dev/null || true
fi

if [ -f "venv/bin/activate" ]; then
  source venv/bin/activate
fi

pip install -q -r requirements.txt

mkdir -p data
export PYTHONPATH="$(pwd)"

if [ ! -f ".env" ]; then
  cp .env.example .env
  echo "Created .env from .env.example — please configure TELEGRAM_BOT_TOKEN"
fi

echo "Starting FastAPI backend on http://localhost:8000"
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

sleep 2

echo "Starting Telegram bot..."
$PYTHON -m bot.main &
BOT_PID=$!

trap "kill $BACKEND_PID $BOT_PID 2>/dev/null" EXIT

echo ""
echo "============================================"
echo " Cyber Hygiene Awareness Training Platform"
echo "============================================"
echo " Web:   http://localhost:8000"
echo " Admin: http://localhost:8000/admin"
echo " Health: http://localhost:8000/health"
echo "============================================"

wait
