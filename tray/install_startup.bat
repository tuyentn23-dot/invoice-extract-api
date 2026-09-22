@echo off
REM Add TNT Monitor to Windows startup
set SHORTCUT=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\TNT-Monitor.lnk
set TARGET=D:\TNT_AI\venv\Scripts\pythonw.exe
set ARGS="D:\TNT_AI\venture_foundry\rapidapi_extract\tray\monitor_tray.py"
set WORKDIR=D:\TNT_AI\venture_foundry\rapidapi_extract

powershell -NoProfile -Command ^
  "$ws = New-Object -ComObject WScript.Shell; ^
   $sc = $ws.CreateShortcut('%SHORTCUT%'); ^
   $sc.TargetPath = '%TARGET%'; ^
   $sc.Arguments = '%ARGS%'; ^
   $sc.WorkingDirectory = '%WORKDIR%'; ^
   $sc.WindowStyle = 7; ^
   $sc.Save()"

echo Installed startup shortcut: %SHORTCUT%
echo TNT Monitor will auto-start on next login.
