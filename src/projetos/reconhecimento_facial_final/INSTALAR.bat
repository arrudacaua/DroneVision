@echo off
cd /d %~dp0
py -3.11 -m venv .venv
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install dlib-bin
pip install -r requirements.txt --no-deps
pip install opencv-python numpy pillow click colorama
pause
