"""API route handlers."""

from backend.routers.api import router as api_router
from backend.routers.admin import router as admin_router
from backend.routers.pages import router as pages_router

__all__ = ["api_router", "admin_router", "pages_router"]
