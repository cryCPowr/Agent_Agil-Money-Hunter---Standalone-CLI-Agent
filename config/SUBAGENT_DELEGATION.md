# SUBAGENT_DELEGATION.md
## Skenario Delegasi ke Sub-Agent

### Pembagian Tugas
- Parent agent (Agent_Agil) boleh spawn sub-agent untuk kerja paralel
  per niche atau per project (mis. 1 sub-agent fokus freelance writing,
  1 sub-agent fokus riset crypto, dsb).
- Sub-agent kerja dalam SATU niche/project spesifik — tidak merangkap
  banyak niche sekaligus (biar fokus & mudah dievaluasi).
- Sub-agent WAJIB mewarisi SOUL.md dari parent (identitas & prinsip inti
  tidak boleh hilang di delegasi).

### Batasan Depth Spawning
- Sub-agent boleh mengusulkan spawn sub-agent baru (depth 2 dan seterusnya) untuk
  memecah tugas lebih kecil.
- Spawning depth > 2 (sub-agent dari sub-agent dari sub-agent) WAJIB
  approval dari parent agent DAN user — untuk mencegah biaya credit LLM
  membengkak tanpa kendali dari spawning yang tidak perlu.
- Setiap sub-agent baru dicatat: siapa parent-nya, tujuannya apa, dan
  budget/limit credit LLM yang dialokasikan untuknya.

### Batasan Konteks yang Di-share
- `skip_context_files` TIDAK boleh aktif untuk SOUL.md — kalau context
  files di-skip saat delegasi, sub-agent WAJIB tetap eksplisit di-load
  dengan SOUL.md minimal (identitas inti), supaya tidak fallback ke
  identitas default generik.
- AGENTS.md yang di-share ke sub-agent cukup bagian relevan ke niche-nya
  (tidak perlu semua niche kalau sub-agent hanya kerja 1 niche).
- Wallet & limit spending: sub-agent TIDAK otomatis dapat akses wallet
  penuh milik parent. Kalau sub-agent butuh dana, request ke parent
  (parent yang pegang kontrol alokasi, bukan tiap sub-agent independen
  akses wallet yang sama).

### Memory/Konteks Awal untuk Sub-Agent
- Ringkasan hasil riset niche yang relevan dari parent (biar tidak mulai
  dari nol).
- Limit & budget yang dialokasikan untuk sub-agent ini.
- Daftar strategi yang sudah terbukti gagal/berhasil di niche terkait
  (dari MEMORY_SEED.json / procedural memory parent).
- Preferensi user yang relevan (lihat MEMORY_SEED.json).
