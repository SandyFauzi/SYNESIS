@echo off
title SYNESIS - latih intent classifier Bulan 2
cd /d "%~dp0.."

set VENV=E:\SYNESIS\.venv\Scripts\python.exe
if not exist "%VENV%" (
    echo venv tidak ada di %VENV%
    echo Enclosure E: terpasang?
    pause
    exit /b 1
)

echo.
echo   melatih pengklasifikasi intent Bulan 2
echo   keluaran juga disalin ke data\bulan2\latihan_terakhir.log
echo.

"%VENV%" -u scripts\latih_bulan2.py 2>&1
if errorlevel 1 (
    echo.
    echo   GAGAL. Lihat pesan di atas.
)

echo.
pause
