@echo off
chcp 65001 > nul
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1
title WOW English Bot & Mini App 24/7
echo ======================================================
echo 🚀 Запуск English Learning Bot & Telegram Mini App...
echo ======================================================
cd /d "%~dp0"
python run.py
pause
