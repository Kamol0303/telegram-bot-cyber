# Cyber Hygiene Training — Tezkor boshlash (Kali / Linux / Termux / Windows)

## ⚠️ Muhim: To'g'ri papka

Loyiha **ikki qavatli** tuzilmada:

```
~/telegram-bot-cyber/              ← git repo ildizi (siz shu yerdasiz)
├── start.sh                       ← ISHLATING
├── stop.sh
├── setup.sh
├── scripts/
│   ├── start-training.sh          ← ISHLATING
│   └── stop-training.sh
└── cyber-hygiene-training/        ← asosiy loyiha kodi
    ├── start.sh
    ├── backend/
    ├── bot/
    └── frontend/
```

---

## Git xatosi: `Permission denied`

Agar `git pull` da xato chiqsa:

```bash
cd ~/telegram-bot-cyber
sudo chown -R $USER:$USER .git
git pull origin main
```

Agar yordam bermasa — qayta klonlang:

```bash
cd ~/Desktop
mv telegram-bot-cyber telegram-bot-cyber-old
git clone https://github.com/Kamol0303/telegram-bot-cyber.git
cd telegram-bot-cyber
```

---

## Kali Linux — to'liq o'rnatish

```bash
# 1. Tizim paketlari
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git curl openssh-client unzip

# 2. Loyiha papkasi
cd ~/telegram-bot-cyber

# 3. Git muammosini tuzatish (agar kerak bo'lsa)
sudo chown -R $USER:$USER .git
git pull origin main

# 4. O'rnatish
bash setup.sh

# 5. Sozlash
nano cyber-hygiene-training/.env
```

`.env` ichida:
```env
TELEGRAM_BOT_TOKEN=botfather-dan-token
NGROK_AUTHTOKEN=ngrok-dan-token
SECRET_KEY=uzun-tasodifiy-kalit
ADMIN_PASSWORD=admin-parol
```

```bash
# 6. Ishga tushirish
bash scripts/start-training.sh

# 7. To'xtatish
bash scripts/stop-training.sh
```

---

## Barcha platformalar — qisqa buyruqlar

| Harakat | Buyruq (repo ildizidan) |
|---------|-------------------------|
| O'rnatish | `bash setup.sh` |
| Ishga tushirish | `bash scripts/start-training.sh` |
| To'xtatish | `bash scripts/stop-training.sh` |
| Holat | `cd cyber-hygiene-training && python3 scripts/launcher.py status` |

Windows: `setup.bat`, `start.bat`, `stop.bat` (`cyber-hygiene-training` ichida)

---

## Tekshirish

```bash
curl http://127.0.0.1:8000/health
```

Telegram botga: `/start`

Batafsil: `cyber-hygiene-training/docs/CROSS_PLATFORM_UZ.md`
