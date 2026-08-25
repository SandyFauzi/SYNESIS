"""Konversi suara RVC v2, ditulis ulang tanpa fairseq dan tanpa faiss.

Dipakai Bulan 3 Sesi 5. Piper mengucapkan kalimatnya, lalu berkas ini
mengganti warna suaranya dengan model yang ada di
`E:\\SYNESIS\\models\\voice\\yukino`.

Kenapa ditulis ulang, dan bukan `pip install rvc-python`:

    rvc-python  -> fairseq==0.12.2  -> tidak ada wheel untuk Python 3.12
    rvc-inferpy -> faiss-cpu==1.7.3 -> tidak ada wheel untuk Python 3.12

Keduanya sudah dicoba dan gagal di tahap penyelesaian dependensi, bukan di
tahap pemakaian. Yang tersisa: pasang Python 3.10 khusus untuk satu paket,
atau menulis lintasan inferensinya sendiri. Berkas ini pilihan kedua, dan
harganya sekitar 500 baris.

Yang dipakai sebagai gantinya:

    ContentVec  transformers.HubertModel + bobot `lengyue233/content-vec-best`
    F0          YIN, ditulis sendiri di berkas ini, memakai teorema konvolusi
                dari Bulan 3 Sesi 1 supaya fungsi selisihnya murah
    faiss       tidak dipakai. Retrieval mempertajam warna suara, dan
                melewatinya setara dengan index_rate = 0.

Arsitekturnya SynthesizerTrnMs768NSFsid, yaitu VITS dengan dekoder
NSF-HiFiGAN. Nama atribut modulnya SENGAJA dipertahankan persis seperti di
RVC, karena nama atribut itulah yang jadi kunci di dalam berkas .pth. Nama
yang dibaca manusia ada di komentar.

Pemeriksanya satu dan menggigit: `muat()` membandingkan himpunan kunci
model dengan himpunan kunci berkas .pth. Kalau ada satu saja yang tidak
cocok, ia berhenti dengan pesan yang menyebut kuncinya.
"""

import math
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

from . import konfig

LRELU = 0.1
F0_MIN, F0_MAX = 50.0, 1100.0
MEL_MIN = 1127.0 * math.log(1 + F0_MIN / 700)
MEL_MAX = 1127.0 * math.log(1 + F0_MAX / 700)

CONTENTVEC = "lengyue233/content-vec-best"


# ══════════════════════════════════════════════════════════════
# Potongan VITS: normalisasi, perhatian, dan FFN
# ══════════════════════════════════════════════════════════════

def _bentuk_pad(pasang):
    """Ubah [[a,b],[c,d]] jadi urutan yang diminta F.pad, yaitu terbalik."""
    return [x for sub in pasang[::-1] for x in sub]


class LayerNorm(nn.Module):
    """LayerNorm di sumbu kanal untuk tensor (B, C, T).

    Bukan `nn.LayerNorm` apa adanya karena kanalnya di sumbu 1, bukan sumbu
    terakhir. Nama parameternya gamma dan beta, mengikuti berkas .pth.
    """

    def __init__(self, channels, eps=1e-5):
        super().__init__()
        self.channels, self.eps = channels, eps
        self.gamma = nn.Parameter(torch.ones(channels))
        self.beta = nn.Parameter(torch.zeros(channels))

    def forward(self, x):
        x = x.transpose(1, -1)
        x = F.layer_norm(x, (self.channels,), self.gamma, self.beta, self.eps)
        return x.transpose(1, -1)


