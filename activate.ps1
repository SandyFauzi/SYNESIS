# Aktifkan lingkungan SYNESIS.
# Pakai:  . .\activate.ps1

$venv = "E:\SYNESIS\.venv\Scripts\Activate.ps1"

if (-not (Test-Path "E:\SYNESIS")) {
    Write-Host "E:\SYNESIS tidak ditemukan. Enclosure E: terpasang?" -ForegroundColor Red
    return
}
if (-not (Test-Path $venv)) {
    Write-Host "venv tidak ada di E:\SYNESIS\.venv" -ForegroundColor Red
    Write-Host "Bangun ulang:" -ForegroundColor Yellow
    Write-Host "  python -m venv E:\SYNESIS\.venv" -ForegroundColor Yellow
    Write-Host "  E:\SYNESIS\.venv\Scripts\python.exe -m pip install -r requirements.txt" -ForegroundColor Yellow
    return
}

& $venv

Write-Host "SYNESIS aktif" -ForegroundColor Green
Write-Host ("  python : " + (python -c "import sys; print(sys.prefix)")) -ForegroundColor DarkGray
