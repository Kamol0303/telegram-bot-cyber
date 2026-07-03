#!/usr/bin/env bash
# Umumiy tunnel funksiyalari (zphisher start/stop dan moslashtirilgan)
# Educational Cyber Hygiene Training — faqat ta'lim simulyatsiyasi uchun

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
DATA_DIR="$PROJECT_DIR/data"
BIN_DIR="$PROJECT_DIR/bin"
PUBLIC_URL_FILE="$DATA_DIR/public_url.txt"
TUNNEL_TYPE_FILE="$DATA_DIR/tunnel_type.txt"
TUNNEL_LOG="$DATA_DIR/tunnel.log"
TUNNEL_PID_FILE="$DATA_DIR/tunnel.pid"
LINK_FILE="$DATA_DIR/tunnel_link.tmp"

APP_PORT="${APP_PORT:-8000}"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

info()  { echo -e "${CYAN}[TUNNEL]${NC} $1"; }
ok()    { echo -e "${GREEN}[TUNNEL]${NC} $1"; }
warn()  { echo -e "${YELLOW}[TUNNEL]${NC} $1"; }
error() { echo -e "${RED}[TUNNEL]${NC} $1"; exit 1; }

save_public_url() {
  local url="$1"
  local type="$2"
  mkdir -p "$DATA_DIR"
  echo "$url" > "$PUBLIC_URL_FILE"
  echo "$type" > "$TUNNEL_TYPE_FILE"

  # .env dagi BASE_URL ni yangilash
  if [ -f "$PROJECT_DIR/.env" ]; then
    if grep -q '^BASE_URL=' "$PROJECT_DIR/.env"; then
      sed -i "s|^BASE_URL=.*|BASE_URL=$url|" "$PROJECT_DIR/.env"
    else
      echo "BASE_URL=$url" >> "$PROJECT_DIR/.env"
    fi
  fi

  # Python orqali ham saqlash (bot/backend uchun)
  if command -v python3 >/dev/null 2>&1; then
    export PYTHONPATH="$PROJECT_DIR"
    python3 -c "
from backend.services.url_service import set_public_url
set_public_url('$url', '$type')
" 2>/dev/null || true
  fi

  ok "Ommaviy havola saqlandi: $url"
  ok "Turi: $type"
}

get_local_ip() {
  ip route get 1 2>/dev/null | awk '{print $7; exit}' || echo "127.0.0.1"
}

stop_tunnel() {
  if [ -f "$TUNNEL_PID_FILE" ]; then
    pid=$(cat "$TUNNEL_PID_FILE" 2>/dev/null || true)
    if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then
      kill "$pid" 2>/dev/null || true
      info "Tunnel jarayoni to'xtatildi (PID: $pid)"
    fi
    rm -f "$TUNNEL_PID_FILE"
  fi

  # zphisher stop() dan — tunnel jarayonlarini tozalash
  pkill -f "ngrok http $APP_PORT" 2>/dev/null || true
  pkill -f "ngrok http ${APP_PORT}" 2>/dev/null || true
  pkill -f "ssh.*serveo.net" 2>/dev/null || true
  pkill -f "ssh.*localhost.run" 2>/dev/null || true

  rm -f "$LINK_FILE" "$DATA_DIR/tunnel_serveo.tmp"
}

# zphisher dan: ngrok binary yuklab olish (ARM/Android va x86)
install_ngrok_binary() {
  mkdir -p "$BIN_DIR"
  local ngrok_bin="$BIN_DIR/ngrok"

  if [ -x "$ngrok_bin" ]; then
    return 0
  fi

  if command -v ngrok >/dev/null 2>&1; then
    ln -sf "$(command -v ngrok)" "$ngrok_bin" 2>/dev/null || cp "$(command -v ngrok)" "$ngrok_bin"
    chmod +x "$ngrok_bin"
    return 0
  fi

  info "Ngrok yuklab olinmoqda (zphisher usulida)..."
  local arch arch2
  arch=$(uname -a | grep -o 'arm' | head -n1 || true)
  arch2=$(uname -a | grep -o 'Android' | head -n1 || true)

  cd "$BIN_DIR"
  if [[ "$arch" == "arm" ]] || [[ "$arch2" == "Android" ]]; then
    curl -# -LO "https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-arm.zip" || true
    if [ -f ngrok-stable-linux-arm.zip ]; then
      unzip -o ngrok-stable-linux-arm.zip >/dev/null 2>&1
      rm -f ngrok-stable-linux-arm.zip
      chmod +x ngrok
      cd "$PROJECT_DIR"
      return 0
    fi
  else
    curl -# -LO "https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-386.zip" || true
    if [ -f ngrok-stable-linux-386.zip ]; then
      unzip -o ngrok-stable-linux-386.zip >/dev/null 2>&1
      rm -f ngrok-stable-linux-386.zip
      chmod +x ngrok
      cd "$PROJECT_DIR"
      return 0
    fi
  fi
  cd "$PROJECT_DIR"
  return 1
}

# Ngrok API dan havola olish (ngrok.io va ngrok-free.app)
get_ngrok_url() {
  local retries=15
  local link=""
  while [ $retries -gt 0 ]; do
    link=$(curl -s http://127.0.0.1:4040/api/tunnels 2>/dev/null | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    for t in data.get('tunnels', []):
        url = t.get('public_url', '')
        if url.startswith('https://'):
            print(url)
            break
except Exception:
    pass
" 2>/dev/null || true)
    if [ -n "$link" ]; then
      echo "$link"
      return 0
    fi
    sleep 2
    retries=$((retries - 1))
  done
  # zphisher grep usuli (zaxira)
  curl -s http://127.0.0.1:4040/api/tunnels 2>/dev/null | grep -oE 'https://[0-9a-zA-Z.-]+\.(ngrok\.io|ngrok-free\.app|ngrok\.app)[^"]*' | head -n1
}

export PROJECT_DIR DATA_DIR APP_PORT PUBLIC_URL_FILE save_public_url stop_tunnel get_local_ip
