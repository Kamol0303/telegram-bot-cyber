#!/usr/bin/env bash
# Universal start — Termux, Linux, macOS
cd "$(dirname "$0")"
exec python3 scripts/launcher.py start "$@"
