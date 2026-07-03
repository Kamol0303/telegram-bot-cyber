"""Quiz submission and certificate generation service."""

import json
import secrets
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.quiz import QuizAttempt
from backend.models.session import TrainingSession
from backend.services.quiz_data import grade_quiz
from backend.services.session_service import get_session_by_token, is_session_valid


def generate_certificate_id() -> str:
    return f"CHT-{secrets.token_hex(4).upper()}-{datetime.now(timezone.utc).strftime('%Y%m')}"


async def submit_quiz(
    db: AsyncSession,
    session_token: str,
    answers: dict,
) -> dict | None:
    """Grade quiz and persist only score metadata — never sensitive inputs."""
    session = await get_session_by_token(db, session_token)
    if not session or not is_session_valid(session):
        return None

    existing = await db.execute(
        select(QuizAttempt).where(QuizAttempt.session_token == session_token)
    )
    if existing.scalar_one_or_none():
        return None

    score, total, results = grade_quiz(answers)
    percentage = round((score / total) * 100, 1)
    cert_id = generate_certificate_id()

    correct_ids = [r["question_id"] for r in results if r["is_correct"]]
    attempt = QuizAttempt(
        session_token=session_token,
        score=score,
        total_questions=total,
        percentage=percentage,
        certificate_id=cert_id,
        results_summary=json.dumps({"correct_question_ids": correct_ids}),
    )
    db.add(attempt)

    session.quiz_completed = True
    session.updated_at = datetime.now(timezone.utc)
    await db.flush()

    return {
        "score": score,
        "total": total,
        "percentage": percentage,
        "certificate_id": cert_id,
        "explanations": results,
    }


async def get_quiz_result(db: AsyncSession, session_token: str) -> QuizAttempt | None:
    result = await db.execute(
        select(QuizAttempt).where(QuizAttempt.session_token == session_token)
    )
    return result.scalar_one_or_none()
