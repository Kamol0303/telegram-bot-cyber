#!/usr/bin/env bash
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT/cyber-hygiene-training" || exit 1
exec bash setup.sh "$@"
