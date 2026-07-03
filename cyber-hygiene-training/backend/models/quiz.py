"""
Quiz attempt model — stores scores and completion only, not answers with PII.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from backend.database import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class QuizAttempt(Base):
    """Records quiz completion for analytics and certificate generation."""

    __tablename__ = "quiz_attempts"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    session_token: Mapped[str] = mapped_column(String(64), index=True)
    score: Mapped[int] = mapped_column(Integer)
    total_questions: Mapped[int] = mapped_column(Integer, default=10)
    percentage: Mapped[float] = mapped_column(Float)
    certificate_id: Mapped[str] = mapped_column(String(32), unique=True)
    completed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    # JSON string of question IDs answered correctly — no free-text PII
    results_summary: Mapped[str] = mapped_column(Text, default="{}")
