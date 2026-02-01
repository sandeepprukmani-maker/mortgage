@echo off
REM Start local development environment (Windows wrapper)
REM Runs the PowerShell script with proper execution policy

cd /d "%~dp0"
powershell -ExecutionPolicy Bypass -File "%~dp0start_local.ps1"
pause