class MultiHeadAttention(nn.Module):
    """Perhatian dengan penyandian posisi RELATIF, jendela 10 bingkai.

    Bedanya dengan perhatian biasa: skornya ditambah suku yang cuma
    bergantung pada JARAK antara dua bingkai, bukan pada posisi mutlaknya.
    Untuk suara itu pilihan yang benar, karena "dua bingkai lalu" berarti hal
    yang sama di detik pertama maupun di detik kelima.

    Kamu akan menurunkan bentuk ini sendiri di Bulan 5.
    """

    def __init__(self, channels, out_channels, n_heads, window_size=10):
        super().__init__()
        self.n_heads = n_heads
        self.window_size = window_size
        self.k_channels = channels // n_heads

        self.conv_q = nn.Conv1d(channels, channels, 1)
        self.conv_k = nn.Conv1d(channels, channels, 1)
        self.conv_v = nn.Conv1d(channels, channels, 1)
        self.conv_o = nn.Conv1d(channels, out_channels, 1)

        sisi = self.k_channels ** -0.5
        self.emb_rel_k = nn.Parameter(
            torch.randn(1, window_size * 2 + 1, self.k_channels) * sisi)
        self.emb_rel_v = nn.Parameter(
            torch.randn(1, window_size * 2 + 1, self.k_channels) * sisi)

    def forward(self, x, c, attn_mask=None):
        q, k, v = self.conv_q(x), self.conv_k(c), self.conv_v(c)
        return self.conv_o(self._perhatian(q, k, v, attn_mask))

    def _perhatian(self, query, key, value, mask):
        b, d, t_s = key.size()
        t_t = query.size(2)
        bentuk = (b, self.n_heads, self.k_channels, -1)
        query = query.view(*bentuk).transpose(2, 3)
        key = key.view(*bentuk).transpose(2, 3)
        value = value.view(*bentuk).transpose(2, 3)

        skor = torch.matmul(query / math.sqrt(self.k_channels),
                            key.transpose(-2, -1))
        rel_k = self._iris_rel(self.emb_rel_k, t_s)
        skor = skor + self._rel_ke_abs(
            torch.matmul(query / math.sqrt(self.k_channels),
                         rel_k.unsqueeze(0).transpose(-2, -1)))
        if mask is not None:
            skor = skor.masked_fill(mask == 0, -1e4)

        p = F.softmax(skor, dim=-1)
        keluar = torch.matmul(p, value)
        rel_v = self._iris_rel(self.emb_rel_v, t_s)
        keluar = keluar + torch.matmul(self._abs_ke_rel(p), rel_v.unsqueeze(0))
        return keluar.transpose(2, 3).contiguous().view(b, d, t_t)

    def _iris_rel(self, emb, panjang):
        """Ambil 2*panjang-1 penyandian relatif, ditambahi nol kalau kurang."""
        pad = max(panjang - (self.window_size + 1), 0)
        mulai = max((self.window_size + 1) - panjang, 0)
        if pad > 0:
            emb = F.pad(emb, _bentuk_pad([[0, 0], [pad, pad], [0, 0]]))
        return emb[:, mulai:mulai + 2 * panjang - 1]

    @staticmethod
    def _rel_ke_abs(x):
        """(b, h, l, 2l-1) -> (b, h, l, l). Pergeseran lewat penambahan nol."""
        b, h, l, _ = x.size()
        x = F.pad(x, _bentuk_pad([[0, 0], [0, 0], [0, 0], [0, 1]]))
        x = x.view(b, h, l * 2 * l)
        x = F.pad(x, _bentuk_pad([[0, 0], [0, 0], [0, l - 1]]))
        return x.view(b, h, l + 1, 2 * l - 1)[:, :, :l, l - 1:]

    @staticmethod
    def _abs_ke_rel(x):
        """Kebalikan _rel_ke_abs."""
        b, h, l, _ = x.size()
        x = F.pad(x, _bentuk_pad([[0, 0], [0, 0], [0, 0], [0, l - 1]]))
        x = x.view(b, h, l ** 2 + l * (l - 1))
        x = F.pad(x, _bentuk_pad([[0, 0], [0, 0], [l, 0]]))
        return x.view(b, h, l, 2 * l)[:, :, :, 1:]


class FFN(nn.Module):
    """Dua konvolusi 1D dengan ReLU di tengah. Padding simetris."""

    def __init__(self, in_channels, out_channels, filter_channels, kernel_size):
        super().__init__()
        self.kernel_size = kernel_size
        self.conv_1 = nn.Conv1d(in_channels, filter_channels, kernel_size)
        self.conv_2 = nn.Conv1d(filter_channels, out_channels, kernel_size)

    def _pad(self, x):
        sisi = (self.kernel_size - 1) // 2
        return F.pad(x, _bentuk_pad([[0, 0], [0, 0], [sisi, sisi]]))

    def forward(self, x, x_mask):
        x = self.conv_1(self._pad(x * x_mask))
        x = torch.relu(x)
        return self.conv_2(self._pad(x * x_mask)) * x_mask


