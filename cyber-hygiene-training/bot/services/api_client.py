"""API client for creating training sessions from the bot."""

import logging
import os

import httpx

from backend.services.url_service import get_base_url

logger = logging.getLogger(__name__)

# Bot doim mahalliy backend bilan gaplashadi (tunnel faqat foydalanuvchi havolasi uchun)
LOCAL_BACKEND = os.getenv("LOCAL_API_URL", "http://127.0.0.1:8000").rstrip("/")


def get_public_base_url() -> str:
    """Ommaviy havola — tunnel yoki BASE_URL (foydalanuvchilar uchun)."""
    return get_base_url()


async def create_training_session(telegram_user_id: int) -> dict | None:
    """Request anonymous session token from local FastAPI backend."""
    url = f"{LOCAL_BACKEND}/api/sessions"
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(
                url,
                json={"telegram_user_id": telegram_user_id},
            )
            if response.status_code == 200:
                data = response.json()
                token = data.get("token")
                public_base = get_public_base_url()
                if token:
                    data["simulation_url"] = f"{public_base}/?token={token}"
                return data
            logger.error("Session creation failed: %s %s", response.status_code, response.text)
    except httpx.HTTPError as exc:
        logger.error("Backend unreachable at %s: %s", LOCAL_BACKEND, exc)
    return None


async def fetch_tunnel_status() -> dict | None:
    """Get tunnel/public URL status from local backend."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{LOCAL_BACKEND}/api/tunnel/status")
            if response.status_code == 200:
                return response.json()
    except httpx.HTTPError as exc:
        logger.error("Tunnel status unreachable: %s", exc)
    return None
