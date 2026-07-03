"""
Ta'lim maqsadida tashrif IP loglari (instruktor ko'radi).
Haqiqiy credential yig'ilmaydi — faqat IP va vaqt.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_DIR / "data"
AUTH_DIR = PROJECT_DIR / "auth"
VISITS_FILE = DATA_DIR / "visits.log"
VISITS_JSON = DATA_DIR / "visits.json"
IP_FILE = AUTH_DIR / "ip.txt"


def log_visit(ip: str, user_agent: str = "", session_token: str = "", page: str = "landing") -> dict:
    """Tashrifni mahalliy faylga yozish — serverga tashqariga yuborilmaydi."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    entry = {
        "ip": ip,
        "user_agent": user_agent[:200] if user_agent else "",
        "session_token": session_token[:16] + "..." if session_token else "",
        "page": page,
        "time": datetime.now(timezone.utc).isoformat(),
    }

    with open(VISITS_FILE, "a", encoding="utf-8") as f:
        f.write(
            f"[{entry['time']}] IP: {ip} | Page: {page} | Token: {entry['session_token']}\n"
        )

    AUTH_DIR.mkdir(parents=True, exist_ok=True)
    with open(IP_FILE, "a", encoding="utf-8") as f:
        f.write(f"{ip}\n")

    visits = []
    if VISITS_JSON.exists():
        try:
            visits = json.loads(VISITS_JSON.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            visits = []
    visits.append(entry)
    visits = visits[-100:]
    VISITS_JSON.write_text(json.dumps(visits, indent=2), encoding="utf-8")

    return entry


def get_recent_visits(limit: int = 20) -> list:
    if not VISITS_JSON.exists():
        return []
    try:
        visits = json.loads(VISITS_JSON.read_text(encoding="utf-8"))
        return visits[-limit:]
    except (json.JSONDecodeError, OSError):
        return []
