#!/data/data/com.termux/files/usr/bin/bash
# Cyber Hygiene Training — Termux da to'xtatish

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
PID_DIR="$PROJECT_DIR/data"

stop_pid_file() {
  local pf="$1"
  local name="$2"
  if [ -f "$pf" ]; then
    pid=$(cat "$pf" 2>/dev/null || true)
    if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then
      kill "$pid" 2>/dev/null && echo "[+] $name to'xtatildi (PID: $pid)"
    else
      echo "[*] $name allaqachon to'xtagan"
    fi
    rm -f "$pf"
  else
    echo "[*] $name PID fayli topilmadi"
  fi
}

stop_pid_file "$PID_DIR/backend.pid" "Backend"
stop_pid_file "$PID_DIR/bot.pid" "Telegram bot"

# Qolgan uvicorn/bot jarayonlarini tozalash
pkill -f "uvicorn backend.main:app" 2>/dev/null && echo "[+] Qolgan uvicorn jarayonlari to'xtatildi" || true
pkill -f "python -m bot.main" 2>/dev/null && echo "[+] Qolgan bot jarayonlari to'xtatildi" || true

echo "[+] Tayyor"
