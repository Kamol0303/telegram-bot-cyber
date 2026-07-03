#!/usr/bin/env python3
"""
Cross-platform launcher — Termux, Linux, Windows, macOS.
Usage:
  python scripts/launcher.py setup
  python scripts/launcher.py start
  python scripts/launcher.py stop
  python scripts/launcher.py status
"""

from __future__ import annotations

import argparse
import os
import secrets
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path

# Loyiha ildizi
PROJECT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_DIR))

from scripts.platform_util import (  # noqa: E402
    Platform,
    detect_platform,
    get_pip_cmd,
    get_python_cmd,
    get_start_hint,
    get_stop_hint,
    is_windows,
    platform_label,
)
from scripts.tunnel_manager import TunnelManager, APP_PORT  # noqa: E402

DATA_DIR = PROJECT_DIR / "data"
BACKEND_PID = DATA_DIR / "backend.pid"
BOT_PID = DATA_DIR / "bot.pid"
BACKEND_LOG = DATA_DIR / "backend.log"
BOT_LOG = DATA_DIR / "bot.log"


def _py_list(project_dir: str) -> list[str]:
    cmd = get_python_cmd(project_dir)
    if " " in cmd:
        return cmd.split()
    return [cmd]


def banner() -> None:
    plat = detect_platform()
    print()
    print("  ╔══════════════════════════════════════════════╗")
    print("  ║   CYBER HYGIENE AWARENESS TRAINING           ║")
    print(f"  ║   Platforma: {platform_label(plat):<30} ║")
    print("  ╚══════════════════════════════════════════════╝")
    print()


def ensure_env() -> None:
    env_file = PROJECT_DIR / ".env"
    example = PROJECT_DIR / ".env.example"
    if not env_file.exists() and example.exists():
        shutil.copy(example, env_file)
        print("[+] .env yaratildi — TELEGRAM_BOT_TOKEN ni sozlang")


def check_token() -> bool:
    env_file = PROJECT_DIR / ".env"
    if not env_file.exists():
        return False
    for line in env_file.read_text(encoding="utf-8").splitlines():
        if line.startswith("TELEGRAM_BOT_TOKEN="):
            token = line.split("=", 1)[1].strip().strip('"').strip("'")
            if token and token != "your-telegram-bot-token-from-botfather":
                return True
    return False


def cmd_setup(termux: bool = False) -> None:
    banner()
    plat = detect_platform()
    print(f"[*] O'rnatish: {platform_label(plat)}")

    if termux or plat == Platform.TERMUX:
        print("[*] Termux paketlari o'rnatilmoqda...")
        subprocess.run(
            ["pkg", "install", "-y", "python", "python-pip", "git", "rust",
             "libffi", "openssl", "openssh", "curl", "unzip"],
            check=False,
        )

    py = _py_list(str(PROJECT_DIR))[0]
    venv_dir = PROJECT_DIR / "venv"

    if not venv_dir.exists():
        print("[*] Virtual muhit yaratilmoqda...")
        subprocess.run([py, "-m", "venv", str(venv_dir)], check=True)

    pip = get_pip_cmd(str(PROJECT_DIR))
    print("[*] Kutubxonalar o'rnatilmoqda...")
    subprocess.run(pip + ["install", "--upgrade", "pip"], check=False)
    subprocess.run(pip + ["install", "-r", str(PROJECT_DIR / "requirements.txt")], check=True)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    ensure_env()

    secret = secrets.token_urlsafe(32)
    print()
    print("=" * 44)
    print("[+] O'rnatish tugallandi!")
    print("=" * 44)
    print()
    print("Keyingi qadamlar:")
    print("  1) .env faylini tahrirlang (TELEGRAM_BOT_TOKEN)")
    print(f"  2) SECRET_KEY={secret}")
    print(f"  3) Ishga tushiring: {get_start_hint()}")
    print()


def _kill_pid(pid: int) -> None:
    if is_windows():
        subprocess.run(["taskkill", "/F", "/PID", str(pid)], capture_output=True)
    else:
        try:
            os.kill(pid, signal.SIGTERM)
        except OSError:
            pass


def _read_pid(path: Path) -> int | None:
    if not path.exists():
        return None
    try:
        return int(path.read_text().strip())
    except ValueError:
        return None


def stop_services() -> None:
    for name, pid_file in [("Backend", BACKEND_PID), ("Bot", BOT_PID)]:
        pid = _read_pid(pid_file)
        if pid:
            _kill_pid(pid)
            print(f"[+] {name} to'xtatildi (PID {pid})")
        pid_file.unlink(missing_ok=True)

    TunnelManager(PROJECT_DIR).stop()

    if is_windows():
        for img in ("uvicorn.exe", "python.exe"):
            subprocess.run(
                ["taskkill", "/F", "/FI", f"WINDOWTITLE eq *backend*"],
                capture_output=True,
            )
    else:
        subprocess.run(["pkill", "-f", "uvicorn backend.main:app"], capture_output=True)
        subprocess.run(["pkill", "-f", "bot.main"], capture_output=True)

    print("[+] Barcha xizmatlar to'xtatildi")


