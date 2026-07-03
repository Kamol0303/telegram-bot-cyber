<p align="center">
<b>🛡️ Cyber Hygiene Awareness Training Platform</b>
</p>

> Ta'lim maqsadidagi phishing simulyatsiyasi — Telegram bot + Web platforma

---

## ⚡ Tezkor ishga tushirish

```bash
cd ~/telegram-bot-cyber
sudo chown -R $USER:$USER .git    # git xato bo'lsa
git pull origin main
bash setup.sh
nano cyber-hygiene-training/.env   # TELEGRAM_BOT_TOKEN kiriting
bash scripts/start-training.sh
```

**To'xtatish:** `bash scripts/stop-training.sh`

📖 To'liq qo'llanma: [QUICKSTART_UZ.md](QUICKSTART_UZ.md)

---

## Papka tuzilmasi

```
telegram-bot-cyber/
├── setup.sh / start.sh / stop.sh     ← shu buyruqlardan foydalaning
├── scripts/start-training.sh
└── cyber-hygiene-training/           ← asosiy kod
```

---

## Platformalar

| OS | O'rnatish | Ishga tushirish |
|----|-----------|-----------------|
| Kali/Linux | `bash setup.sh` | `bash scripts/start-training.sh` |
| Termux | `bash setup.sh` | `bash scripts/start-training.sh` |
| Windows | `cyber-hygiene-training\setup.bat` | `start.bat` |

---

## Eski ZPhisher

Eski zphisher hali `zphisher.sh` da mavjud. Yangi ta'lim platformasi — `cyber-hygiene-training/` papkasida.
