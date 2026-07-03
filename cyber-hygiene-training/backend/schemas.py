"""Pydantic schemas for API request/response validation."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class SessionCreateRequest(BaseModel):
    """Create anonymous training session — no PII accepted."""

    telegram_user_id: Optional[int] = Field(
        None, description="Telegram user ID; hashed before storage"
    )


class SessionCreateResponse(BaseModel):
    token: str
    simulation_url: str
    expires_at: datetime


class SessionProgressUpdate(BaseModel):
    """Update non-sensitive progress flags only."""

    landing_viewed: Optional[bool] = None
    simulation_completed: Optional[bool] = None
    reveal_viewed: Optional[bool] = None
    learning_viewed: Optional[bool] = None


class SessionStatusResponse(BaseModel):
    token: str
    valid: bool
    landing_viewed: bool
    simulation_completed: bool
    reveal_viewed: bool
    learning_viewed: bool
    quiz_completed: bool
    expires_at: datetime


class QuizQuestion(BaseModel):
    id: int
    question: str
    options: List[str]
    # Correct answer index NOT sent to client until after submission


class QuizSubmitRequest(BaseModel):
    """Submit quiz answers — only question IDs and selected option indices."""

    session_token: str
    answers: Dict[str, int] = Field(
        ..., description="Map of question_id (string) to selected option index"
    )
    display_name: Optional[str] = Field(
        None, description="Optional name for certificate — stays in request only"
    )


class QuizSubmitResponse(BaseModel):
    score: int
    total: int
    percentage: float
    certificate_id: str
    explanations: List[Dict[str, Any]]


class AdminLoginRequest(BaseModel):
    username: str
    password: str


class AdminStatsResponse(BaseModel):
    total_sessions: int
    completed_simulations: int
    completed_quizzes: int
    average_quiz_score: float
    recent_sessions: List[Dict]
