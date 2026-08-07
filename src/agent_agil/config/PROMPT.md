# PROMPT.md
---

### PROMPT UNTUK HERMES ()

```
Aku mau kamu buatkan sub-agent baru bernama "Money-Hunter" berdasarkan
file-file berikut. Baca dan proses dengan urutan ini, karena urutannya
penting untuk membangun konteks yang benar:

1. PRD_Agent_Agil.txt — baca dulu untuk paham tujuan, prinsip desain, dan scope
   secara keseluruhan sebelum baca file lain.

2. SOUL.md — ini identitas inti agent, taruh sebagai layer paling dasar
   di system prompt sub-agent (slot #1). Ini tidak boleh ditimpa atau
   diringkas oleh file lain.

3. AGENTS.md — konteks domain/proyek, termasuk daftar tools dan
   kategorinya (bebas pakai / butuh cek limit / selalu butuh approval).
   Terapkan pembagian akses ini persis seperti yang tertulis — jangan
   samakan semua tools jadi "bebas pakai".

4. MCP_TOOLS.md — sambungkan MCP server yang disebutkan di sini. Untuk
   bagian wallet crypto, ikuti catatan keamanan yang tertulis: JANGAN
   berikan private key mentah dengan akses tanpa batas. Kalau provider
   wallet yang tersedia di Hermes belum mendukung session key/scoped
   permission, beri tahu aku dulu sebelum lanjut — jangan diam-diam
   fallback ke akses penuh.

5. SKILLS.md — install/aktifkan skill yang relevan dari Skills Hub kalau
   tersedia, atau catat sebagai skill custom kalau tidak ada.

6. config.yaml — set personality overlay sesuai isi file ini, aktifkan
   /personality switching.

7. WORKFLOW.md — jadikan ini alur kerja standar tiap siklus kerja
   agent (dari riset niche sampai laporan & evaluasi keberlanjutan).

8. SUBAGENT_DELEGATION.md — aturan ini berlaku kalau/ketika Money-Hunter
   mendelegasikan tugas ke sub-agent lain. Terapkan batas depth spawning
   persis seperti yang tertulis.

9. MEMORY_SEED.json — ini memory awal & preferensi user. Load semua
   angka limit dan preferensi dari sini sebagai konfigurasi aktif,
   BUKAN sebagai saran yang bisa diabaikan.

Setelah semua file diproses, konfirmasi ke aku dalam bentuk ringkasan:
- Tools apa saja yang berhasil dikonfigurasi vs yang gagal/belum tersedia
- perkiraan Limit spending harian & per-transaksi yang aktif sekarang
- MCP server mana yang berhasil terkoneksi
- Kalau ada bagian dari file yang tidak bisa diterapkan persis (misal
  Hermes tidak punya fitur session key untuk wallet), sebutkan
  eksplisit apa alternatifnya, jangan diam-diam skip.

Jangan mulai eksekusi project apa pun sebelum aku konfirmasi ringkasan
ini benar.
```

---

### Kenapa Diminta Konfirmasi Dulu (bukan langsung eksekusi)

Ini bukan langkah opsional — ini kesempatan terakhir kamu untuk cek:
- Apakah wallet setup-nya beneran pakai scoped permission, atau Hermes
  cuma bisa kasih akses penuh (kalau begitu, kamu masih punya kesempatan
  mundur/isi wallet dengan jumlah kecil dulu).
- Apakah ada tools/MCP yang diminta di file tapi tidak tersedia di
  Hermes, supaya kamu bisa cari alternatif sebelum agent mulai jalan.

### Setelah Konfirmasi OK
Baru kasih perintah eksekusi, misalnya:
```
Oke, mulai siklus pertama. Fokus riset niche dulu (jangan langsung
eksekusi project), laporkan ke aku hasil riset & rencana project
sebelum kamu commit dana/waktu ke satu niche.
```

Ini juga sekaligus "tes drive" — biar kamu lihat dulu cara mikirnya
sebelum kasih dia keleluasaan penuh sesuai batas yang sudah ditentukan.

### GUI/TUI
- buatkan semenarik mungkin untuk AGENT_AGIL ini (high)
- buatkan se-responsif (high)
- buatkan se-atraktif (high)
