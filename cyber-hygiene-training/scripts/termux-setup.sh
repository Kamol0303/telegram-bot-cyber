#!/data/data/com.termux/files/usr/bin/bash
# Cyber Hygiene Training — Termux bir martalik o'rnatish skripti
# One-time setup script for Termux (Android)

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

# Loyiha papkasini topish
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_DIR"

info "Cyber Hygiene Training — Termux o'rnatish"
info "Loyiha papkasi: $PROJECT_DIR"

# Termux tekshiruvi
if [ ! -d "/data/data/com.termux" ]; then
  warn "Bu skript Termux uchun mo'ljallangan."
  warn "Linux/macOS da oddiy start.sh dan foydalaning."
fi

# Tizim paketlarini o'rnatish
info "Termux paketlari o'rnatilmoqda..."
pkg update -y
pkg install -y python python-pip git rust libffi openssl openssh curl unzip

# Virtual muhit
if [ ! -d "venv" ]; then
  info "Virtual muhit yaratilmoqda..."
  python -m venv venv
fi

source venv/bin/activate

info "Python kutubxonalari o'rnatilmoqda (bir necha daqiqa davom etishi mumkin)..."
pip install --upgrade pip
pip install -r requirements.txt

mkdir -p data

# .env fayli
if [ ! -f ".env" ]; then
  cp .env.example .env
  ok ".env fayli yaratildi"
else
  ok ".env allaqachon mavjud"
fi

# Telefon IP manzilini aniqlash
LOCAL_IP=$(ip route get 1 2>/dev/null | awk '{print $7; exit}' || echo "127.0.0.1")

echo ""
echo "============================================"
ok "O'rnatish tugallandi!"
echo "============================================"
echo ""
echo "Keyingi qadamlar:"
echo ""
echo "1) .env faylini tahrirlang:"
echo "   nano .env"
echo ""
echo "2) Quyidagilarni to'ldiring:"
echo "   TELEGRAM_BOT_TOKEN=BotFather dan olingan token"
echo "   SECRET_KEY=$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
echo "   ADMIN_PASSWORD=kuchli-parol"
echo ""
echo "3) BASE_URL ni sozlang:"
echo "   Faqat shu telefonda:  BASE_URL=http://127.0.0.1:8000"
echo "   Wi-Fi orqali boshqalar: BASE_URL=http://${LOCAL_IP}:8000"
echo ""
echo "4) Ishga tushiring:"
echo "   bash scripts/start-termux.sh"
echo ""
