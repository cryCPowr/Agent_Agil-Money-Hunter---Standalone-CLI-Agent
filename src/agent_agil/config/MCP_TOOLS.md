# MCP_TOOLS.md
## MCP Server & Tool Requirements

### MCP Server yang Perlu Dikoneksikan
- **Browser/search MCP** — riset umum (wajib).
- **GitHub MCP** — baca/analisis/fork repo (wajib).
- **Social media read-only MCP** — riset tren & niche (wajib, read-only saja
  di awal; write access/posting butuh approval eksplisit per platform).
- **Crypto wallet MCP** — LIHAT CATATAN KEAMANAN DI BAWAH. Gunakan
  provider yang mendukung session key / scoped permission / spending limit
  (mis. account abstraction, EIP-7702-style permission), BUKAN private key
  mentah yang dipegang penuh oleh agent.
- **Payment/finance MCP** — untuk terima pembayaran freelance/jasa (kalau
  platform freelance yang dipakai menyediakan).
- **Freelance platform MCP** (kalau tersedia) — untuk niche freelance.
- **Email MCP — akun terpisah khusus agent** (bukan email pribadi utama
  user). Tidak untuk membaca/forward OTP akun pribadi user.
- **Logging/storage MCP** — untuk mencatat transaksi & laporan supaya bisa
  diaudit (persistent storage, bukan cuma di memory percakapan).
- **Location & Mapping MCP (mis. Mapbox/OpenStreetMap MCP)** — wajib untuk niche *Travel & Tourism* dan *Outdoor Trail Scouting* guna membaca data elevasi, rute mikro, dan koordinat jalur secara presisi.
- **Media Transkripsi & Audio Processing MCP** — untuk niche *Genealogy & Legacy*, *Sonic Branding/ASMR*, dan *Linguistic Preservation* guna menangani file audio besar, transkripsi fonetik, dan *noise removal*.
- **Game Engine & Asset Registry MCP** — untuk niche *Game World Building* dan *Tabletop/Board Game* guna membaca repositori aset visual, struktur skrip kode game, serta memvalidasi aturan main (*ruleset*).
- **Automation & Workflow Engine MCP** — untuk niche *AI Automation Architect* guna menguji dan menghubungkan rantai integrasi bot secara otomatis.
- **Database Inventaris Tumbuhan MCP (mis. PlantNet/OpenWeather MCP)** — untuk niche *Urban Farming & Plant Care* guna mendiagnosis kesehatan daun via visual dan memantau siklus cuaca harian.
- **Social Listening & Trend Scraper MCP** — untuk niche *Fashion Scouting* dan *Community Management* guna memindai pergerakan tren visual global serta memoderasi ruang obrolan.
- **Calendar & Resource Management MCP** — untuk niche *Cultural Event Production* guna mengatur linimasa menit-demi-menit, anggaran logistik, dan koordinasi jadwal.

Niche tambahan yang ditemukan agent dari pengalaman/memory-nya sendiri boleh
diajukan sebagai MCP baru — tapi tetap lewat approval user sebelum
dikoneksikan (karena setiap MCP baru = akses/kredensial baru).

### Toolset Whitelist/Filter
Lihat AGENTS.md bagian TOOLS untuk daftar detail per kategori:
- **Bebas Dipakai Tanpa Approval:** 
  - Scraping data tren publik, analisis teks/transkripsi audio lokal, pemetaan rute satelit publik, dan pengujian kode skrip di lingkungan *sandbox*.
- **Butuh Cek Limit Sebelum Eksekusi:** 
  - Penggunaan API berbayar untuk pemrosesan AI skala besar (seperti konversi audio panjang atau rendering aset visual) dan panggilan API pihak ketiga yang memiliki kuota harian.
- **Selalu Butuh Approval Eksplisit:** 
  - Publikasi konten massal ke platform eksternal, perubahan struktur sistem otomatisasi yang berdampak langsung pada pengguna, atau pengeluaran dana operasional.

### CATATAN KEAMANAN — WALLET CRYPTO
Jangan berikan private key mentah dengan akses penuh tanpa batas ke agent.
Risiko utama: kalau agent kena prompt-injection (dari halaman web, repo
GitHub, DM sosmed, dsb) yang dibacanya saat riset, private key mentah bisa
langsung disalahgunakan tanpa ada "pagar" yang menahan.
- **Pemisahan Ruang Data:** Pastikan dokumen privat seperti arsip sejarah keluarga atau catatan kebugaran pribadi disimpan di direktori terenkripsi terpisah, tidak tercampur dengan data publik yang diakses agen saat riset.
- **Validasi Eksternal:** Untuk niche yang melibatkan interaksi dunia nyata (seperti *Urban Farming*, *Travel*, atau *Event Production*), agen hanya bertindak sebagai pemberi rekomendasi dan pengingat; eksekusi fisik di lapangan tetap berada di tangan manusia sepenuhnya.

Rekomendasi setup:
- Isi wallet secukupnya (bukan seluruh dana user).
- Pakai session key/scoped permission dengan expiry & spending limit,
  kalau provider walletnya mendukung.
- Set limit harian & limit per-transaksi eksplisit di MCP config.
- Transaksi di atas limit → auto-pause, minta approval user, bukan
  auto-reject total (biar tetap fleksibel tapi tetap ada kontrol).

### Custom Tools
Agent dapat mengembangkan alat bantu (*custom tools*) sendiri untuk otomatisasi tugas repetitif pada niche-niche di atas, dengan ketentuan:
- Wajib melalui tahap uji coba (*testing*) di lingkungan lokal yang aman(default), atau lingkungan eksplisit(optional ask user).
- Dicatat dalam berkas memori internal secara transparan.
- Memerlukan izin persetujuan (*approval*) dari pengguna apabila *custom tool* tersebut memerlukan kredensial akun baru atau hak akses jaringan eksternal.
