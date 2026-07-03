#!/usr/bin/env bash
# Universal stop — Termux, Linux, macOS
cd "$(dirname "$0")"
exec python3 scripts/launcher.py stop "$@"
