@echo off
REM Stop local development environment (Windows wrapper)
REM Runs the PowerShell script with proper execution policy

cd /d "%~dp0"
powershell -ExecutionPolicy Bypass -File "%~dp0stop_local.ps1"
pause
