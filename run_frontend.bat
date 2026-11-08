@echo off
setlocal
echo ========================================================
echo Starting AI Legal Document Analyzer - Flutter UI
echo ========================================================

REM Automatically locate Flutter SDK in project or system PATH
if exist "%~dp0flutter\bin\flutter.bat" (
    set "PATH=%~dp0flutter\bin;%~dp0Git\cmd;%PATH%"
)

cd /d "%~dp0frontend"

echo Detecting available display targets...
echo.
echo Select target platform:
echo [1] Chrome Web (Recommended - Fast & Instant)
echo [2] Windows Desktop App
echo.
choice /c 12 /n /m "Choose target [1 or 2]: "

if errorlevel 2 goto run_windows
if errorlevel 1 goto run_chrome

:run_chrome
echo.
echo Launching on Google Chrome...
call flutter run -d chrome
goto end

:run_windows
echo.
echo Launching on Windows Desktop...
call flutter run -d windows
if errorlevel 1 (
    echo.
    echo [Notice] Windows desktop build failed (Visual Studio C++ may not be installed).
    echo Falling back to Chrome Web...
    call flutter run -d chrome
)
goto end

:end
pause
