@echo off
title Attendance System Launcher

echo Starting local server...
start "" python main.py

timeout /t  >nul

echo Starting ngrok tunnel...
start "" ngrok http 5000

echo.
echo System is running. You can close this window when finished.
pause