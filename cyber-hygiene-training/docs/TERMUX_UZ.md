# Termux orqali ishga tushirish (O'zbekcha)

Bu qo'llanma **Android telefonda Termux** orqali Cyber Hygiene Awareness Training platformasini ishga tushirish uchun.

> **Eslatma:** Bu platforma faqat **ta'lim maqsadida**. Haqiqiy to'lov kartalari, parollar yoki SMS kodlari yig'ilmaydi.

---

## Talablar

- Android telefon
- [Termux](https://f-droid.org/en/packages/com.termux/) (F-Droid dan o'rnating)
- Internet ulanishi
- Telegram Bot Token ([@BotFather](https://t.me/BotFather) dan)

---

## 1-qadam: Termux o'rnatish

1. F-Droid dan **Termux** ilovasini o'rnating (Google Play dagi Termux eskirgan — F-Droid dan oling)
2. Termux ni oching

---

## 2-qadam: Loyihani yuklab olish

```bash
pkg update && pkg install git -y
cd ~
git clone https://github.com/Kamol0303/telegram-bot-cyber.git
cd telegram-bot-cyber/cyber-hygiene-training
```

Agar allaqachon yuklab olingan bo'lsa:

```bash
cd ~/telegram-bot-cyber/cyber-hygiene-training
git pull
```

---

## 3-qadam: Avtomatik o'rnatish

```bash
bash scripts/termux-setup.sh
```

Bu skript quyidagilarni bajaradi:
- Python, pip, rust va boshqa kerakli paketlarni o'rnatadi
- Virtual muhit (`venv`) yaratadi
- Kutubxonalarni o'rnatadi
- `.env` faylini yaratadi

O'rnatish 5–15 daqiqa davom etishi mumkin (internet tezligiga qarab).

---

## 4-qadam: Sozlash (.env)

```bash
nano .env
```

Quyidagi qatorlarni o'zgartiring:

```env
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
SECRET_KEY=uzun-tasodifiy-kalit-bu-yerga
ADMIN_PASSWORD=kuchli-admin-parol
BASE_URL=http://127.0.0.1:8000
```

### BASE_URL qanday tanlanadi?

| Holat | BASE_URL |
|-------|----------|
| Hammasi shu telefonda | `http://127.0.0.1:8000` |
| Wi-Fi orqali boshqa qurilmalar | `http://TELEFON_IP:8000` |
| Internetdan kirish (ngrok) | `https://sizning-url.ngrok.io` |

Telefon IP manzilini bilish:

```bash
ip route get 1 | awk '{print $7; exit}'
```

`nano` da saqlash: `Ctrl+O`, Enter, chiqish: `Ctrl+X`

---

## 5-qadam: Ishga tushirish

```bash
bash scripts/start-termux.sh
```

Muvaffaqiyatli bo'lsa, quyidagicha xabar chiqadi:

```
[+] Platforma ishga tushdi!

  Telefon brauzeri:  http://127.0.0.1:8000
  Admin panel:       http://127.0.0.1:8000/admin
```

---

## 6-qadam: Tekshirish

### Brauzerda (telefonda)

Termux da:

```bash
termux-open-url http://127.0.0.1:8000
```

Yoki brauzerda `http://127.0.0.1:8000` manzilini oching.

### Telegram botda

1. BotFather da yaratgan botingizni oching
2. `/start` yuboring
3. Ism va telefon raqamini kiriting (simulyatsiya uchun)
4. **"Continue Simulation"** tugmasini bosing

---

## To'xtatish

```bash
bash scripts/stop-termux.sh
```

---

## Muammolarni hal qilish

### "Backend ishga tushmadi"

```bash
cat data/backend.log
```

Ko'pincha port band bo'ladi. To'xtating va qayta ishga tushiring:

```bash
bash scripts/stop-termux.sh
bash scripts/start-termux.sh
```

### "Bot ishga tushmadi"

```bash
cat data/bot.log
```

- `TELEGRAM_BOT_TOKEN` to'g'ri ekanligini tekshiring
- `BASE_URL` backend manziliga mos kelishi kerak
- Internet ulanishi borligini tekshiring

### Kutubxona o'rnatishda xato

```bash
pkg install rust libffi openssl -y
pip install --upgrade pip
pip install -r requirements.txt
```

### Termux yopilganda server to'xtaydi

Termux fon rejimida ishlashi uchun **Termux:Boot** yoki **wake lock** ishlatishingiz mumkin:

```bash
pkg install termux-api
termux-wake-lock
bash scripts/start-termux.sh
```

---

## Qo'lda ishga tushirish (2 ta oyna)

Agar skript ishlamasa, ikkita Termux oynasida:

**Oyna 1 — Backend:**
```bash
cd ~/telegram-bot-cyber/cyber-hygiene-training
source venv/bin/activate
export PYTHONPATH=$(pwd)
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

**Oyna 2 — Bot** (yangi Termux sessiyasi: uzoq bosib → "New session"):
```bash
cd ~/telegram-bot-cyber/cyber-hygiene-training
source venv/bin/activate
export PYTHONPATH=$(pwd)
python -m bot.main
```

---

## Linux / kompyuterda ishga tushirish

Termux emas, oddiy kompyuterda:

```bash
cd cyber-hygiene-training
cp .env.example .env
# .env ni tahrirlang
pip install -r requirements.txt
export PYTHONPATH=$(pwd)
bash start.sh
```

Yoki Docker:

```bash
docker compose up --build
```

Batafsil: [INSTALLATION.md](INSTALLATION.md)

---

## Foydali havolalar

| Sahifa | Manzil |
|--------|--------|
| Bosh sahifa (simulyatsiya) | `http://127.0.0.1:8000/` |
| To'lov simulyatsiyasi | `http://127.0.0.1:8000/simulation` |
| Ogohlantirish | `http://127.0.0.1:8000/reveal` |
| O'quv materiallari | `http://127.0.0.1:8000/learn` |
| Test | `http://127.0.0.1:8000/quiz` |
| Sertifikat | `http://127.0.0.1:8000/certificate` |
| Admin | `http://127.0.0.1:8000/admin` |
