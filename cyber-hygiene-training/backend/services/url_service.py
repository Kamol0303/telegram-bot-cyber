"""
Dynamic public URL resolver for tunnel integration.
Reads tunnel URL written by scripts/tunnel (adapted from zphisher port-forwarding).
"""

from pathlib import Path

from backend.config import get_settings

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
PUBLIC_URL_FILE = DATA_DIR / "public_url.txt"
TUNNEL_TYPE_FILE = DATA_DIR / "tunnel_type.txt"


def get_base_url() -> str:
    """
    Return public training URL.
    Priority: data/public_url.txt (tunnel) > BASE_URL from .env
    """
    if PUBLIC_URL_FILE.exists():
        try:
            url = PUBLIC_URL_FILE.read_text(encoding="utf-8").strip()
            if url:
                return url.rstrip("/")
        except OSError:
            pass
    return get_settings().base_url.rstrip("/")


def get_tunnel_info() -> dict:
    """Return current tunnel status for API and bot."""
    public_url = None
    tunnel_type = "none"

    if PUBLIC_URL_FILE.exists():
        try:
            public_url = PUBLIC_URL_FILE.read_text(encoding="utf-8").strip() or None
        except OSError:
            pass

    if TUNNEL_TYPE_FILE.exists():
        try:
            tunnel_type = TUNNEL_TYPE_FILE.read_text(encoding="utf-8").strip() or "unknown"
        except OSError:
            pass

    return {
        "public_url": public_url,
        "tunnel_type": tunnel_type,
        "active": bool(public_url),
        "local_url": "http://127.0.0.1:8000",
    }


def set_public_url(url: str, tunnel_type: str = "manual") -> None:
    """Save public URL (used by tunnel scripts via CLI)."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    PUBLIC_URL_FILE.write_text(url.rstrip("/") + "\n", encoding="utf-8")
    TUNNEL_TYPE_FILE.write_text(tunnel_type + "\n", encoding="utf-8")
