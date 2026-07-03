# Installation Guide

## Prerequisites

- Python 3.11 or higher
- pip
- A Telegram Bot Token from [@BotFather](https://t.me/BotFather)
- (Optional) Docker and Docker Compose

## Step 1: Clone and Navigate

```bash
git clone <repository-url>
cd cyber-hygiene-training
```

## Step 2: Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your values:

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | Long random string for JWT signing | Yes |
| `TELEGRAM_BOT_TOKEN` | Token from BotFather | Yes (for bot) |
| `BASE_URL` | Public URL of your backend | Yes |
| `ADMIN_USERNAME` | Admin panel username | Yes |
| `ADMIN_PASSWORD` | Admin panel password | Yes |
| `DATABASE_URL` | SQLite connection string | No (default works) |

Generate a secure secret key:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(48))"
```

## Step 3: Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Step 4: Create Data Directory

```bash
mkdir -p data
```

The SQLite database is created automatically on first startup.

## Step 5: Start Services

### Option A: Manual (Development)

**Terminal 1 — Backend:**
```bash
export PYTHONPATH=$(pwd)
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 — Telegram Bot:**
```bash
export PYTHONPATH=$(pwd)
python -m bot.main
```

### Option B: Start Script

```bash
chmod +x start.sh
./start.sh
```

### Option C: Docker

```bash
docker compose up --build -d
```

## Step 6: Configure Telegram Bot

1. Open [@BotFather](https://t.me/BotFather) in Telegram
2. Create a new bot with `/newbot`
3. Copy the token to `TELEGRAM_BOT_TOKEN` in `.env`
4. Set `BASE_URL` to your public URL (use ngrok for local testing)

### Local Testing with ngrok

```bash
ngrok http 8000
# Set BASE_URL=https://your-ngrok-url.ngrok.io in .env
```

## Step 7: Verify Installation

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "platform": "Cyber Hygiene Awareness Training",
  "educational_only": true
}
```

## Step 8: Test the Flow

1. Open your Telegram bot and send `/start`
2. Enter a simulated name and phone number
3. Click "Continue Simulation"
4. Complete the landing page and payment simulation
5. View the reveal, learning section, and quiz
6. Access admin panel at `/admin`

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Bot can't reach backend | Ensure `BASE_URL` is accessible from the bot process |
| Database errors | Check `data/` directory permissions |
| Import errors | Set `PYTHONPATH` to project root |
| CORS errors | Add your domain to `CORS_ORIGINS` in `.env` |

## Termux (Android)

For running on Android phones with Termux, see the dedicated guide:

**[Termux Guide (O'zbekcha)](TERMUX_UZ.md)**

Quick commands:

```bash
bash scripts/termux-setup.sh
nano .env
bash scripts/start-termux.sh
```