class Encoder(nn.Module):
    """Enam lapisan perhatian + FFN, masing-masing dengan sambungan lompat."""

    def __init__(self, hidden_channels, filter_channels, n_heads, n_layers,
                 kernel_size=1, window_size=10):
        super().__init__()
        self.n_layers = n_layers
        self.attn_layers = nn.ModuleList()
        self.norm_layers_1 = nn.ModuleList()
        self.ffn_layers = nn.ModuleList()
        self.norm_layers_2 = nn.ModuleList()
        for _ in range(n_layers):
            self.attn_layers.append(MultiHeadAttention(
                hidden_channels, hidden_channels, n_heads, window_size))
            self.norm_layers_1.append(LayerNorm(hidden_channels))
            self.ffn_layers.append(FFN(
                hidden_channels, hidden_channels, filter_channels, kernel_size))
            self.norm_layers_2.append(LayerNorm(hidden_channels))

    def forward(self, x, x_mask):
        attn_mask = x_mask.unsqueeze(2) * x_mask.unsqueeze(-1)
        x = x * x_mask
        for i in range(self.n_layers):
            x = self.norm_layers_1[i](x + self.attn_layers[i](x, x, attn_mask))
            x = self.norm_layers_2[i](x + self.ffn_layers[i](x, x_mask))
        return x * x_mask


class TextEncoder768(nn.Module):
    """Ubah ciri ContentVec 768 dimensi plus nada jadi sebaran laten.

    Namanya "text encoder" karena VITS aslinya membaca fonem. Di RVC, yang
    masuk bukan fonem melainkan ciri dari HuBERT, dan itulah seluruh gagasan
    konversi suara: ciri HuBERT membawa APA yang diucapkan tanpa membawa
    SIAPA yang mengucapkannya.
    """

    def __init__(self, out_channels=192, hidden_channels=192,
                 filter_channels=768, n_heads=2, n_layers=6, kernel_size=3):
        super().__init__()
        self.out_channels = out_channels
        self.hidden_channels = hidden_channels
        self.emb_phone = nn.Linear(768, hidden_channels)
        self.emb_pitch = nn.Embedding(256, hidden_channels)
        self.lrelu = nn.LeakyReLU(0.1)
        self.encoder = Encoder(hidden_channels, filter_channels, n_heads,
                               n_layers, kernel_size)
        self.proj = nn.Conv1d(hidden_channels, out_channels * 2, 1)

    def forward(self, phone, pitch, lengths):
        x = self.emb_phone(phone) + self.emb_pitch(pitch)
        x = x * math.sqrt(self.hidden_channels)
        x = self.lrelu(x)
        x = torch.transpose(x, 1, -1)
        x_mask = (torch.arange(x.size(2), device=x.device)[None, :]
                  < lengths[:, None]).unsqueeze(1).to(x.dtype)
        x = self.encoder(x * x_mask, x_mask)
        m, logs = torch.split(self.proj(x) * x_mask, self.out_channels, dim=1)
        return m, logs, x_mask


# ══════════════════════════════════════════════════════════════
# Aliran balik: ResidualCouplingBlock
# ══════════════════════════════════════════════════════════════

