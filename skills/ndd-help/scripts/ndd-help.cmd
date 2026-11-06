@echo off
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0print-help.ps1"
exit /b %errorlevel%
