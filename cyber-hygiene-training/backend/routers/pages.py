"""HTML page routes serving the training frontend."""

from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent / "frontend"
templates = Jinja2Templates(directory=str(FRONTEND_DIR / "templates"))

router = APIRouter(tags=["pages"])


@router.get("/", response_class=HTMLResponse)
async def landing_page(request: Request):
    return templates.TemplateResponse("landing.html", {"request": request})


@router.get("/simulation", response_class=HTMLResponse)
async def simulation_page(request: Request):
    return templates.TemplateResponse("simulation.html", {"request": request})


@router.get("/reveal", response_class=HTMLResponse)
async def reveal_page(request: Request):
    return templates.TemplateResponse("reveal.html", {"request": request})


@router.get("/learn", response_class=HTMLResponse)
async def learn_page(request: Request):
    return templates.TemplateResponse("learn.html", {"request": request})


@router.get("/quiz", response_class=HTMLResponse)
async def quiz_page(request: Request):
    return templates.TemplateResponse("quiz.html", {"request": request})


@router.get("/certificate", response_class=HTMLResponse)
async def certificate_page(request: Request):
    return templates.TemplateResponse("certificate.html", {"request": request})


@router.get("/admin", response_class=HTMLResponse)
async def admin_page(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})
