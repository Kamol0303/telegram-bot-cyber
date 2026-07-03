"""Admin API routes with JWT authentication."""

from fastapi import APIRouter, Depends, Header, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.schemas import AdminLoginRequest, AdminStatsResponse
from backend.services.admin_service import (
    create_admin_token,
    get_platform_stats,
    log_admin_action,
    verify_admin_credentials,
    verify_admin_token,
)

router = APIRouter(prefix="/api/admin", tags=["admin"])


async def require_admin(authorization: str = Header(None)) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing authorization")
    token = authorization.split(" ", 1)[1]
    username = verify_admin_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return username


@router.post("/login")
async def admin_login(
    body: AdminLoginRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    if not verify_admin_credentials(body.username, body.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_admin_token(body.username)
    client_ip = request.client.host if request.client else None
    await log_admin_action(db, "login", f"Admin {body.username} logged in", client_ip)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/stats", response_model=AdminStatsResponse)
async def admin_stats(
    db: AsyncSession = Depends(get_db),
    admin: str = Depends(require_admin),
):
    stats = await get_platform_stats(db)
    return AdminStatsResponse(**stats)
