#!/usr/bin/env bash
# Barcha tunnellarni to'xtatish (zphisher stop() dan)

source "$(dirname "$0")/lib.sh"

stop_tunnel
rm -f "$PUBLIC_URL_FILE" "$TUNNEL_TYPE_FILE"
ok "Tunnellar to'xtatildi va ommaviy havola tozalandi."
