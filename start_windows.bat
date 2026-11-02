@echo off
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe py -m venv .venv
call .venv\Scripts\activate
python -m pip install -r requirements.txt
if not exist .env copy .env.example .env
findstr /C:"your_new_api_key_here" .env >nul
if %errorlevel%==0 (
  echo Add your NEW OpenAI API key inside .env, then run this file again.
  pause
  exit /b 0
)
uvicorn main:app --host 127.0.0.1 --port 8000
