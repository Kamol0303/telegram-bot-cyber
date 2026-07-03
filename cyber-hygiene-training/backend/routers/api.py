"""
Public API routes for session and quiz management.
SECURITY: These endpoints never accept card numbers, CVV, OTP, or passwords.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.config import get_settings
from backend.database import get_db
from backend.schemas import (
    QuizSubmitRequest,
    QuizSubmitResponse,
    SessionCreateRequest,
    SessionCreateResponse,
    SessionProgressUpdate,
    SessionStatusResponse,
)
from backend.services.quiz_data import get_questions_for_client
from backend.services.quiz_service import submit_quiz
from backend.services.session_service import (
    create_session,
    get_session_by_token,
    is_session_valid,
    update_session_progress,
)

router = APIRouter(prefix="/api", tags=["api"])
settings = get_settings()


@router.post("/sessions", response_model=SessionCreateResponse)
async def create_training_session(
    body: SessionCreateRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Create anonymous session for bot users.
    No personal data is stored — only a hashed Telegram ID for analytics.
    """
    session = await create_session(db, body.telegram_user_id)
    return SessionCreateResponse(
        token=session.token,
        simulation_url=f"{settings.base_url}/?token={session.token}",
        expires_at=session.expires_at,
    )


@router.get("/sessions/{token}", response_model=SessionStatusResponse)
async def get_session_status(token: str, db: AsyncSession = Depends(get_db)):
    session = await get_session_by_token(db, token)
    valid = is_session_valid(session)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return SessionStatusResponse(
        token=token,
        valid=valid,
        landing_viewed=session.landing_viewed,
        simulation_completed=session.simulation_completed,
        reveal_viewed=session.reveal_viewed,
        learning_viewed=session.learning_viewed,
        quiz_completed=session.quiz_completed,
        expires_at=session.expires_at,
    )


@router.patch("/sessions/{token}/progress")
async def update_progress(
    token: str,
    body: SessionProgressUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update non-sensitive progress flags only."""
    session = await update_session_progress(
        db,
        token,
        landing_viewed=body.landing_viewed,
        simulation_completed=body.simulation_completed,
        reveal_viewed=body.reveal_viewed,
        learning_viewed=body.learning_viewed,
    )
    if not session:
        raise HTTPException(status_code=404, detail="Session not found or expired")
    return {"status": "ok"}


@router.get("/quiz/questions")
async def get_quiz_questions():
    """Return quiz questions without correct answers."""
    return {"questions": get_questions_for_client()}


@router.post("/quiz/submit", response_model=QuizSubmitResponse)
async def submit_quiz_answers(
    body: QuizSubmitRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Submit quiz answers. Only question IDs and option indices accepted.
    Rejects any attempt to submit sensitive field names.
    """
    forbidden_keys = {"card", "cvv", "otp", "password", "pin", "sms"}
    for key in body.answers.keys():
        if any(f in key.lower() for f in forbidden_keys):
            raise HTTPException(
                status_code=400,
                detail="Sensitive data cannot be submitted to this API.",
            )

    result = await submit_quiz(db, body.session_token, body.answers)
    if not result:
        raise HTTPException(status_code=400, detail="Invalid session or quiz already completed")
    return QuizSubmitResponse(**result)
