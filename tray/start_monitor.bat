@echo off
REM Start TNT Monitor in system tray (no console window)
cd /d "%~dp0.."
start "" "D:\TNT_AI\venv\Scripts\pythonw.exe" "tray\monitor_tray.py"
exit
