# Deployment Guide

## Production Checklist

- [ ] Set strong `SECRET_KEY` (48+ random characters)
- [ ] Change default `ADMIN_PASSWORD`
- [ ] Set `DEBUG=false`
- [ ] Configure HTTPS with valid TLS certificate
- [ ] Set `BASE_URL` to production HTTPS URL
- [ ] Restrict `CORS_ORIGINS` to your domain
- [ ] Back up SQLite database regularly
- [ ] Configure firewall (expose only 443/80)

## Docker Deployment (Recommended)

### 1. Prepare Server

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install -y docker.io docker-compose-plugin
sudo usermod -aG docker $USER
```

### 2. Deploy

```bash
git clone <repository-url>
cd cyber-hygiene-training
cp .env.example .env
# Edit .env with production values
docker compose up --build -d
```

### 3. Reverse Proxy (Nginx)

```nginx
server {
    listen 443 ssl http2;
    server_name training.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/training.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/training.yourdomain.com/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Obtain TLS certificate:
```bash
sudo certbot --nginx -d training.yourdomain.com
```

## Manual Deployment

### Using systemd

**`/etc/systemd/system/cyber-training-api.service`:**
```ini
[Unit]
Description=Cyber Hygiene Training API
After=network.target

[Service]
User=www-data
WorkingDirectory=/opt/cyber-hygiene-training
Environment=PYTHONPATH=/opt/cyber-hygiene-training
EnvironmentFile=/opt/cyber-hygiene-training/.env
ExecStart=/opt/cyber-hygiene-training/venv/bin/uvicorn backend.main:app --host 127.0.0.1 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

**`/etc/systemd/system/cyber-training-bot.service`:**
```ini
[Unit]
Description=Cyber Hygiene Training Telegram Bot
After=network.target cyber-training-api.service

[Service]
User=www-data
WorkingDirectory=/opt/cyber-hygiene-training
Environment=PYTHONPATH=/opt/cyber-hygiene-training
EnvironmentFile=/opt/cyber-hygiene-training/.env
ExecStart=/opt/cyber-hygiene-training/venv/bin/python -m bot.main
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable --now cyber-training-api cyber-training-bot
```

## Environment Variables (Production)

```env
APP_ENV=production
DEBUG=false
SECRET_KEY=<generated-48-char-secret>
BASE_URL=https://training.yourdomain.com
TELEGRAM_BOT_TOKEN=<your-bot-token>
ADMIN_USERNAME=admin
ADMIN_PASSWORD=<strong-password>
CORS_ORIGINS=https://training.yourdomain.com
DATABASE_URL=sqlite+aiosqlite:///./data/training.db
```

## Database Backup

```bash
# Cron job — daily backup at 2 AM
0 2 * * * cp /opt/cyber-hygiene-training/data/training.db /backups/training-$(date +\%Y\%m\%d).db
```

## Monitoring

Health check endpoint:
```bash
curl -f https://training.yourdomain.com/health
```

Monitor with your preferred tool (Uptime Kuma, Datadog, etc.).

## Scaling Notes

This platform is designed for training workloads with moderate traffic. For high-volume deployments:

- Migrate SQLite to PostgreSQL
- Run multiple uvicorn workers behind a load balancer
- Use Redis for bot FSM state instead of in-memory storage

## Updating

```bash
cd /opt/cyber-hygiene-training
git pull
docker compose up --build -d
# or: sudo systemctl restart cyber-training-api cyber-training-bot
```
