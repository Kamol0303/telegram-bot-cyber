#!/usr/bin/env bash
# Telegram menu — zphisher uslubida, Cloudflared avto havola
cd "$(dirname "$0")/cyber-hygiene-training" 2>/dev/null || cd "$(dirname "$0")"
exec python3 scripts/telegram_menu.py
