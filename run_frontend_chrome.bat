@echo off
setlocal
echo ========================================================
echo Starting AI Legal Document Analyzer - Chrome Web
echo ========================================================
if exist "%~dp0flutter\bin\flutter.bat" (
    set "PATH=%~dp0flutter\bin;%~dp0Git\cmd;%PATH%"
)
cd /d "%~dp0frontend"
call flutter run -d chrome
pause
