#!/usr/bin/env bash
# Localhost — faqat mahalliy tarmoq (zphisher start_l dan)

source "$(dirname "$0")/lib.sh"

LOCAL_IP=$(get_local_ip)
URL="http://${LOCAL_IP}:${APP_PORT}"

save_public_url "$URL" "localhost"
ok "Ta'lim platformasi mahalliy tarmoqda:"
echo "  $URL"
echo "  http://127.0.0.1:${APP_PORT}"
warn "Bu havola faqat bir xil Wi-Fi tarmog'idagi qurilmalar uchun ishlaydi."
