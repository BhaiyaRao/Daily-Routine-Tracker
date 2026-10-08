@echo off
title Daily Routine Tracker - College Project Launcher
color 0A

echo =====================================================================
echo          DAILY ROUTINE TRACKER - COLLEGE PROJECT LAUNCHER
echo =====================================================================
echo.
echo [1/2] Checking Python environment...

where py >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set PY_CMD=py
) else (
    where python >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        set PY_CMD=python
    ) else (
        echo [ERROR] Python is not found on your system!
        echo Please install Python 3.10+ from https://www.python.org/
        pause
        exit /b 1
    )
)

echo Python found! Using: %PY_CMD%
echo.
echo [2/2] Starting Streamlit Application...
echo.
echo Application will open automatically in your default browser...
echo (Press CTRL + C in this window to stop the server)
echo =====================================================================

%PY_CMD% -m streamlit run app.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [NOTICE] Streamlit encountered an issue or was closed.
    pause
)
