@echo off
cd /d "%~dp0"
if not exist venv python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
start "LegalEase Backend" cmd /k "cd /d %~dp0 && call venv\Scripts\activate && uvicorn legalEaseAPI.main:app --port 8000"
timeout /t 6 /nobreak >nul
streamlit run frontend/app.py
