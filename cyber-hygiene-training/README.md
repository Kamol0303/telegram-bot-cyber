# Cyber Hygiene Awareness Training Platform

A complete **educational cybersecurity awareness training platform** that simulates common online scam patterns to teach users how to recognize and avoid phishing, fake lotteries, OTP theft, and social engineering attacks.

> **IMPORTANT:** This platform is for **education only**. It never collects real payment cards, passwords, SMS codes, or personal financial information. All sensitive inputs are simulated locally and discarded immediately.

## Project Flow

```
Telegram Bot → Educational Landing Page → Cyber Awareness Simulation → Explanation → Learning → Quiz → Certificate
```

## Features

- **Telegram Bot** (Aiogram 3) — Welcomes users with an intentionally suspicious prize message
- **Fake Lottery Landing Page** — Contains subtle warning signs (poor grammar, suspicious domain, countdown timer)
- **Payment Simulation** — Rejects real card numbers (Luhn validation), generates random training OTP codes
- **Dramatic Reveal** — Transitions to cybersecurity awareness message
- **Learning Section** — Covers phishing, scams, social engineering, and more
- **Knowledge Quiz** — 10 interactive questions with explanations
- **Completion Certificate** — Issued after quiz completion
- **Admin Panel** — Anonymous analytics dashboard

## Quick Start (barcha platformalar)

| Platforma | O'rnatish | Ishga tushirish |
|-----------|-----------|-----------------|
| **Windows** | `setup.bat` | `start.bat` |
| **Linux** | `bash setup.sh` | `bash start.sh` |
| **Termux** | `bash setup.sh` | `bash start.sh` |
| **macOS** | `bash setup.sh` | `bash start.sh` |

```bash
# Yoki Python launcher (har qanday OS):
python scripts/launcher.py setup
python scripts/launcher.py start
python scripts/launcher.py stop
```

`.env` ni sozlang: `TELEGRAM_BOT_TOKEN`, `NGROK_AUTHTOKEN`, `SECRET_KEY`

Batafsil: **[Cross-Platform qo'llanma (O'zbekcha)](docs/CROSS_PLATFORM_UZ.md)**

Docker:

```bash
docker compose up --build
```

## URLs

| URL | Description |
|-----|-------------|
| `http://localhost:8000/` | Scam simulation landing page |
| `http://localhost:8000/simulation` | Payment/OTP simulation |
| `http://localhost:8000/reveal` | Cybersecurity reveal |
| `http://localhost:8000/learn` | Educational content |
| `http://localhost:8000/quiz` | Knowledge quiz |
| `http://localhost:8000/certificate` | Completion certificate |
| `http://localhost:8000/admin` | Admin dashboard |
| `http://localhost:8000/health` | Health check |

## Security Principles

- Real payment card numbers are **rejected** client-side via Luhn algorithm
- OTP codes are **randomly generated** training codes — real banking codes are never accepted
- Name/phone from bot are passed via **URL fragment** (never sent to server)
- Server stores only **anonymous session tokens** and quiz scores
- Clear **educational disclaimer** shown only at the final reveal step

## Documentation

- [Cross-Platform Guide (O'zbekcha)](docs/CROSS_PLATFORM_UZ.md)
- [Installation Guide](docs/INSTALLATION.md)
- [Termux Guide (O'zbekcha)](docs/TERMUX_UZ.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Security Review](docs/SECURITY_REVIEW.md)
- [Threat Model](docs/THREAT_MODEL.md)

## Tech Stack

- **Backend:** FastAPI, SQLAlchemy, SQLite
- **Bot:** Aiogram 3
- **Frontend:** HTML, CSS, JavaScript, Bootstrap 5
- **Auth:** JWT (admin panel)

## License

Educational use only. See LICENSE in repository root.
