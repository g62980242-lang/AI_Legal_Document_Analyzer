@echo off
echo ========================================================
echo Starting AI Legal Document Analyzer - FastAPI Backend
echo Privacy-First Local Offline Engine
echo ========================================================
cd /d "%~dp0\backend"
set PYTHONPATH=%~dp0\backend;%PYTHONPATH%
..\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
pause
