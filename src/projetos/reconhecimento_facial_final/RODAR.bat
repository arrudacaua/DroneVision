@echo off
cd /d %~dp0
call .venv\Scripts\activate.bat
python reconhecimento_facial.py
pause
