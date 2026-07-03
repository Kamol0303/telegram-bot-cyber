#!/data/data/com.termux/files/usr/bin/bash
# Cyber Hygiene Training — Termux da ishga tushirish
# Run backend + Telegram bot on Android Termux

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

info()  { echo -e "${CYAN}[*]${NC} $1"; }
ok()    { echo -e "${GREEN}[+]${NC} $1"; }
warn()  { echo -e "${YELLOW}[!]${NC} $1"; }
error() { echo -e "${RED}[x]${NC} $1"; exit 1; }

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_DIR"

PID_DIR="$PROJECT_DIR/data"
BACKEND_PID_FILE="$PID_DIR/backend.pid"
BOT_PID_FILE="$PID_DIR/bot.pid"
mkdir -p "$PID_DIR"

# Oldingi jarayonlarni to'xtatish
stop_old() {
  for pf in "$BACKEND_PID_FILE" "$BOT_PID_FILE"; do
    if [ -f "$pf" ]; then
      old_pid=$(cat "$pf" 2>/dev/null || true)
      if [ -n "$old_pid" ] && kill -0 "$old_pid" 2>/dev/null; then
        warn "Eski jarayon to'xtatilmoqda (PID: $old_pid)..."
        kill "$old_pid" 2>/dev/null || true
        sleep 1
      fi
      rm -f "$pf"
    fi
  done
}

# Virtual muhit
if [ ! -d "venv" ]; then
  error "Virtual muhit topilmadi. Avval o'rnating:\n  bash scripts/termux-setup.sh"
fi

source venv/bin/activate
export PYTHONPATH="$PROJECT_DIR"

if [ ! -f ".env" ]; then
  cp .env.example .env
  warn ".env yaratildi. Avval nano .env bilan sozlang, keyin qayta ishga tushiring."
  exit 1
fi

TELEGRAM_BOT_TOKEN=$(grep '^TELEGRAM_BOT_TOKEN=' .env | cut -d= -f2- | tr -d '"' | tr -d "'" | xargs)
if [ -z "$TELEGRAM_BOT_TOKEN" ] || [ "$TELEGRAM_BOT_TOKEN" = "your-telegram-bot-token-from-botfather" ]; then
  error "TELEGRAM_BOT_TOKEN sozlanmagan!\n  nano .env"
fi

stop_old

LOCAL_IP=$(ip route get 1 2>/dev/null | awk '{print $7; exit}' || echo "127.0.0.1")

info "Backend ishga tushirilmoqda..."
nohup uvicorn backend.main:app --host 0.0.0.0 --port 8000 > "$PID_DIR/backend.log" 2>&1 &
echo $! > "$BACKEND_PID_FILE"
sleep 3

if ! kill -0 "$(cat "$BACKEND_PID_FILE")" 2>/dev/null; then
  error "Backend ishga tushmadi. Log: data/backend.log"
fi

info "Telegram bot ishga tushirilmoqda..."
nohup python -m bot.main > "$PID_DIR/bot.log" 2>&1 &
echo $! > "$BOT_PID_FILE"
sleep 2

if ! kill -0 "$(cat "$BOT_PID_FILE")" 2>/dev/null; then
  error "Bot ishga tushmadi. Log: data/bot.log"
fi

echo ""
echo "============================================"
ok "Platforma ishga tushdi!"
echo "============================================"
echo ""
echo "  Telefon brauzeri:  http://127.0.0.1:8000"
echo "  Wi-Fi (boshqalar): http://${LOCAL_IP}:8000"
echo "  Admin panel:       http://127.0.0.1:8000/admin"
echo "  Sog'liq tekshiruv: http://127.0.0.1:8000/health"
echo ""
echo "  Telegram: botingizga /start yuboring"
echo ""
echo "  Loglar:"
echo "    data/backend.log"
echo "    data/bot.log"
echo ""
echo "  To'xtatish: bash scripts/stop-termux.sh"
echo "============================================"
