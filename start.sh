#!/usr/bin/env bash
# Repo ildizi — cyber-hygiene-training ga yo'naltirish
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT/cyber-hygiene-training" || {
  echo "[x] cyber-hygiene-training papkasi topilmadi!"
  echo "    Siz ~/telegram-bot-cyber papkasidamisiz? Tekshiring: ls"
  exit 1
}
exec bash start.sh "$@"
