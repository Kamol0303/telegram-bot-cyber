"""
Training session model.
Stores only anonymous session tokens and progress — never PII or payment data.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.database import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class TrainingSession(Base):
    """Anonymous training session linked to a Telegram user ID hash."""

    __tablename__ = "training_sessions"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    token: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    telegram_user_id_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    landing_viewed: Mapped[bool] = mapped_column(Boolean, default=False)
    simulation_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    reveal_viewed: Mapped[bool] = mapped_column(Boolean, default=False)
    learning_viewed: Mapped[bool] = mapped_column(Boolean, default=False)
    quiz_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow
    )
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
