@echo off
REM Peluncur SYNESIS tanpa .exe. Klik dua kali, atau jalankan dari terminal.
REM Isinya sama persis dengan SYNESIS.exe; bedanya cuma ini tidak perlu
REM dibangun ulang tiap kali synesis\luncur.py berubah.
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
REM HF_HOME hanya disetel kalau belum ada. Kalau kamu sudah
REM menyetelnya sendiri, setelanmu yang menang.
if "%HF_HOME%"=="" set HF_HOME=E:\SYNESIS\.cache\huggingface

if not exist "E:\SYNESIS\.venv\Scripts\python.exe" (
    echo.
    echo   venv tidak ditemukan di E:\SYNESIS\.venv
    echo   Enclosure E: terpasang?
    echo.
    pause
    exit /b 1
)

"E:\SYNESIS\.venv\Scripts\python.exe" -m synesis.luncur %*
