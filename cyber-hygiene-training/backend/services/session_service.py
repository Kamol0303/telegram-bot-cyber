"""
Session management service.
Creates anonymous tokens — never stores names, phones, cards, or OTP codes.
"""

import hashlib
import secrets
from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.config import get_settings
from backend.models.session import TrainingSession

settings = get_settings()


def hash_telegram_id(user_id: int) -> str:
    """One-way hash of Telegram user ID for anonymous analytics."""
    return hashlib.sha256(f"{user_id}:{settings.secret_key}".encode()).hexdigest()[:32]


def generate_token() -> str:
    return secrets.token_urlsafe(32)


async def create_session(
    db: AsyncSession, telegram_user_id: int | None = None
) -> TrainingSession:
    """Create a new anonymous training session."""
    now = datetime.now(timezone.utc)
    session = TrainingSession(
        token=generate_token(),
        telegram_user_id_hash=hash_telegram_id(telegram_user_id) if telegram_user_id else None,
        expires_at=now + timedelta(hours=settings.session_token_expire_hours),
    )
    db.add(session)
    await db.flush()
    return session


async def get_session_by_token(db: AsyncSession, token: str) -> TrainingSession | None:
    result = await db.execute(
        select(TrainingSession).where(TrainingSession.token == token)
    )
    return result.scalar_one_or_none()


def is_session_valid(session: TrainingSession | None) -> bool:
    if session is None:
        return False
    now = datetime.now(timezone.utc)
    expires = session.expires_at
    if expires.tzinfo is None:
        expires = expires.replace(tzinfo=timezone.utc)
    return now < expires


async def update_session_progress(
    db: AsyncSession,
    token: str,
    landing_viewed: bool | None = None,
    simulation_completed: bool | None = None,
    reveal_viewed: bool | None = None,
    learning_viewed: bool | None = None,
) -> TrainingSession | None:
    session = await get_session_by_token(db, token)
    if not session or not is_session_valid(session):
        return None
    if landing_viewed is not None:
        session.landing_viewed = landing_viewed
    if simulation_completed is not None:
        session.simulation_completed = simulation_completed
    if reveal_viewed is not None:
        session.reveal_viewed = reveal_viewed
    if learning_viewed is not None:
        session.learning_viewed = learning_viewed
    session.updated_at = datetime.now(timezone.utc)
    await db.flush()
    return session
