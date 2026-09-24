@echo off
chcp 65001 > nul
title Push to GitHub
cd /d "%~dp0"
echo ========================================================
echo 🚀 Отправка проекта в GitHub: wow-english-bot...
echo ========================================================
"C:\PROJECTS\bin\git\cmd\git.exe" remote set-url origin https://github.com/omelescenko-translator-bot/wow-english-bot.git
"C:\PROJECTS\bin\git\cmd\git.exe" branch -M main
"C:\PROJECTS\bin\git\cmd\git.exe" push -u origin main
echo.
echo ✅ Если всё прошло успешно, нажмите любую клавишу для закрытия.
pause
