# Aktifkan venv SYNESIS yang tinggal di E:
# Pakai:  . .\activate.ps1
$venv = "E:\SYNESIS\.venv\Scripts\Activate.ps1"
if (-not (Test-Path $venv)) {
    Write-Host "venv tidak ditemukan di E:\SYNESIS\.venv" -ForegroundColor Red
    Write-Host "Enclosure E: terpasang? Kalau tidak, colok dulu." -ForegroundColor Yellow
    return
}
& $venv
Write-Host "venv SYNESIS aktif  ->  $(python -c 'import sys; print(sys.prefix)')" -ForegroundColor Green
