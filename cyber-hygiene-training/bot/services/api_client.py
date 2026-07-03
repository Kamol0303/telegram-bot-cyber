"""API client for creating training sessions from the bot."""

import logging

import httpx

from bot.config import bot_settings

logger = logging.getLogger(__name__)


async def create_training_session(telegram_user_id: int) -> dict | None:
    """Request anonymous session token from FastAPI backend."""
    url = f"{bot_settings.base_url}/api/sessions"
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(
                url,
                json={"telegram_user_id": telegram_user_id},
            )
            if response.status_code == 200:
                return response.json()
            logger.error("Session creation failed: %s %s", response.status_code, response.text)
    except httpx.HTTPError as exc:
        logger.error("Backend unreachable: %s", exc)
    return None
