@echo off
REM Cyber Hygiene Training — Windows ishga tushirish
cd /d "%~dp0"
python scripts\launcher.py start %*
if errorlevel 1 (
    py -3 scripts\launcher.py start %*
)
pause
