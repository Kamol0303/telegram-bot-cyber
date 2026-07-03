#!/usr/bin/env bash
# Cyber Hygiene Training — to'liq ishga tushirish
# zphisher start() menyusidan moslashtirilgan (ta'lim maqsadida)
#
# Tunnel turlari:
#   1) Localhost (mahalliy Wi-Fi)
#   2) Ngrok
#   3) Serveo
#   4) Localhost.run

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_DIR"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

banner() {
  clear 2>/dev/null || true
  echo -e "${CYAN}"
  echo "  ╔══════════════════════════════════════════════╗"
  echo "  ║   CYBER HYGIENE AWARENESS TRAINING           ║"
  echo "  ║   Ta'lim simulyatsiyasi — Phishing ko'rsatish║"
  echo "  ╚══════════════════════════════════════════════╝"
  echo -e "${NC}"
  echo -e "${YELLOW}  ⚠️  FAQAT TA'LIM MAQSADIDA — haqiqiy ma'lumot yig'ilmaydi${NC}"
  echo ""
}

select_tunnel() {
  echo -e "${CYAN}  Port forwarding (zphisher usulida):${NC}"
  echo ""
  echo "  [1] LocalHost (Wi-Fi / mahalliy)"
  echo "  [2] Ngrok.io"
  echo "  [3] Serveo.net"
  echo "  [4] Localhost.run"
  echo "  [5] Tunnel yo'q (faqat 127.0.0.1)"
  echo ""
  read -rp "  Tanlang [2]: " tunnel_opt
  tunnel_opt="${tunnel_opt:-2}"

  case "$tunnel_opt" in
    1)  bash "$SCRIPT_DIR/tunnel/local.sh" ;;
    2)  bash "$SCRIPT_DIR/tunnel/ngrok.sh" ;;
    3)  bash "$SCRIPT_DIR/tunnel/serveo.sh" ;;
    4)  bash "$SCRIPT_DIR/tunnel/localhostrun.sh" ;;
    5)  echo "http://127.0.0.1:8000" > "$PROJECT_DIR/data/public_url.txt"
        echo "none" > "$PROJECT_DIR/data/tunnel_type.txt"
        ;;
    *)  echo -e "${RED}  Noto'g'ri tanlov${NC}"; select_tunnel ;;
  esac
}

start_backend() {
  if [ -f "$PROJECT_DIR/data/backend.pid" ]; then
    old=$(cat "$PROJECT_DIR/data/backend.pid" 2>/dev/null || true)
    kill "$old" 2>/dev/null || true
  fi
  mkdir -p "$PROJECT_DIR/data"
  export PYTHONPATH="$PROJECT_DIR"

  if [ -d "$PROJECT_DIR/venv" ]; then
    # shellcheck disable=SC1091
    source "$PROJECT_DIR/venv/bin/activate"
  fi

  nohup uvicorn backend.main:app --host 0.0.0.0 --port 8000 \
    > "$PROJECT_DIR/data/backend.log" 2>&1 &
  echo $! > "$PROJECT_DIR/data/backend.pid"
  sleep 3
  echo -e "${GREEN}  [+] Backend ishga tushdi (port 8000)${NC}"
}

start_bot() {
  if [ -f "$PROJECT_DIR/data/bot.pid" ]; then
    old=$(cat "$PROJECT_DIR/data/bot.pid" 2>/dev/null || true)
    kill "$old" 2>/dev/null || true
  fi
  export PYTHONPATH="$PROJECT_DIR"

  if [ -d "$PROJECT_DIR/venv" ]; then
    # shellcheck disable=SC1091
    source "$PROJECT_DIR/venv/bin/activate"
  fi

  nohup python3 -m bot.main > "$PROJECT_DIR/data/bot.log" 2>&1 &
  echo $! > "$PROJECT_DIR/data/bot.pid"
  sleep 2
  echo -e "${GREEN}  [+] Telegram bot ishga tushdi${NC}"
}

show_result() {
  local pub_url=""
  if [ -f "$PROJECT_DIR/data/public_url.txt" ]; then
    pub_url=$(cat "$PROJECT_DIR/data/public_url.txt")
  fi

  echo ""
  echo -e "${GREEN}  ══════════════════════════════════════════${NC}"
  echo -e "${GREEN}  Platforma tayyor!${NC}"
  echo -e "${GREEN}  ══════════════════════════════════════════${NC}"
  echo ""
  echo -e "  ${CYAN}Ommaviy havola:${NC} ${YELLOW}${pub_url:-http://127.0.0.1:8000}${NC}"
  echo -e "  ${CYAN}Admin:${NC}         ${pub_url:-http://127.0.0.1:8000}/admin"
  echo -e "  ${CYAN}Telegram:${NC}      Botga /start yuboring"
  echo -e "  ${CYAN}Status:${NC}        Botga /status yuboring"
  echo ""
  echo -e "  ${CYAN}To'xtatish:${NC}    bash scripts/stop-training.sh"
  echo ""
}

# Asosiy
banner

if [ ! -f ".env" ]; then
  cp .env.example .env
  echo -e "${YELLOW}  .env yaratildi — TELEGRAM_BOT_TOKEN ni sozlang: nano .env${NC}"
fi

TOKEN=$(grep '^TELEGRAM_BOT_TOKEN=' .env 2>/dev/null | cut -d= -f2- | tr -d '"' | xargs || true)
if [ -z "$TOKEN" ] || [ "$TOKEN" = "your-telegram-bot-token-from-botfather" ]; then
  echo -e "${RED}  TELEGRAM_BOT_TOKEN sozlanmagan! nano .env${NC}"
  exit 1
fi

echo -e "${CYAN}  [1/3] Backend ishga tushirilmoqda...${NC}"
start_backend

echo -e "${CYAN}  [2/3] Tunnel tanlanmoqda...${NC}"
select_tunnel

echo -e "${CYAN}  [3/3] Telegram bot ishga tushirilmoqda...${NC}"
start_bot

show_result
