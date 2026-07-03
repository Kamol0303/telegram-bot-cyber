#!/usr/bin/env bash
# Eski buyruq nomi — repo ildizidan ishlaydi
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT/cyber-hygiene-training" || {
  echo "[x] cyber-hygiene-training topilmadi!"
  exit 1
}
exec bash start.sh "$@"
