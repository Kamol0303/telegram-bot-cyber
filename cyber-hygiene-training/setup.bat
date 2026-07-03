@echo off
REM Cyber Hygiene Training — Windows o'rnatish
cd /d "%~dp0"
echo Cyber Hygiene Training - Windows o'rnatish
python scripts\launcher.py setup 2>nul || py -3 scripts\launcher.py setup
if not exist .env copy .env.example .env
echo.
echo Keyingi qadam: .env faylini tahrirlang va start.bat ni ishga tushiring
pause
