"""
Dynamic public URL resolver for tunnel integration.
Reads tunnel URL written by scripts/tunnel (adapted from zphisher port-forwarding).
"""

from pathlib import Path

import json

from backend.config import get_settings

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
PUBLIC_URL_FILE = DATA_DIR / "public_url.txt"
TUNNEL_TYPE_FILE = DATA_DIR / "tunnel_type.txt"
MASK_URLS_FILE = DATA_DIR / "mask_urls.json"


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
        "mask_urls": get_mask_urls(),
    }


def get_mask_urls() -> dict | None:
    """Mask URL lar (URL 1, URL 2, URL 3) — ta'lim uchun."""
    if MASK_URLS_FILE.exists():
        try:
            return json.loads(MASK_URLS_FILE.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            pass
    return None


def set_public_url(url: str, tunnel_type: str = "manual") -> None:
    """Save public URL (used by tunnel scripts via CLI)."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    PUBLIC_URL_FILE.write_text(url.rstrip("/") + "\n", encoding="utf-8")
    TUNNEL_TYPE_FILE.write_text(tunnel_type + "\n", encoding="utf-8")
