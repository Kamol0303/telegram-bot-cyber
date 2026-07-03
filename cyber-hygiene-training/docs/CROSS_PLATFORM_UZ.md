# Cross-platform ishga tushirish (O'zbekcha)

Bitta kod bazasi — **Termux**, **Linux**, **Windows** va **macOS** da ishlaydi.

---

## Tezkor boshlash

| Platforma | O'rnatish | Ishga tushirish | To'xtatish |
|-----------|-----------|-----------------|------------|
| **Windows** | `setup.bat` | `start.bat` | `stop.bat` |
| **Linux** | `bash setup.sh` | `bash start.sh` | `bash stop.sh` |
| **Termux** | `bash setup.sh` | `bash start.sh` | `bash stop.sh` |
| **macOS** | `bash setup.sh` | `bash start.sh` | `bash stop.sh` |

Yoki har qanday platformada:

```bash
python scripts/launcher.py setup
python scripts/launcher.py start
python scripts/launcher.py stop
python scripts/launcher.py status
```

---

## Windows

### Talablar
- Python 3.11+ — https://python.org (o'rnatishda **Add to PATH** belgilang)
- Git (ixtiyoriy)

### Qadamlar

1. Loyihani yuklab oling:
```cmd
git clone https://github.com/Kamol0303/telegram-bot-cyber.git
cd telegram-bot-cyber\cyber-hygiene-training
```

2. O'rnating:
```cmd
setup.bat
```

3. `.env` faylini tahrirlang (Notepad):
```env
TELEGRAM_BOT_TOKEN=botfather-token
NGROK_AUTHTOKEN=ngrok-token
SECRET_KEY=tasodifiy-kalit
ADMIN_PASSWORD=admin-parol
```

4. Ishga tushiring:
```cmd
start.bat
```

Tunnel menyusidan **2 (Ngrok)** ni tanlang.

5. To'xtatish:
```cmd
stop.bat
```

### Windows muammolari

| Muammo | Yechim |
|--------|--------|
| `python` topilmadi | `py -3 scripts/launcher.py setup` |
| Ngrok ishlamaydi | https://ngrok.com/download dan o'rnating |
| SSH yo'q | Serveo/localhost.run o'rniga Ngrok ishlating |
| Firewall | Port 8000 ga ruxsat bering |

---

## Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git curl openssh-client unzip

git clone https://github.com/Kamol0303/telegram-bot-cyber.git
cd telegram-bot-cyber/cyber-hygiene-training

bash setup.sh
nano .env
bash start.sh
```

Tunnel: `2` (Ngrok) yoki `1` (mahalliy Wi-Fi)

---

## Termux (Android)

```bash
pkg update && pkg install -y git python
cd ~
git clone https://github.com/Kamol0303/telegram-bot-cyber.git
cd telegram-bot-cyber/cyber-hygiene-training

bash setup.sh
nano .env
bash start.sh
```

> `setup.sh` Termux da avtomatik `pkg install` qiladi (openssh, rust, va h.k.)

Fon rejimida ishlashi uchun:
```bash
termux-wake-lock
bash start.sh
```

---

## Tunnel turlari (barcha platformalar)

| # | Turi | Qachon ishlatiladi |
|---|------|-------------------|
| 1 | LocalHost | Bir xil Wi-Fi tarmog'i |
| 2 | Ngrok | Internetdan kirish (tavsiya) |
| 3 | Serveo | SSH bor bo'lsa |
| 4 | Localhost.run | SSH bor bo'lsa |
| 5 | Yo'q | Faqat shu qurilmada test |

Tunnel tanlamasdan ishga tushirish:
```bash
python scripts/launcher.py start --tunnel 2
```

---

## Fayl tuzilmasi

```
cyber-hygiene-training/
├── start.bat / stop.bat / setup.bat   ← Windows
├── start.sh  / stop.sh  / setup.sh    ← Linux/Termux/macOS
└── scripts/
    ├── launcher.py        ← asosiy (barcha OS)
    ├── platform_util.py
    └── tunnel_manager.py
```

---

## Tekshirish

```bash
python scripts/launcher.py status
```

Yoki brauzerda: `http://127.0.0.1:8000/health`

Telegram: `/start` va `/status`
