#!/data/data/com.termux/files/usr/bin/bash
# Termux: to'liq platforma + tunnel (zphisher integratsiyasi)
# Eski start-termux.sh o'rniga start-training.sh ni chaqiradi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec bash "$SCRIPT_DIR/start-training.sh"
