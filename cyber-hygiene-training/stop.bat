@echo off
REM Cyber Hygiene Training — Windows to'xtatish
cd /d "%~dp0"
python scripts\launcher.py stop 2>nul || py -3 scripts\launcher.py stop
echo Tayyor.
pause