class WN(nn.Module):
    """Tumpukan konvolusi berkondisi, gaya WaveNet. Tiga lapisan, kernel 5."""

    def __init__(self, hidden_channels, kernel_size, dilation_rate, n_layers,
                 gin_channels=0):
        super().__init__()
        self.hidden_channels = hidden_channels
        self.n_layers = n_layers
        self.in_layers = nn.ModuleList()
        self.res_skip_layers = nn.ModuleList()
        self.cond_layer = nn.Conv1d(
            gin_channels, 2 * hidden_channels * n_layers, 1)
        for i in range(n_layers):
            d = dilation_rate ** i
            pad = (kernel_size * d - d) // 2
            self.in_layers.append(nn.Conv1d(
                hidden_channels, 2 * hidden_channels, kernel_size,
                dilation=d, padding=pad))
            keluar = 2 * hidden_channels if i < n_layers - 1 else hidden_channels
            self.res_skip_layers.append(
                nn.Conv1d(hidden_channels, keluar, 1))

    def forward(self, x, x_mask, g):
        keluar = torch.zeros_like(x)
        n = self.hidden_channels
        g = self.cond_layer(g)
        for i in range(self.n_layers):
            akt = self.in_layers[i](x) + g[:, i * 2 * n:(i + 1) * 2 * n, :]
            akt = torch.tanh(akt[:, :n, :]) * torch.sigmoid(akt[:, n:, :])
            rs = self.res_skip_layers[i](akt)
            if i < self.n_layers - 1:
                x = (x + rs[:, :n, :]) * x_mask
                keluar = keluar + rs[:, n:, :]
            else:
                keluar = keluar + rs
        return keluar * x_mask


class ResidualCouplingLayer(nn.Module):
    """Separuh kanal dipakai untuk menggeser separuh lainnya. Bisa dibalik."""

    def __init__(self, channels, hidden_channels, kernel_size, dilation_rate,
                 n_layers, gin_channels=0):
        super().__init__()
        self.half = channels // 2
        self.pre = nn.Conv1d(self.half, hidden_channels, 1)
        self.enc = WN(hidden_channels, kernel_size, dilation_rate, n_layers,
                      gin_channels)
        self.post = nn.Conv1d(hidden_channels, self.half, 1)

    def forward(self, x, x_mask, g, reverse=True):
        x0, x1 = torch.split(x, [self.half, self.half], 1)
        m = self.post(self.enc(self.pre(x0) * x_mask, x_mask, g)) * x_mask
        # mean_only: logs = 0, jadi pembalikannya cuma pengurangan.
        x1 = (x1 - m) * x_mask if reverse else (x1 + m) * x_mask
        return torch.cat([x0, x1], 1)


class ResidualCouplingBlock(nn.Module):
    """Empat lapisan gandeng, diselingi pembalikan urutan kanal.

    Pembalikan itu perlu: tanpa ia, separuh kanal yang sama selalu jadi
    penggeser dan tidak pernah tergeser.
    """

    def __init__(self, channels=192, hidden_channels=192, kernel_size=5,
                 dilation_rate=1, n_layers=3, n_flows=4, gin_channels=256):
        super().__init__()
        self.flows = nn.ModuleList()
        for _ in range(n_flows):
            self.flows.append(ResidualCouplingLayer(
                channels, hidden_channels, kernel_size, dilation_rate,
                n_layers, gin_channels))
            self.flows.append(nn.Identity())     # tempat Flip, tanpa bobot

    def forward(self, x, x_mask, g):
        for i in range(len(self.flows) - 2, -1, -2):
            x = torch.flip(x, [1])
            x = self.flows[i](x, x_mask, g, reverse=True)
        return x


# ══════════════════════════════════════════════════════════════
# Dekoder: NSF-HiFiGAN
# ══════════════════════════════════════════════════════════════

class ResBlock1(nn.Module):
    """Tiga pasang konvolusi berdilatasi dengan sambungan sisa."""

    def __init__(self, channels, kernel_size=3, dilation=(1, 3, 5)):
        super().__init__()
        def pad(k, d):
            return (k * d - d) // 2
        self.convs1 = nn.ModuleList([
            nn.Conv1d(channels, channels, kernel_size, 1, dilation=d,
                      padding=pad(kernel_size, d)) for d in dilation])
        self.convs2 = nn.ModuleList([
            nn.Conv1d(channels, channels, kernel_size, 1, dilation=1,
                      padding=pad(kernel_size, 1)) for _ in dilation])

    def forward(self, x):
        for c1, c2 in zip(self.convs1, self.convs2):
            xt = c2(F.leaky_relu(c1(F.leaky_relu(x, LRELU)), LRELU))
            x = xt + x
        return x


