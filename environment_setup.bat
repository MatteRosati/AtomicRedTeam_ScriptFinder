@echo off
echo [*] Creazione ambiente virtuale...
python -m venv venv

echo [*] Attivazione ambiente virtuale...
call venv\Scripts\activate.bat

echo [*] Installazione dei pacchetti...
pip install -r requirements.txt

echo [✓] Ambiente pronto. Ora puoi lanciare lo script con:
echo    venv\Scripts\activate && python Finder.py
pause
