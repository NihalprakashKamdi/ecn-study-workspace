#!/data/data/com.termux/files/usr/bin/bash
set -e
cd "$(dirname "$0")"
pkg install -y python
python -m pip install -r requirements.txt
if [ ! -f .env ]; then cp .env.example .env; fi
if grep -q 'your_new_api_key_here' .env; then
  echo 'Edit .env and add your NEW OpenAI API key, then run this script again.'
  exit 0
fi
uvicorn main:app --host 127.0.0.1 --port 8000