def start_process(name: str, args: list[str], pid_file: Path, log_file: Path) -> None:
    old = _read_pid(pid_file)
    if old:
        _kill_pid(old)

    env = os.environ.copy()
    env["PYTHONPATH"] = str(PROJECT_DIR)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    log = open(log_file, "w", encoding="utf-8")

    kwargs: dict = {}
    if is_windows():
        kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS
    else:
        kwargs["start_new_session"] = True

    proc = subprocess.Popen(args, stdout=log, stderr=subprocess.STDOUT, env=env, **kwargs)
    pid_file.write_text(str(proc.pid), encoding="utf-8")
    print(f"[+] {name} ishga tushdi (PID {proc.pid})")


def start_backend() -> None:
    py = _py_list(str(PROJECT_DIR))
    uvicorn = shutil.which("uvicorn")
    if uvicorn and not is_windows():
        cmd = [uvicorn, "backend.main:app", "--host", "0.0.0.0", "--port", str(APP_PORT)]
    else:
        cmd = py + ["-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", str(APP_PORT)]
    start_process("Backend", cmd, BACKEND_PID, BACKEND_LOG)
    time.sleep(3)


def start_bot() -> None:
    py = _py_list(str(PROJECT_DIR))
    cmd = py + ["-m", "bot.main"]
    start_process("Telegram bot", cmd, BOT_PID, BOT_LOG)
    time.sleep(2)


def select_tunnel() -> str:
    print()
    print("  Port forwarding:")
    print("  [1] LocalHost (Wi-Fi / mahalliy)")
    print("  [2] Ngrok.io          (tavsiya)")
    print("  [3] Serveo.net")
    print("  [4] Localhost.run")
    print("  [5] Tunnel yo'q (127.0.0.1)")
    print()

    try:
        choice = input("  Tanlang [2]: ").strip() or "2"
    except (EOFError, KeyboardInterrupt):
        choice = "2"

    tm = TunnelManager(PROJECT_DIR)
    try:
        return tm.start_tunnel(choice)
    except Exception as e:
        print(f"[!] Tunnel xatosi: {e}")
        print("[*] Mahalliy rejimga o'tilmoqda...")
        return tm.start_none()


def cmd_start(tunnel: str | None = None) -> None:
    banner()
    ensure_env()

    if not check_token():
        print("[x] TELEGRAM_BOT_TOKEN sozlanmagan! .env faylini tahrirlang.")
        sys.exit(1)

    print("[1/3] Backend ishga tushirilmoqda...")
    start_backend()

    print("[2/3] Tunnel sozlanmoqda...")
    if tunnel:
        url = TunnelManager(PROJECT_DIR).start_tunnel(tunnel)
    else:
        url = select_tunnel()

    print("[3/3] Telegram bot ishga tushirilmoqda...")
    start_bot()

    pub_file = DATA_DIR / "public_url.txt"
    public = pub_file.read_text().strip() if pub_file.exists() else url

    print()
    print("=" * 44)
    print("  Platforma tayyor!")
    print("=" * 44)
    print(f"  Ommaviy havola: {public}")
    print(f"  Admin:          {public}/admin")
    print(f"  Telegram:       /start")
    print(f"  To'xtatish:     {get_stop_hint()}")
    print()


def cmd_status() -> None:
    banner()
    for name, pid_file in [("Backend", BACKEND_PID), ("Bot", BOT_PID)]:
        pid = _read_pid(pid_file)
        status = f"ishlayapti (PID {pid})" if pid else "to'xtagan"
        print(f"  {name}: {status}")

    pub = DATA_DIR / "public_url.txt"
    if pub.exists():
        print(f"  Havola: {pub.read_text().strip()}")
    print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Cyber Hygiene Training Launcher")
    parser.add_argument("command", choices=["setup", "start", "stop", "status"])
    parser.add_argument("--termux", action="store_true", help="Termux paketlarini o'rnatish")
    parser.add_argument(
        "--tunnel", choices=["1", "2", "3", "4", "5"],
        help="Tunnel tanlovi (interaktiv so'ramsiz)",
    )
    args = parser.parse_args()

    os.chdir(PROJECT_DIR)

    if args.command == "setup":
        cmd_setup(termux=args.termux)
    elif args.command == "start":
        cmd_start(tunnel=args.tunnel)
    elif args.command == "stop":
        banner()
        stop_services()
    elif args.command == "status":
        cmd_status()


if __name__ == "__main__":
    main()