class SourceModuleHnNSF(nn.Module):
    """Bangkitkan gelombang sinus pada f0, lalu lewatkan satu lapisan linear.

    Inilah bagian "NSF", neural source filter. HiFiGAN polos harus menebak
    fase nada dasar dari nol, dan hasilnya sering berdesir. Di sini
    eksitasinya diberikan langsung sebagai sinus pada f0 yang terukur, jadi
    jaringan tinggal membentuk warna suaranya.

    Fasenya dihitung sebagai jumlah kumulatif f0/laju dalam float64. RVC
    aslinya memakai koreksi berjenjang untuk menghindari hilangnya ketelitian
    float32 pada jumlah kumulatif yang panjang; memakai float64 langsung
    menyelesaikan hal yang sama dengan satu baris.
    """

    def __init__(self, sampling_rate, sine_amp=0.1, noise_std=0.003):
        super().__init__()
        self.sampling_rate = sampling_rate
        self.sine_amp = sine_amp
        self.noise_std = noise_std
        self.l_linear = nn.Linear(1, 1)
        self.l_tanh = nn.Tanh()

    def forward(self, f0, upp):
        # f0 (B, T) -> (B, T*upp, 1)
        f0 = F.interpolate(f0.unsqueeze(1), scale_factor=float(upp),
                           mode="nearest").transpose(1, 2)
        fase = torch.cumsum(f0.double() / self.sampling_rate, dim=1) * 2 * np.pi
        sinus = torch.sin(fase).to(f0.dtype) * self.sine_amp
        uv = (f0 > 0).to(f0.dtype)
        amp = uv * self.noise_std + (1 - uv) * self.sine_amp / 3
        sinus = sinus * uv + amp * torch.randn_like(sinus)
        return self.l_tanh(self.l_linear(sinus))


