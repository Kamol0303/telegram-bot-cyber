#!/usr/bin/env bash
# Ngrok tunnel (zphisher start_n dan moslashtirilgan — ta'lim uchun)

source "$(dirname "$0")/lib.sh"

stop_tunnel
mkdir -p "$DATA_DIR" "$BIN_DIR"

# Ngrok authtoken (.env dan)
NGROK_AUTHTOKEN=""
if [ -f "$PROJECT_DIR/.env" ]; then
  NGROK_AUTHTOKEN=$(grep '^NGROK_AUTHTOKEN=' "$PROJECT_DIR/.env" | cut -d= -f2- | tr -d '"' | tr -d "'" | xargs || true)
fi

if ! install_ngrok_binary; then
  error "Ngrok o'rnatilmadi. .env ga NGROK_AUTHTOKEN qo'shing yoki: pkg install ngrok"
fi

NGROK_BIN="$BIN_DIR/ngrok"
[ -x "$NGROK_BIN" ] || NGROK_BIN="ngrok"

if [ -n "$NGROK_AUTHTOKEN" ]; then
  "$NGROK_BIN" config add-authtoken "$NGROK_AUTHTOKEN" >/dev/null 2>&1 || \
  "$NGROK_BIN" authtoken "$NGROK_AUTHTOKEN" >/dev/null 2>&1 || true
fi

info "Ngrok ishga tushirilmoqda (port $APP_PORT)..."
nohup "$NGROK_BIN" http "$APP_PORT" --log=stdout > "$TUNNEL_LOG" 2>&1 &
echo $! > "$TUNNEL_PID_FILE"

sleep 3
LINK=$(get_ngrok_url)

if [ -z "$LINK" ]; then
  warn "Ngrok havolasi olinmadi. Log: $TUNNEL_LOG"
  warn "NGROK_AUTHTOKEN kerak bo'lishi mumkin: https://dashboard.ngrok.com"
  exit 1
fi

save_public_url "$LINK" "ngrok"
echo ""
ok "Ta'lim simulyatsiyasi uchun ommaviy havola:"
echo -e "  \033[1;93m$LINK\033[0m"
echo ""
info "Bu havolani Telegram bot orqali ishtirokchilarga yuboring."
