#!/usr/bin/env bash
# Cyber Hygiene Training — to'xtatish

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

stop_pid() {
  local f="$1" name="$2"
  if [ -f "$f" ]; then
    pid=$(cat "$f" 2>/dev/null || true)
    if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then
      kill "$pid" 2>/dev/null && echo "[+] $name to'xtatildi"
    fi
    rm -f "$f"
  fi
}

stop_pid "$PROJECT_DIR/data/backend.pid" "Backend"
stop_pid "$PROJECT_DIR/data/bot.pid" "Telegram bot"
bash "$SCRIPT_DIR/tunnel/stop.sh" 2>/dev/null || true

pkill -f "uvicorn backend.main:app" 2>/dev/null || true
pkill -f "python3 -m bot.main" 2>/dev/null || true

echo "[+] Barcha xizmatlar to'xtatildi"
