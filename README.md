<p align="center">
<b>🛡️ Cyber Hygiene Awareness Training Platform</b>
</p>

> Ta'lim maqsadidagi phishing simulyatsiyasi — Telegram bot + Web platforma

---

## ⚡ Tezkor ishga tushirish (Kali — git ishlamasa ham)

**Bitta buyruq** (tavsiya etiladi):

```bash
curl -fsSL https://raw.githubusercontent.com/Kamol0303/telegram-bot-cyber/main/install-kali.sh | bash
```

Yoki lokal:

```bash
cd ~/telegram-bot-cyber
bash install-kali.sh
```

---

## Qo'lda (git ishlasa)

```bash
cd ~/telegram-bot-cyber
sudo chown -R $USER:$USER .git
git pull origin main
bash setup.sh
nano cyber-hygiene-training/.env
bash telegram.sh
```

**To'xtatish:** `bash scripts/stop-training.sh`

📖 To'liq qo'llanma: [QUICKSTART_UZ.md](QUICKSTART_UZ.md)

---

## Papka tuzilmasi

```
telegram-bot-cyber/
├── setup.sh / start.sh / stop.sh / telegram.sh  ← shu buyruqlardan foydalaning
├── scripts/start-training.sh
└── cyber-hygiene-training/           ← asosiy kod
```

---

## Platformalar

| OS | O'rnatish | Ishga tushirish |
|----|-----------|-----------------|
| Kali/Linux | `bash setup.sh` | `bash telegram.sh` (Cloudflared avto) |
| Termux | `bash setup.sh` | `bash scripts/start-training.sh` |
| Windows | `cyber-hygiene-training\setup.bat` | `start.bat` |

---

## Eski ZPhisher

Eski zphisher hali `zphisher.sh` da mavjud. Yangi ta'lim platformasi — `cyber-hygiene-training/` papkasida.
