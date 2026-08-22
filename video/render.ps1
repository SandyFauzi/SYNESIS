# Render seluruh seri video SYNESIS lalu sambung jadi satu berkas.
# Pakai dari folder video:  .\render.ps1

$py = "S:\Code\manimations\.venv\Scripts\python.exe"

if (-not (Test-Path $py)) {
    Write-Host "venv manim tidak ditemukan di $py" -ForegroundColor Red
    Write-Host "Ubah baris `$py di berkas ini kalau lokasinya pindah." -ForegroundColor Yellow
    return
}

$bab = @(
    @{ berkas = "bab1_menuruni.py";  kelas = "Bab1"; nama = "bab1" },
    @{ berkas = "bab2_lanskap.py";   kelas = "Bab2"; nama = "bab2" },
    @{ berkas = "bab3_menghafal.py"; kelas = "Bab3"; nama = "bab3" },
    @{ berkas = "bab4_mesin.py";     kelas = "Bab4"; nama = "bab4" }
)

New-Item -ItemType Directory -Force keluaran | Out-Null

foreach ($b in $bab) {
    Write-Host "render $($b.nama) ..." -ForegroundColor Cyan
    & $py -m manim -ql --disable_caching -o "$($b.nama).mp4" $b.berkas $b.kelas
    if (-not $?) {
        Write-Host "gagal di $($b.nama)" -ForegroundColor Red
        return
    }
    $src = Get-ChildItem -Recurse -Path media/videos -Filter "$($b.nama).mp4" |
           Select-Object -First 1
    Copy-Item $src.FullName "keluaran/$($b.nama).mp4" -Force
}

# sambung keempatnya
$daftar = "keluaran/daftar.txt"
$bab | ForEach-Object { "file '$($_.nama).mp4'" } | Out-File -Encoding utf8 $daftar

Write-Host "menyambung jadi satu ..." -ForegroundColor Cyan
ffmpeg -y -v error -f concat -safe 0 -i $daftar -c copy `
       keluaran/synesis-bulan0-lengkap.mp4

Write-Host "selesai. hasil ada di keluaran\" -ForegroundColor Green
Get-ChildItem keluaran/*.mp4 |
    Select-Object Name, @{n = "MB"; e = { [math]::Round($_.Length / 1MB, 2) } } |
    Format-Table -AutoSize
