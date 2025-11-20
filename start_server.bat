@echo off
title Attendance System Launcher

REM Navigate to your project folder
cd C:\Users\DNCMES\Desktop\AttenTrack\ATTENTRACK

REM Check if venv folder exists, if so activate it
IF EXIST ..\venv\Scripts\Activate.bat (
    REM If virtual environment exists, activate it
    call ..\venv\Scripts\Activate.bat
) ELSE (
    echo No virtual environment found. Skipping activation.
)

REM Start Flask in a new window
start "" python main.py

REM Wait for Flask to start (10 seconds)
timeout /t 10 >nul

REM Start ngrok in a new window
start "" ngrok http 5000

REM Display info message
echo.
echo System is running. Keep both Flask and ngrok windows open.
pause
