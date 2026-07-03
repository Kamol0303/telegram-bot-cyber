#!/usr/bin/env bash
# Kali / Linux — bir buyruqda o'rnatish va ishga tushirish
# Git pull ishlamasa ham ishlaydi (yangi klon qiladi)
#
# Ishlatish:
#   bash install-kali.sh
# yoki:
#   curl -fsSL https://raw.githubusercontent.com/Kamol0303/telegram-bot-cyber/main/install-kali.sh | bash

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

INSTALL_DIR="${INSTALL_DIR:-$HOME/telegram-bot-cyber}"
REPO_URL="https://github.com/Kamol0303/telegram-bot-cyber.git"

info "Cyber Hygiene Training — Kali/Linux o'rnatuvchi"
info "Maqsad papka: $INSTALL_DIR"
echo ""

# Tizim paketlari
info "Tizim paketlari tekshirilmoqda..."
if command -v apt >/dev/null 2>&1; then
  sudo apt update -qq
  sudo apt install -y python3 python3-venv python3-pip git curl openssh-client unzip 2>/dev/null || \
  apt install -y python3 python3-venv python3-pip git curl openssh-client unzip 2>/dev/null || true
fi

clone_fresh() {
  local backup="${INSTALL_DIR}.old.$(date +%s)"
  if [ -d "$INSTALL_DIR" ]; then
    warn "Eski papka zaxiralanmoqda: $backup"
    mv "$INSTALL_DIR" "$backup" 2>/dev/null || sudo mv "$INSTALL_DIR" "$backup"
  fi
  info "GitHub dan yuklab olinmoqda..."
  git clone "$REPO_URL" "$INSTALL_DIR"
}

update_repo() {
  if [ ! -d "$INSTALL_DIR/.git" ]; then
    clone_fresh
    return
  fi

  info "Git ruxsatlari tuzatilmoqda..."
  sudo chown -R "$USER:$USER" "$INSTALL_DIR" 2>/dev/null || chown -R "$USER:$USER" "$INSTALL_DIR" 2>/dev/null || true

  cd "$INSTALL_DIR"
  if git pull origin main 2>/dev/null; then
    ok "Yangilandi (git pull)"
    return
  fi

  warn "git pull ishlamadi — yangi nusxa yuklanmoqda..."
  cd "$HOME"
  clone_fresh
}

update_repo
cd "$INSTALL_DIR"

# Papka tekshiruvi
if [ ! -d "cyber-hygiene-training" ]; then
  error "cyber-hygiene-training topilmadi! clone muvaffaqiyatsiz."
fi

if [ ! -f "scripts/start-training.sh" ]; then
  error "scripts/start-training.sh topilmadi! git pull yoki qayta clone kerak."
fi

ok "Loyiha tayyor: $INSTALL_DIR"

# O'rnatish
info "Python kutubxonalari o'rnatilmoqda..."
bash setup.sh

# .env
ENV_FILE="$INSTALL_DIR/cyber-hygiene-training/.env"
if [ ! -f "$ENV_FILE" ]; then
  cp "$INSTALL_DIR/cyber-hygiene-training/.env.example" "$ENV_FILE"
fi

if grep -q "your-telegram-bot-token-from-botfather" "$ENV_FILE" 2>/dev/null; then
  echo ""
  warn "TELEGRAM_BOT_TOKEN hali sozlanmagan!"
  echo ""
  echo "  nano $ENV_FILE"
  echo ""
  echo "Keyin ishga tushiring:"
  echo "  cd $INSTALL_DIR"
  echo "  bash scripts/start-training.sh"
  echo ""
  exit 0
fi

echo ""
read -rp "Hozir ishga tushirilsinmi? [Y/n]: " ans
ans="${ans:-Y}"
if [[ "$ans" =~ ^[Yy]$ ]]; then
  bash scripts/start-training.sh
else
  echo ""
  ok "Tayyor! Ishga tushirish:"
  echo "  cd $INSTALL_DIR"
  echo "  bash scripts/start-training.sh"
  echo ""
fi
