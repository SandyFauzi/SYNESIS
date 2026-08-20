# Pantau progres instalasi paket besar ke E:\SYNESIS
# Pakai: powershell -File progress.ps1
$ErrorActionPreference = "SilentlyContinue"
$TARGET = 5600   # perkiraan ukuran venv setelah PyTorch, dalam MB
$host.UI.RawUI.WindowTitle = "SYNESIS - progres instalasi"

function Ukur($p) {
    if (-not (Test-Path $p)) { return 0 }
    return (Get-ChildItem $p -Recurse -File | Measure-Object Length -Sum).Sum / 1MB
}

$mulai = Get-Date
$prev = Ukur "E:\SYNESIS\.venv"

while ($true) {
    $venv  = Ukur "E:\SYNESIS\.venv"
    $cache = Ukur "E:\SYNESIS\.cache\pip"
    $cdrv  = Ukur "$env:LOCALAPPDATA\pip\Cache"
    $torch = Test-Path "E:\SYNESIS\.venv\Lib\site-packages\torch\__init__.py"

    $pct = [math]::Min(100, [int](($venv / $TARGET) * 100))
    $isi = [int]($pct / 2)
    $bar = ("#" * $isi) + ("." * (50 - $isi))
    $laju = [math]::Max(0, $venv - $prev) * 2   # MB per detik (refresh 0.5s)
    $prev = $venv

    Clear-Host
    Write-Host ""
    Write-Host "  PROGRES INSTALASI SYNESIS" -ForegroundColor Cyan
    Write-Host "  =========================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host ("  [{0}] {1,3}%" -f $bar, $pct) -ForegroundColor Green
    Write-Host ""
    Write-Host ("  venv di E:      {0,8:N0} MB  / ~{1:N0} MB" -f $venv, $TARGET)
    Write-Host ("  cache pip E:    {0,8:N0} MB" -f $cache)
    if ($cdrv -gt 50) {
        Write-Host ("  cache di C:     {0,8:N0} MB   <-- BOCOR" -f $cdrv) -ForegroundColor Red
    } else {
        Write-Host ("  cache di C:     {0,8:N0} MB   bersih" -f $cdrv) -ForegroundColor DarkGray
    }
    Write-Host ""
    Write-Host ("  laju            {0,8:N1} MB/s" -f $laju)
    Write-Host ("  berjalan        {0,8}" -f ((Get-Date) - $mulai).ToString("hh\:mm\:ss"))
    Write-Host ""
    if ($torch) {
        Write-Host "  torch: TERPASANG" -ForegroundColor Green
        Write-Host ""
        Write-Host "  Selesai. Tutup jendela ini." -ForegroundColor Yellow
        break
    } else {
        Write-Host "  torch: masih mengunduh / memasang" -ForegroundColor Yellow
    }
    Start-Sleep -Milliseconds 500
}
Write-Host ""
Read-Host "  Tekan Enter untuk menutup"
