"""Admin authentication and statistics service."""

import json
from datetime import datetime, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.config import get_settings
from backend.models.admin import AdminAuditLog
from backend.models.quiz import QuizAttempt
from backend.models.session import TrainingSession

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"
TOKEN_EXPIRE_HOURS = 8


def verify_admin_credentials(username: str, password: str) -> bool:
    return username == settings.admin_username and password == settings.admin_password


def create_admin_token(username: str) -> str:
    expire = datetime.now(timezone.utc).timestamp() + TOKEN_EXPIRE_HOURS * 3600
    payload = {"sub": username, "exp": expire, "role": "admin"}
    return jwt.encode(payload, settings.secret_key, algorithm=ALGORITHM)


def verify_admin_token(token: str) -> str | None:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        if payload.get("role") != "admin":
            return None
        return payload.get("sub")
    except JWTError:
        return None


async def log_admin_action(
    db: AsyncSession, action: str, details: str = "", ip: str | None = None
) -> None:
    log = AdminAuditLog(action=action, details=details, ip_address=ip)
    db.add(log)
    await db.flush()


async def get_platform_stats(db: AsyncSession) -> dict:
    total_sessions = await db.scalar(select(func.count()).select_from(TrainingSession))
    completed_sim = await db.scalar(
        select(func.count())
        .select_from(TrainingSession)
        .where(TrainingSession.simulation_completed.is_(True))
    )
    completed_quiz = await db.scalar(
        select(func.count())
        .select_from(TrainingSession)
        .where(TrainingSession.quiz_completed.is_(True))
    )
    avg_score = await db.scalar(select(func.avg(QuizAttempt.percentage))) or 0.0

    recent = await db.execute(
        select(TrainingSession)
        .order_by(TrainingSession.created_at.desc())
        .limit(10)
    )
    recent_sessions = [
        {
            "id": s.id[:8],
            "landing": s.landing_viewed,
            "simulation": s.simulation_completed,
            "quiz": s.quiz_completed,
            "created": s.created_at.isoformat() if s.created_at else None,
        }
        for s in recent.scalars().all()
    ]

    return {
        "total_sessions": total_sessions or 0,
        "completed_simulations": completed_sim or 0,
        "completed_quizzes": completed_quiz or 0,
        "average_quiz_score": round(float(avg_score), 1),
        "recent_sessions": recent_sessions,
    }
