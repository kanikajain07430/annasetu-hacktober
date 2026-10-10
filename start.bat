@echo off
title AnnaSetu Platform Launcher
echo =========================================================
echo    🌾 AnnaSetu Smart AgTech & Surplus Redistribution
echo =========================================================
echo.
echo [1/2] Starting Backend Service on http://127.0.0.1:8000 ...
start "" http://127.0.0.1:8000
cd /d "%~dp0backend"
py run.py
pause