class GeneratorNSF(nn.Module):
    """Naikkan laju dari 100 bingkai per detik jadi 40.000 cuplikan per detik.

    Empat tahap: 10x, 10x, 2x, 2x. Hasil kalinya 400, dan 400 cuplikan pada
    40 kHz persis 10 milidetik, yaitu satu bingkai.
    """

    def __init__(self, initial_channel=192, resblock_kernel_sizes=(3, 7, 11),
                 resblock_dilation_sizes=((1, 3, 5),) * 3,
                 upsample_rates=(10, 10, 2, 2), upsample_initial_channel=512,
                 upsample_kernel_sizes=(16, 16, 4, 4), gin_channels=256,
                 sr=40000):
        super().__init__()
        self.num_kernels = len(resblock_kernel_sizes)
        self.num_upsamples = len(upsample_rates)
        self.upp = int(np.prod(upsample_rates))
        self.m_source = SourceModuleHnNSF(sr)

        self.noise_convs = nn.ModuleList()
        self.ups = nn.ModuleList()
        for i, u in enumerate(upsample_rates):
            k = upsample_kernel_sizes[i]
            self.ups.append(nn.ConvTranspose1d(
                upsample_initial_channel // (2 ** i),
                upsample_initial_channel // (2 ** (i + 1)),
                k, u, padding=(k - u) // 2))
            c = upsample_initial_channel // (2 ** (i + 1))
            if i + 1 < len(upsample_rates):
                langkah = int(np.prod(upsample_rates[i + 1:]))
                self.noise_convs.append(nn.Conv1d(
                    1, c, langkah * 2, stride=langkah, padding=langkah // 2))
            else:
                self.noise_convs.append(nn.Conv1d(1, c, 1))

        self.resblocks = nn.ModuleList()
        for i in range(self.num_upsamples):
            c = upsample_initial_channel // (2 ** (i + 1))
            for k, d in zip(resblock_kernel_sizes, resblock_dilation_sizes):
                self.resblocks.append(ResBlock1(c, k, d))

        self.conv_pre = nn.Conv1d(initial_channel, upsample_initial_channel,
                                  7, 1, padding=3)
        self.conv_post = nn.Conv1d(c, 1, 7, 1, padding=3, bias=False)
        self.cond = nn.Conv1d(gin_channels, upsample_initial_channel, 1)

    def forward(self, x, f0, g):
        sumber = self.m_source(f0, self.upp).transpose(1, 2)
        x = self.conv_pre(x) + self.cond(g)
        for i in range(self.num_upsamples):
            x = self.ups[i](F.leaky_relu(x, LRELU))
            # Eksitasi disuntikkan lagi di setiap tahap, pada laju cuplik
            # tahap itu. Inilah bedanya NSF-HiFiGAN dengan HiFiGAN biasa.
            n = self.noise_convs[i](sumber)
            x = x + n[:, :, :x.size(2)] if n.size(2) >= x.size(2) else \
                x[:, :, :n.size(2)] + n
            xs = sum(self.resblocks[i * self.num_kernels + j](x)
                     for j in range(self.num_kernels))
            x = xs / self.num_kernels
        return torch.tanh(self.conv_post(F.leaky_relu(x)))


class SynthesizerTrnMs768NSFsid(nn.Module):
    """Model utuh: encoder, aliran balik, dekoder, dan embedding pembicara."""

    def __init__(self, config):
        super().__init__()
        (_, _, inter, hidden, filt, heads, layers, kernel, _, _,
         rb_k, rb_d, up_r, up_c, up_k, n_spk, gin, sr) = config[:18]
        self.enc_p = TextEncoder768(inter, hidden, filt, heads, layers, kernel)
        self.flow = ResidualCouplingBlock(inter, hidden, 5, 1, 3, 4, gin)
        self.dec = GeneratorNSF(inter, tuple(rb_k), tuple(map(tuple, rb_d)),
                                tuple(up_r), up_c, tuple(up_k), gin, sr)
        self.emb_g = nn.Embedding(n_spk, gin)

    @torch.no_grad()
    def infer(self, phone, phone_lengths, pitch, nsff0, sid, skala=0.66666):
        g = self.emb_g(sid).unsqueeze(-1)
        m_p, logs_p, x_mask = self.enc_p(phone, pitch, phone_lengths)
        z_p = (m_p + torch.exp(logs_p) * torch.randn_like(m_p) * skala) * x_mask
        z = self.flow(z_p, x_mask, g)
        return self.dec(z * x_mask, nsff0, g)


# ══════════════════════════════════════════════════════════════
# Nada dasar: YIN
# ══════════════════════════════════════════════════════════════

def f0_yin(x, laju=16000, loncat=160, bingkai=1024, ambang=0.12):
    """Perkirakan f0 tiap bingkai dengan YIN. Kembalikan array Hz, 0 = tak bersuara.

    YIN adalah autokorelasi yang diperbaiki dua kali:

        1  yang dicari bukan puncak autokorelasi melainkan lembah fungsi
           selisih d(tau) = sum_j (x[j] - x[j+tau])^2, yang tidak bias
           terhadap tau kecil;
        2  d(tau) dibagi rerata kumulatifnya, sehingga ambang mutlak jadi
           berarti dan kesalahan oktaf jauh berkurang.

    Fungsi selisihnya dihitung lewat autokorelasi, karena

        d(tau) = e(0) + e(tau) - 2 r(tau)

    dengan r autokorelasi dan e tenaga berjalan. Teorema konvolusi dari Sesi 1
    dipakai apa adanya di sini, dan itu yang membuat 100 bingkai per detik
    bisa dihitung lebih cepat daripada waktu nyata.
    """
    x = np.asarray(x, dtype=np.float64)
    tau_min = max(2, int(laju / F0_MAX))
    tau_maks = min(bingkai // 2, int(laju / F0_MIN))
    n_bingkai = max(1, len(x) // loncat)
    hasil = np.zeros(n_bingkai)

    bantal = np.pad(x, (0, bingkai + tau_maks))
    n_fft = 1 << (2 * bingkai - 1).bit_length()
    kumulatif = np.concatenate([[0.0], np.cumsum(bantal ** 2)])

    for i in range(n_bingkai):
        a = i * loncat
        w = bantal[a:a + bingkai]
        if w.std() < 1e-4:                       # bingkai sunyi
            continue
        spek = np.fft.rfft(w, n_fft)
        r = np.fft.irfft(spek * np.conj(spek), n_fft)[:tau_maks + 1]
        tenaga0 = kumulatif[a + bingkai] - kumulatif[a]
        tau = np.arange(tau_maks + 1)
        tenaga_tau = (kumulatif[a + bingkai + tau] - kumulatif[a + tau])
        d = tenaga0 + tenaga_tau - 2 * r

        d[0] = 0.0
        jumlah = np.cumsum(d[1:])
        dp = np.ones_like(d)
        dp[1:] = d[1:] * np.arange(1, len(d)) / np.maximum(jumlah, 1e-12)

        calon = np.where(dp[tau_min:tau_maks] < ambang)[0]
        if len(calon):
            t = tau_min + int(calon[0])
            # turun ke dasar lembahnya
            while t + 1 < tau_maks and dp[t + 1] < dp[t]:
                t += 1
        else:
            t = tau_min + int(np.argmin(dp[tau_min:tau_maks]))
            if dp[t] > 0.6:                      # terlalu lemah, sebut sunyi
                continue

        # interpolasi parabola pada tiga titik di sekitar lembah
        if 0 < t < tau_maks - 1:
            y0, y1, y2 = dp[t - 1], dp[t], dp[t + 1]
            geser = 0.5 * (y0 - y2) / max(1e-12, y0 - 2 * y1 + y2)
            t = t + np.clip(geser, -1.0, 1.0)
        hasil[i] = laju / t

    return hasil


def haluskan_nada(f0, lebar=5):
    """Tapis median untuk membuang lompatan oktaf sesaat. Disediakan."""
    if lebar < 3 or len(f0) < lebar:
        return f0
    dari = np.lib.stride_tricks.sliding_window_view(
        np.pad(f0, lebar // 2, mode="edge"), lebar)
    keluar = np.median(dari, axis=-1)
    keluar[f0 == 0] = 0.0                        # jangan hidupkan yang sunyi
    return keluar


def nada_kasar(f0):
    """Kuantisasi f0 jadi 1..255 di skala mel, untuk emb_pitch. Disediakan."""
    mel = 1127.0 * np.log(1 + f0 / 700.0)
    bukan_nol = mel > 0
    mel[bukan_nol] = ((mel[bukan_nol] - MEL_MIN) * 254.0
                      / (MEL_MAX - MEL_MIN) + 1.0)
    return np.rint(np.clip(mel, 1, 255)).astype(np.int64)


# ══════════════════════════════════════════════════════════════
# Pemakaian
# ══════════════════════════════════════════════════════════════

def _lepas_weight_norm(sd):
    """Gabungkan weight_g dan weight_v jadi satu weight biasa.

    RVC menyimpan bobot dalam bentuk terparametrisasi: arah v dan besar g,
    dengan w = g * v / ||v||. Bentuk itu berguna waktu melatih dan tidak
    berguna sama sekali waktu menyimpulkan. Menggabungkannya di sini membuat
    seluruh modul di berkas ini jadi Conv1d biasa, dan itu satu lapis
    kerumitan yang hilang.
    """
    keluar = {}
    for k, v in sd.items():
        if k.endswith(".weight_v"):
            dasar = k[:-len("_v")]
            g = sd[dasar + "_g"]
            norma = v.reshape(v.shape[0], -1).norm(dim=1)
            norma = norma.reshape(-1, *([1] * (v.dim() - 1)))
            keluar[dasar] = v * (g / norma)
        elif k.endswith(".weight_g"):
            continue
        else:
            keluar[k] = v
    return keluar


class Yukino:
    """Pengubah warna suara. Muat sekali, pakai berkali-kali.

    Pemakaian:

        y = Yukino()
        keluar, laju = y.ubah(sinyal_16k, nada=0)
    """

    def __init__(self, berkas=None, peranti=None):
        self.peranti = peranti or ("cuda" if torch.cuda.is_available()
                                   else "cpu")
        self.berkas = Path(berkas or konfig.RVC_MODEL)
        self.net_g = None
        self.hubert = None

    def muat(self):
        """Muat kedua model. Kunci .pth diperiksa satu per satu. Disediakan."""
        if self.net_g is not None:
            return self
        if not self.berkas.exists():
            raise FileNotFoundError(f"model RVC tidak ada: {self.berkas}")

        titik = torch.load(self.berkas, map_location="cpu", weights_only=False)
        self.laju_keluar = int(titik["config"][-1])
        self.net_g = SynthesizerTrnMs768NSFsid(titik["config"])
        sd = _lepas_weight_norm(titik["weight"])

        punya = set(self.net_g.state_dict())
        datang = set(sd)
        if punya != datang:
            hilang = sorted(punya - datang)[:5]
            lebih = sorted(datang - punya)[:5]
            raise RuntimeError(
                f"kunci tidak cocok. hilang {len(punya - datang)} "
                f"{hilang}, berlebih {len(datang - punya)} {lebih}")
        self.net_g.load_state_dict(sd, strict=True)
        self.net_g.eval().to(self.peranti)

        from transformers import HubertModel
        self.hubert = HubertModel.from_pretrained(CONTENTVEC)
        self.hubert.eval().to(self.peranti)
        return self

    @torch.no_grad()
    def ubah(self, x, nada=0, sid=0):
        """Ubah warna suara sinyal 16 kHz. Kembalikan (sinyal, laju keluar).

        nada : geseran dalam semiton. Piper Indonesia yang dipakai SYNESIS
               suaranya sudah perempuan, jadi 0 biasanya benar. Sumber suara
               laki-laki perlu +12.
        """
        self.muat()
        x = np.asarray(x, dtype=np.float32)
        puncak = np.abs(x).max()
        if puncak > 0.95:
            x = x * (0.95 / puncak)

        wav = torch.from_numpy(x).unsqueeze(0).to(self.peranti)
        ciri = self.hubert(wav).last_hidden_state          # (1, T, 768)
        ciri = F.interpolate(ciri.transpose(1, 2), scale_factor=2,
                             mode="nearest").transpose(1, 2)

        p_len = min(len(x) // 160, ciri.size(1))
        ciri = ciri[:, :p_len]

        f0 = haluskan_nada(f0_yin(x))[:p_len]
        f0 = np.pad(f0, (0, max(0, p_len - len(f0))))
        f0 = f0 * (2.0 ** (nada / 12.0))

        pitch = torch.from_numpy(nada_kasar(f0.copy())).unsqueeze(0).to(self.peranti)
        pitchf = torch.from_numpy(f0.astype(np.float32)).unsqueeze(0).to(self.peranti)
        panjang = torch.LongTensor([p_len]).to(self.peranti)
        sid_t = torch.LongTensor([sid]).to(self.peranti)

        keluar = self.net_g.infer(ciri, panjang, pitch, pitchf, sid_t)
        return keluar[0, 0].float().cpu().numpy(), self.laju_keluar


def _demo():
    """Periksa yang bisa diperiksa tanpa audio: bentuk, kunci, dan f0."""
    # YIN pada sinus murni harus mengembalikan frekuensinya.
    t = np.arange(16000) / 16000
    for f in (120.0, 220.0, 440.0):
        x = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t)
        ukur = np.median(f0_yin(x)[5:-5])
        galat = abs(ukur - f) / f
        assert galat < 0.02, f"YIN {f} Hz -> {ukur:.1f} Hz"

    # Sunyi harus dilaporkan sebagai tak bersuara.
    assert f0_yin(np.zeros(16000)).max() == 0.0

    # Kuantisasi mel harus monoton dan di dalam 1..255.
    kasar = nada_kasar(np.array([0.0, 50.0, 200.0, 1100.0, 2000.0]))
    assert kasar[0] == 1 and kasar[-1] == 255
    assert (np.diff(kasar) >= 0).all()

    if Path(konfig.RVC_MODEL).exists():
        titik = torch.load(konfig.RVC_MODEL, map_location="cpu",
                           weights_only=False)
        net = SynthesizerTrnMs768NSFsid(titik["config"])
        sd = _lepas_weight_norm(titik["weight"])
        assert set(net.state_dict()) == set(sd), "kunci RVC tidak cocok"
        for k, v in net.state_dict().items():
            assert v.shape == sd[k].shape, f"bentuk beda di {k}"


if __name__ == "__main__":
    _demo()
    print("rvc: semua lulus")
