@echo off
cd /d "%~dp0"
powershell.exe -ExecutionPolicy Bypass -File "%~dp0KHOI_DONG_WIDGET.ps1"
exit /b 0
