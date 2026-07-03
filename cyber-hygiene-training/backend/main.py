"""
FastAPI application entry point.
Cyber Hygiene Awareness Training Platform — educational simulation only.
"""

import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.config import get_settings
from backend.database import init_db
from backend.routers import admin_router, api_router, pages_router

settings = get_settings()

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title=settings.app_name,
    description=(
        "Educational cybersecurity awareness training platform. "
        "Never collects real payment cards, OTP codes, or passwords."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH"],
    allow_headers=["Authorization", "Content-Type"],
)

FRONTEND_STATIC = Path(__file__).resolve().parent.parent / "frontend" / "static"
app.mount("/static", StaticFiles(directory=str(FRONTEND_STATIC)), name="static")

app.include_router(api_router)
app.include_router(admin_router)
app.include_router(pages_router)


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "platform": "Cyber Hygiene Awareness Training",
        "educational_only": True,
    }
