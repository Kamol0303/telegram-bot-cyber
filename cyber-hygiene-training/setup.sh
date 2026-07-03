#!/usr/bin/env bash
# Universal setup — Termux, Linux, macOS
cd "$(dirname "$0")"

if [ -d "/data/data/com.termux" ]; then
  exec python3 scripts/launcher.py setup --termux "$@"
else
  exec python3 scripts/launcher.py setup "$@"
fi
