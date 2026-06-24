# Product Requirements Document (PRD)
## MetaLearn — Platform Pembelajaran Adaptif Berbasis AI

**Versi:** 1.1.0
**Tanggal:** Juni 2026
**Tim:** NexaNode — Universitas Muria Kudus
**Kompetisi:** Samsung Solve for Tomorrow 2026
**Status:** Concept Paper / Pre-Development

---

## Daftar Isi

1. [Ringkasan Eksekutif](#1-ringkasan-eksekutif)
2. [Konteks & Permasalahan](#2-konteks--permasalahan)
3. [Target Pengguna](#3-target-pengguna)
4. [Tujuan Produk](#4-tujuan-produk)
5. [Scope & Batasan](#5-scope--batasan)
6. [Fitur & Persyaratan Fungsional](#6-fitur--persyaratan-fungsional)
7. [Project-Based Memory System](#7-project-based-memory-system)
8. [Persyaratan Non-Fungsional](#8-persyaratan-non-fungsional)
9. [Arsitektur & Stack Teknologi](#9-arsitektur--stack-teknologi)
10. [Alur Pengguna (User Flow)](#10-alur-pengguna-user-flow)
11. [Desain Database (ERD)](#11-desain-database-erd)
12. [Kontribusi AI](#12-kontribusi-ai)
13. [Gamifikasi & Motivasi](#13-gamifikasi--motivasi)
14. [Dampak & Keberlanjutan](#14-dampak--keberlanjutan)
15. [Aspek STEM](#15-aspek-stem)
16. [Risiko & Mitigasi](#16-risiko--mitigasi)
17. [Referensi](#17-referensi)

---

## 1. Ringkasan Eksekutif

MetaLearn adalah **Progressive Web Application (PWA) berbasis AI** yang dirancang untuk mengatasi krisis motivasi dan pemahaman konseptual siswa sekolah menengah Indonesia. Platform ini menggabungkan tiga pilar teknologi: **Adaptive Learning**, **Gamification**, dan **Natural Language Processing (NLP)**.

Berdasarkan data PISA 2022, Indonesia berada di posisi ke-72 dari 78 negara peserta dengan skor literasi matematika hanya 379. MetaLearn hadir sebagai respons konkret terhadap kegagalan metodologi pengajaran konvensional yang bersifat satu arah dan tidak adaptif.

**Proposisi nilai inti:** Setiap siswa mendapat jalur belajar yang dikalibrasi secara real-time oleh AI, bukan kurikulum seragam yang mengabaikan kecepatan kognitif individu. Seluruh konteks belajar, preferensi, dan progres tersimpan dalam **Project-Based Memory System** — memori persisten berbasis file yang memungkinkan AI mengingat dan melanjutkan sesi tanpa kehilangan konteks.

---

## 2. Konteks & Permasalahan

### 2.1 Latar Belakang

Ekosistem akademik Indonesia mengalami degradasi kronis yang termanifestasi dalam beberapa indikator:

- **Peringkat PISA 2022:** Posisi ke-72 dari 78 negara dengan skor matematika 379
- **Metode pengajaran:** Dominasi instruksi satu arah yang membatasi imajinasi dan eksplorasi mandiri
- **Infrastruktur teknologi:** Ketidaksiapan adopsi teknologi adaptif di mayoritas institusi
- **Karakteristik Generasi Z:** Durasi fokus singkat akibat paparan gawai, kebutuhan akan interaktivitas dan otonomi belajar

### 2.2 Pernyataan Masalah (How Might We)

> *Bagaimana cara menciptakan ekosistem pembelajaran digital yang mampu mengadaptasi kurikulum sesuai kecepatan pemahaman individu secara otomatis, sekaligus memadukan kecerdasan buatan dengan mekanika permainan demi membangkitkan dorongan intrinsik siswa?*

### 2.3 Temuan Riset Pengguna

Berdasarkan observasi lapangan terhadap persona representatif siswa SMA usia 16 tahun:

- Siswa menolak rutinitas menghafal rumus abstrak
- Keinginan belajar dalam format interaktif dan berbasis permainan
- Kebutuhan penghargaan inkremental untuk mempertahankan rasa ingin tahu
- Absennya otonomi memilih jalur belajar menyebabkan apatis

### 2.4 Bukti Empiris

Integrasi elemen gamifikasi berbasis teknologi terbukti menyumbang **31,3% peningkatan partisipasi peserta didik** (Ditha et al., 2026; Niyazova et al., 2026).

---

## 3. Target Pengguna

### 3.1 Pengguna Utama

| Segmen | Deskripsi | Kebutuhan Utama |
|--------|-----------|-----------------|
| Siswa SMP | Usia 12–15 tahun | Konten visual, gamifikasi tinggi, panduan eksplisit |
| Siswa SMA/SMK | Usia 15–18 tahun | Adaptivitas jalur, analitik performa, otonomi belajar |

### 3.2 Pengguna Sekunder

| Segmen | Deskripsi | Kebutuhan Utama |
|--------|-----------|-----------------|
| Guru / Tenaga Pendidik | Pemantau kemajuan kelas | Dashboard analitik real-time, laporan narrative AI |
| Administrator Sekolah | Pengelola institusi | Manajemen akun massal, integrasi kurikulum |

---

## 4. Tujuan Produk

### 4.1 Tujuan Primer

1. **Meningkatkan otonomi belajar** melalui *Adaptive Interest Scanner* dan *AI-Driven Adaptive Pathway* yang memetakan minat dan gaya belajar setiap siswa
2. **Memperdalam pemahaman konseptual** dengan *Knowledge Tree Assessment* berbasis Abstract Syntax Tree (evaluasi struktur logika, bukan sekadar pencocokan kata kunci)
3. **Menyediakan pembelajaran personal real-time** melalui *Real-Time Personalization Engine*, *Dynamic Re-routing*, dan *Pause & Ask AI*

### 4.2 Tujuan Sekunder

4. **Meringankan beban guru** dengan *AI-Generated Narrative Report*, *Metacognitive Dashboard*, dan sistem gamifikasi otomatis
5. **Mendukung SDG 4** (Pendidikan Berkualitas & Inklusif) dengan jalur belajar yang mengakomodasi kebutuhan neurokognitif individu, termasuk *remedial mission* dan *continuous learning scheduler*
6. **Mempertahankan konteks belajar lintas sesi** melalui *Project-Based Memory System* yang menyimpan memori AI secara lokal dan terstruktur, memastikan kontinuitas personalisasi tanpa pengulangan onboarding

### 4.3 Metrik Keberhasilan (KPI)

| Metrik | Target | Periode |
|--------|--------|---------|
| Tingkat penyelesaian misi (mission completion rate) | ≥ 70% | Bulan ke-3 |
| Retensi pengguna aktif 30 hari | ≥ 60% | Bulan ke-3 |
| Peningkatan skor assessment | ≥ 20% vs baseline | Bulan ke-6 |
| Waktu sesi rata-rata | ≥ 25 menit | Bulan ke-1 |
| Net Promoter Score guru | ≥ 7/10 | Bulan ke-6 |

---

## 5. Scope & Batasan

### 5.1 Dalam Scope (MVP)

- Onboarding & profiling minat pengguna
- Knowledge Map interaktif berbasis konstelasi visual
- Adaptive Learning Path dengan Dynamic Difficulty Adjustment
- Sistem assessment berbasis Knowledge Tracing
- Gamifikasi (poin XP, lencana, level)
- Fitur Pause & Ask AI (NLP)
- Dashboard laporan guru
- Dukungan PWA (offline-capable)
- **Project-Based Memory System** (memory.md, context.json, embeddings.db per pengguna)

### 5.2 Di Luar Scope (v1.0)

- Integrasi langsung dengan Sistem Informasi Sekolah (SIS)
- Konten video pembelajaran produksi sendiri
- Marketplace konten pihak ketiga
- Fitur komunikasi real-time antar siswa (chat/forum)
- Sertifikasi resmi terakreditasi

### 5.3 Asumsi

- Perangkat pengguna memiliki browser modern (Chrome 90+, Firefox 88+, Safari 14+)
- Koneksi internet minimal 3G untuk sesi aktif; fitur offline tersedia via Service Worker
- Konten kurikulum disesuaikan dengan Kurikulum Merdeka Belajar

---

## 6. Fitur & Persyaratan Fungsional

### 6.1 Modul Onboarding & Profiling

**FR-001: Adaptive Interest Scanner**

- Sistem menampilkan kuis interaktif (≤ 10 pertanyaan) untuk memetakan minat dan gaya belajar
- Output: profil `interests` dan `learning_styles` tersimpan di database
- AI merekomendasikan topik awal berdasarkan hasil scanning

**FR-002: Registrasi & Autentikasi**

- Pendaftaran via email/password atau SSO institusi
- Verifikasi email wajib sebelum akses penuh
- Role-based access: `siswa`, `guru`, `admin`

### 6.2 Modul Knowledge Map

**FR-003: Visualisasi Peta Pengetahuan**

- Antarmuka berbentuk konstelasi bintang interaktif (bukan daftar bab linear)
- Setiap "planet" merepresentasikan topik dengan indikator penguasaan visual
- Pengguna dapat menjelajahi topik secara non-linear

**FR-004: Indeks Pengetahuan**

- Kategorisasi konten: Populer, Baru, Belum Dipelajari
- Filter dan pencarian topik

### 6.3 Modul Adaptive Learning

**FR-005: AI-Driven Adaptive Pathway**

- AI menyusun `learning_paths` dan `missions` secara personal berdasarkan profil pengguna
- Penyesuaian `difficulty_level` berdasarkan kecepatan dan akurasi jawaban real-time
- Dynamic Re-routing: AI menambah *remedial mission* jika penguasaan di bawah ambang

**FR-006: Real-Time Personalization Engine**

- Setiap interaksi (klik, jeda, revisi) dicatat di tabel `cognitive_traces`
- Engine mendeteksi pola menebak vs pemahaman sejati
- Penyesuaian urutan misi secara otomatis

### 6.4 Modul Assessment

**FR-007: Knowledge Tree Assessment**

- Evaluasi struktur logika jawaban menggunakan Abstract Syntax Tree
- Mendukung tipe soal: pilihan ganda, esai singkat, drag-and-drop konsep
- `structure_answer` disimpan dalam format JSON untuk analisis mendalam
- Kegagalan parsial memicu pemberian petunjuk spesifik secara progresif

**FR-008: Intelligent Assessment (Knowledge Tracing)**

- Algoritma Knowledge Tracing memperkirakan probabilitas penguasaan konsep
- Threshold penguasaan ≥ 80% untuk lanjut ke topik berikutnya
- Pengguna dapat mengulang misi dengan konfigurasi soal berbeda

### 6.5 Modul Pause & Ask AI

**FR-009: NLP-Based Contextual Help**

- Tombol "Pause & Ask" tersedia di setiap layar quiz dan materi
- AI membekukan tampilan saat diaktifkan (tidak mengganggu progres)
- Sistem memproses pertanyaan dalam konteks materi yang sedang dipelajari
- Jawaban AI mengacu pada `question_bank.explanation` yang relevan
- Fitur "Hentikan Lalu Tanya" mencerna keraguan kontekstual via NLP

### 6.6 Modul Gamifikasi

**FR-010: Sistem Poin, Lencana & Level**

- Setiap misi selesai memberikan `xp_reward` sesuai tingkat kesulitan
- Lencana (`badges`) diberikan adaptif berdasarkan pencapaian spesifik (contoh: "Ninja Fokus", "Penjelajah Konsep")
- Level naik berdasarkan akumulasi XP dengan threshold di tabel `levels`
- Kriteria lencana dapat berupa `xp_threshold`, `streak`, atau kriteria AI dinamis

**FR-011: Karakter 2D untuk Quiz**

- Karakter visual yang dapat dikustomisasi (costume, aura, topwear, bottomwear)
- Karakter bereaksi terhadap jawaban benar/salah secara animatif
- Item karakter dibuka melalui pencapaian milestone tertentu

**FR-012: Papan Peringkat (Leaderboard)**

- Leaderboard berbasis topik/minat, bukan global semata
- Mendukung grup/kelas untuk kompetisi sehat antar teman sebaya

### 6.7 Modul Refleksi & Metakognisi

**FR-013: Metacognitive Dashboard**

- Peta panas visualisasi area kebingungan (confusion heatmap)
- Saran strategi belajar personal berdasarkan `learning_style_id`
- Rekap progres: topik dikuasai, area lemah, waktu belajar efektif

**FR-014: Laporan Perkembangan**

- AI-Generated Narrative Report: laporan naratif personal dari data `users`, `missions`, `badges`, `levels`, dan `cognitive_traces`
- Ekspor laporan dalam format PDF untuk kebutuhan guru
- Visualisasi grafik pertumbuhan kompetensi

### 6.8 Modul Guru (Dashboard Analitik)

**FR-015: Teacher Dashboard**

- Pemantauan kemajuan seluruh siswa di kelas real-time
- Filter per topik, per siswa, per rentang waktu
- Notifikasi otomatis jika siswa tertentu mengalami stagnasi signifikan
- Ekspor data batch untuk pelaporan sekolah

### 6.9 Modul Scheduler

**FR-016: Continuous Learning Scheduler**

- AI menjadwalkan sesi belajar berikutnya berdasarkan pola waktu optimal pengguna
- Notifikasi pengingat (push notification via PWA)
- Pengaturan `learning_paths.is_active` otomatis sesuai jadwal

---

## 7. Project-Based Memory System

### 7.1 Konsep & Motivasi

Mayoritas platform AI bersifat stateless antar sesi: setiap kali pengguna kembali, AI tidak mengenal konteks sebelumnya. MetaLearn memecahkan ini melalui **Project-Based Memory System** — sebuah lapisan memori persisten berbasis file yang hidup bersama proyek belajar pengguna, bukan di cloud yang tidak transparan.

Setiap pengguna memiliki direktori memori pribadi (`.ai/`) yang berisi tiga komponen inti. AI Gemini membaca lapisan ini di setiap sesi untuk memulihkan konteks secara instan.

### 7.2 Struktur File Memory

```
metalearn-user-{id}/
├── .ai/
│   ├── memory.md          # Narasi memori manusiawi — ringkasan progres,
│   │                      # preferensi gaya belajar, topik sulit, catatan guru
│   ├── context.json       # Snapshot konteks terstruktur — state sesi terakhir,
│   │                      # misi aktif, skor penguasaan per topik, XP terkini
│   └── embeddings.db      # Vector database ringan (SQLite + pgvector) —
│                          # embedding semantik dari seluruh riwayat interaksi
│                          # untuk retrieval konteks relevan via RAG
├── progress/
│   ├── missions_log.json  # Log penyelesaian misi per sesi
│   └── traces/            # Cognitive trace files per misi
└── assets/
    └── character.json     # Konfigurasi karakter 2D pengguna
```

### 7.3 Anatomi Setiap Komponen

#### `memory.md` — Memori Naratif

File Markdown yang ditulis dan diperbarui oleh AI secara otomatis setelah setiap sesi selesai. Dirancang agar mudah dibaca manusia (guru, wali, pengguna sendiri).

```markdown
# Memori Belajar: Budi Santoso
**Terakhir diperbarui:** 2026-06-24 20:15 WIB

## Profil Singkat
- Gaya belajar dominan: Visual-Kinestetik
- Topik favorit: Aljabar, Geometri
- Topik yang masih sulit: Trigonometri (sesi 4–6 konsisten menunjukkan kebingungan)

## Progres Terkini
- Misi selesai minggu ini: 8 dari 10 target
- XP minggu ini: +340 (total: 2.840)
- Lencana baru: "Penjelajah Konsep" (diraih 2026-06-23)

## Catatan Penting
- Sesi 2026-06-20: Siswa menggunakan Pause & Ask 5x pada topik sin/cos/tan
- Guru merekomendasikan remedial unit "Lingkaran Satuan" sebelum lanjut
- Waktu belajar paling efektif: pukul 19.00–21.00 WIB
```

#### `context.json` — Snapshot Konteks Terstruktur

JSON yang diinject ke prompt AI di awal setiap sesi. Berisi state machine belajar pengguna yang bisa diparse secara programatik.

```json
{
  "user_id": "usr_8472",
  "session_count": 14,
  "last_session": "2026-06-24T20:15:00+07:00",
  "active_learning_path": {
    "id": "lp_math_trigonometry",
    "name": "Trigonometri Dasar",
    "progress_pct": 42,
    "current_mission_id": "msn_unit_circle_intro"
  },
  "mastery_scores": {
    "aljabar_linear": 0.91,
    "geometri_bidang": 0.87,
    "trigonometri": 0.38
  },
  "gamification": {
    "total_xp": 2840,
    "level": 7,
    "active_badges": ["penjelajah_konsep", "ninja_fokus"],
    "streak_days": 5
  },
  "ai_flags": {
    "confusion_zones": ["trigonometri.sin_cos", "trigonometri.identitas"],
    "learning_style_id": "visual_kinesthetic",
    "preferred_session_duration_min": 35,
    "pause_ask_frequency": "high"
  }
}
```

#### `embeddings.db` — Vector Database Lokal

Database SQLite yang dilengkapi ekstensi vector (sqlite-vec atau pgvector via PostgreSQL). Menyimpan embedding semantik dari seluruh riwayat interaksi pengguna untuk digunakan dalam **Retrieval-Augmented Generation (RAG)**.

```sql
-- Skema tabel embeddings
CREATE TABLE memory_chunks (
    id          INTEGER PRIMARY KEY,
    user_id     TEXT NOT NULL,
    source_type TEXT,           -- 'session', 'question', 'feedback', 'trace'
    content     TEXT NOT NULL,  -- teks asli
    embedding   BLOB NOT NULL,  -- vector float32[768]
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_user ON memory_chunks(user_id);
```

Saat pengguna mengajukan pertanyaan via Pause & Ask AI, sistem melakukan similarity search ke `embeddings.db` untuk mengambil konteks historis paling relevan sebelum memanggil Gemini API.

### 7.4 Alur Kerja Memory System

```
┌─────────────────────────────────────────────────────────────────┐
│                    ALUR PROJECT-BASED MEMORY                    │
└─────────────────────────────────────────────────────────────────┘

[SESI DIMULAI]
     │
     ▼
┌──────────────────┐
│ Baca context.json│ ──► Inject ke system prompt Gemini
│ Baca memory.md   │ ──► Tambah sebagai "user background"
└──────────────────┘
     │
     ▼
┌──────────────────────────────────┐
│ Similarity Search embeddings.db  │
│ (top-5 chunk paling relevan)     │ ──► Masuk ke RAG context window
└──────────────────────────────────┘
     │
     ▼
┌────────────────────────────────────────────────────────────────┐
│                   SESI BELAJAR AKTIF                           │
│                                                                │
│  User (Browser)  ──►  React + Vite Frontend                   │
│        ↕                      ↕                               │
│  Laravel Backend  ◄──►  WebSocket (Laravel Reverb)            │
│        ↕                      ↕                               │
│  Gemini API  ◄──────────────────────────────                   │
│        ↕                                                      │
│  PostgreSQL / Redis (state sesi)                               │
└────────────────────────────────────────────────────────────────┘
     │
     ▼
[SESI SELESAI — Memory Writer berjalan otomatis]
     │
     ├──► Update context.json (state terbaru)
     ├──► Append memory.md (ringkasan sesi via Gemini)
     └──► Embed chunk baru ke embeddings.db
```

### 7.5 Persyaratan Fungsional Memory System

**FR-017: Memory Initialization**

- Saat akun baru dibuat, sistem men-generate struktur `.ai/` awal dengan nilai default
- `context.json` diisi dari hasil Adaptive Interest Scanner (onboarding)
- `memory.md` diisi dengan narasi profil awal dari data onboarding

**FR-018: Context Injection**

- Di setiap request ke Gemini API, backend Laravel mengambil `context.json` dan `memory.md` pengguna aktif
- Top-5 embedding chunk paling relevan dari `embeddings.db` disertakan dalam context window
- Total token injected ≤ 2.000 token untuk efisiensi biaya API

**FR-019: Post-Session Memory Update**

- Setelah sesi berakhir (atau pengguna tidak aktif > 5 menit), Memory Writer Service dipicu
- Gemini menghasilkan ringkasan sesi dalam format Markdown dan di-append ke `memory.md`
- `context.json` diperbarui dengan state terkini (XP, misi, skor penguasaan)
- Chunk baru dari sesi di-embed dan disimpan ke `embeddings.db`

**FR-020: Memory Export & Transparency**

- Pengguna dan guru dapat mengunduh `memory.md` kapan saja dari profil
- Pengguna dapat mereset atau menghapus memori tertentu (GDPR-compliant)
- Audit log perubahan memori tersedia selama 90 hari

**FR-021: Memory Storage di Cloudflare R2 / MinIO**

- File `.ai/memory.md` dan `.ai/context.json` disimpan di object storage (Cloudflare R2 atau MinIO self-hosted)
- `embeddings.db` disinkronkan ke S3-compatible storage setiap akhir sesi
- Enkripsi at-rest AES-256 wajib untuk seluruh file memory

### 7.6 KPI Tambahan

| Metrik | Target |
|--------|--------|
| Waktu pemulihan konteks sesi (context load time) | < 300ms |
| Akurasi RAG retrieval (relevansi chunk) | ≥ 85% (dinilai sampel) |
| Ukuran `embeddings.db` per pengguna setelah 6 bulan | < 50MB |
| Pengguna yang menilai "AI mengenal saya" positif | ≥ 75% (survei) |

---

## 8. Persyaratan Non-Fungsional

### 7.1 Performa

| Parameter | Target |
|-----------|--------|
| First Contentful Paint (FCP) | < 1.5 detik |
| Time to Interactive (TTI) | < 3 detik (koneksi 3G) |
| API response time (AI inference) | < 2 detik (p95) |
| Uptime | ≥ 99.5% |

### 7.2 Keamanan & Privasi

- Enkripsi data pengguna at-rest dan in-transit (AES-256, TLS 1.3)
- Kepatuhan terhadap regulasi perlindungan data anak (UU PDP Indonesia)
- Hashing password menggunakan bcrypt atau Argon2
- Audit bias algoritma rutin untuk memastikan fairness rekomendasi
- Tidak ada penjualan data pengguna kepada pihak ketiga

### 7.3 Aksesibilitas

- Kompatibilitas lintas peramban: Chrome, Firefox, Safari, Edge
- Responsif untuk perangkat mobile (320px), tablet (768px), dan desktop (1024px+)
- Dukungan pembaca layar (ARIA labels) untuk inklusivitas
- Mode offline via Service Worker PWA untuk area dengan koneksi terbatas

### 7.4 Skalabilitas

- Arsitektur mampu menangani 10.000 pengguna konkuren pada fase awal
- Desain database mendukung horizontal scaling
- CDN untuk aset statis guna mengurangi latensi lintas geografis

---

## 9. Arsitektur & Stack Teknologi

### 9.1 Frontend

| Komponen | Teknologi |
|----------|-----------|
| Framework | React.js + Vite (PWA-ready, fast HMR) |
| State Management | Zustand / Redux Toolkit |
| Styling | Tailwind CSS |
| Animasi Karakter 2D | PixiJS / Spine2D |
| Visualisasi Data | D3.js / Recharts |
| Offline Support | Service Worker + IndexedDB |

### 9.2 Backend

| Komponen | Teknologi |
|----------|-----------|
| Framework | Laravel 11 (PHP 8.3) |
| Database | PostgreSQL 16 (relasional) |
| Cache | Redis 7 |
| Real-Time | WebSocket via Laravel Reverb |
| Queue | Laravel Horizon + Redis |
| AI Integration | Gemini API (Google) |
| Knowledge Tracing | BKT (Bayesian Knowledge Tracing) — service PHP/Python |
| Abstract Syntax Tree | Custom PHP parser + JS Esprima |

### 9.3 Storage & Infrastructure

| Komponen | Teknologi |
|----------|-----------|
| Object Storage (S3) | Cloudflare R2 / MinIO (self-hosted) |
| Memory Files (.ai/) | Cloudflare R2 / MinIO — enkripsi AES-256 |
| Container | Docker + Docker Compose |
| CI/CD | GitHub Actions |
| Monitoring | Prometheus + Grafana |
| Vector DB (lokal) | SQLite + sqlite-vec (embeddings.db) |

### 9.4 Diagram Arsitektur Lengkap

```
┌──────────────────────────────────────────────────────────────────────┐
│                    CLIENT LAYER                                      │
│         React + Vite (PWA) — Tailwind CSS — PixiJS — D3.js          │
│                Service Worker (offline support)                      │
└─────────────────────────────┬────────────────────────────────────────┘
                              │ HTTPS / WSS
┌─────────────────────────────▼────────────────────────────────────────┐
│                    LARAVEL BACKEND (API + Queue)                     │
│                                                                      │
│  ┌──────────────┐  ┌───────────────┐  ┌──────────────────────────┐  │
│  │ Auth Service │  │  Core App API │  │  Memory Writer Service   │  │
│  │ (JWT/Sanctum)│  │  (REST + WS)  │  │  (Post-session updater)  │  │
│  └──────┬───────┘  └───────┬───────┘  └──────────┬───────────────┘  │
│         │                  │                      │                  │
│  ┌──────▼──────────────────▼──────────────────────▼───────────────┐  │
│  │            LARAVEL REVERB (WebSocket Server)                   │  │
│  └────────────────────────────────────────────────────────────────┘  │
└────────┬────────────────────┬────────────────────┬───────────────────┘
         │                    │                    │
┌────────▼───────┐  ┌─────────▼────────┐  ┌───────▼────────────────────┐
│  PostgreSQL 16 │  │   Redis Cache    │  │   Gemini API (Google AI)   │
│  (Primary DB)  │  │  (Session/Queue) │  │   ┌────────────────────┐   │
│                │  │                  │  │   │ context.json inject │   │
│  - users       │  │  - active users  │  │   │ memory.md inject   │   │
│  - missions    │  │  - leaderboard   │  │   │ RAG dari embeddings│   │
│  - progress    │  │  - realtime XP   │  │   └────────────────────┘   │
│  - traces      │  │                  │  └────────────────────────────┘
└────────────────┘  └──────────────────┘
         │
┌────────▼─────────────────────────────────────────────────────────────┐
│               OBJECT STORAGE — Cloudflare R2 / MinIO                │
│                                                                      │
│   user-{id}/.ai/memory.md          (memori naratif per pengguna)    │
│   user-{id}/.ai/context.json       (snapshot konteks terstruktur)   │
│   user-{id}/.ai/embeddings.db      (vector DB lokal, sync S3)       │
│   user-{id}/assets/character.json  (konfigurasi karakter 2D)        │
│   shared/media/                    (aset materi — gambar, audio)    │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 10. Alur Pengguna (User Flow)

### 9.1 Alur Utama Siswa (12 Langkah)

```
[1] PEMINDAIAN MINAT & PROFIL BELAJAR
    └─ Kuis interaktif → profil interests + learning_styles tersimpan

[2] PENENTUAN KONTEKS & JALUR BELAJAR
    └─ Knowledge Map (konstelasi visual) → pilih topik secara non-linear

[3] MENJALANKAN PEMBELAJARAN ADAPTIF
    └─ Materi mengalir dinamis → cabang pengetahuan terbuka per interaksi

[4] DETEKSI KEBINGUNGAN
    ├─ Kebingungan terdeteksi → [5] TANTANGAN KONSEPTUAL
    └─ Tidak ada kebingungan → lanjut ke [8]

[5] TANTANGAN KONSEPTUAL
    └─ Knowledge Tree Assessment → evaluasi struktur logika

[6] MENGANALISIS PROSES BERPIKIR
    └─ Cognitive Trace Recorder → catat klik, jeda, revisi

[7] MEMBERIKAN UMPAN BALIK REAL-TIME
    └─ Adaptive Feedback Engine → penjelasan spesifik berdasarkan pola kesalahan

[8] MENCATAT POIN, LENCANA & LEVEL
    └─ Distribusi reward → XP, badges adaptif, naik level

[9] MEREFLEKSIKAN PROGRES & METAKOGNISI
    └─ Metacognitive Dashboard → peta panas kebingungan + saran strategi

[10] PENGECEKAN JALUR BELAJAR
    ├─ Belum selesai → kembali ke [3]
    └─ Selesai → [11]

[11] MENAMPILKAN LAPORAN PERKEMBANGAN
    └─ AI-Generated Narrative Report → grafik pertumbuhan + rekomendasi

[12] SELESAI
    └─ Continuous Learning Scheduler → jadwalkan sesi berikutnya
```

### 9.2 Alur Pause & Ask AI

```
Pengguna menemui kebingungan saat belajar
    └─ Klik tombol "Pause & Ask"
        └─ Tampilan dibekukan (progres tetap tersimpan)
            └─ Pengguna mengetik pertanyaan
                └─ NLP Engine memproses dalam konteks materi aktif
                    └─ AI memberikan klarifikasi + contoh relevan
                        └─ Pengguna menutup panel
                            └─ Tampilan kembali, belajar dilanjutkan
```

---

## 11. Desain Database (ERD)

### 10.1 Entitas Utama

```
users
├── id (PK)
├── name
├── email
├── password_hash
├── role_id (FK → roles)
├── learning_style_id (FK → learning_styles)
├── created_at
└── is_active

roles
├── id (PK)
├── name
└── description

learning_styles
├── id (PK)
├── code
├── name
└── description

interests
├── id (PK)
├── name
├── icon
└── color

topics
├── id (PK)
├── name
├── description
├── icon
├── color_hex
└── category

learning_paths
├── id (PK)
├── topic_id (FK → topics)
├── name
├── difficulty_level
├── description
├── sequence_order
└── is_active

missions
├── id (PK)
├── learning_path_id (FK → learning_paths)
├── title
├── type (enum)
├── difficulty (tinyint)
├── xp_reward
├── estimated_minutes
└── sequence_order

question_bank
├── id (PK)
├── mission_id (FK → missions)
├── type (enum)
├── question_text
├── correct_answer
├── explanation
└── xp_value

answer_options
├── id (PK)
├── question_id (FK → question_bank)
├── option_text
└── is_correct

badges
├── id (PK)
├── name
├── description
├── icon
├── criteria_type (enum)
└── criteria_value

levels
├── id (PK)
├── level_number
├── title
├── min_xp
├── max_xp
└── description
```

### 10.2 Tabel Tambahan (Tracking & Gamifikasi)

```
user_interests (pivot)
├── user_id (FK)
└── interest_id (FK)

user_progress
├── id (PK)
├── user_id (FK)
├── mission_id (FK)
├── status (enum: not_started/in_progress/completed/failed)
├── score
├── xp_earned
├── attempts
└── completed_at

cognitive_traces
├── id (PK)
├── user_id (FK)
├── question_id (FK)
├── action_type (enum: click/pause/revise/submit)
├── duration_ms
├── payload (JSON)
└── recorded_at

user_badges (pivot)
├── user_id (FK)
├── badge_id (FK)
└── earned_at

user_level
├── user_id (FK, PK)
├── current_xp
├── level_id (FK)
└── updated_at
```

---

## 12. Kontribusi AI

### 12.1 Gemini sebagai AI Engine Utama

MetaLearn menggunakan **Google Gemini** sebagai model AI primer, dengan pertimbangan:

- Context window besar (Gemini 1.5 Pro: 1M token) mengakomodasi injeksi Project-Based Memory yang kaya
- Dukungan multimodal (teks, gambar, audio) relevan untuk konten visual dan soal berbasis gambar
- Biaya API kompetitif untuk skala pelajar Indonesia
- Tidak memerlukan VPN — API tersedia langsung dari infrastruktur Indonesia

Setiap request ke Gemini menyertakan tiga lapisan dari Project-Based Memory:

```
System Prompt Gemini
├── [1] context.json  → state belajar terkini (misi aktif, XP, skor penguasaan)
├── [2] memory.md     → narasi profil singkat + catatan sesi sebelumnya
└── [3] RAG chunks    → 5 embedding paling relevan dari embeddings.db
```

### 12.2 NLP untuk Pause & Ask AI

AI membekukan sesi aktif dan memproses pertanyaan dalam konteks transkrip materi spesifik yang sedang dipelajari. Jawaban kontekstual diberikan tanpa mengacaukan alur belajar yang sedang berjalan.

### 12.3 Knowledge Tree Assessment (Abstract Syntax Tree)

AI mengevaluasi struktur semantik pemikiran siswa menggunakan representasi pohon abstrak. Variasi jawaban dengan anatomi logika setara tetap divalidasi sebagai benar. Ini melampaui pencocokan teks sederhana menuju pemahaman struktur berpikir.

### 12.4 Dynamic Pathway Generation

AI mengambil alih navigasi pembelajaran berdasarkan akumulasi data `cognitive_traces`. Rute belajar disesuaikan secara real-time dengan ritme kognitif individu, mereduksi beban memori berlebih.

### 12.5 Gamifikasi Dinamis & Kalibrasi Otonom

Large Language Models mengkalibrasi tingkat rintangan dan distribusi lencana secara otomatis. Lencana bersifat adaptif dengan kriteria dinamis, mempertimbangkan konsistensi, pola fokus, dan gaya belajar.

---

## 13. Gamifikasi & Motivasi

### 12.1 Fondasi Teori

Platform dibangun di atas **Self-Determination Theory (SDT)** yang mencakup tiga kebutuhan psikologis dasar:

| Kebutuhan | Implementasi di MetaLearn |
|-----------|--------------------------|
| **Otonomi** | Peta pengetahuan non-linear, pemilihan topik bebas |
| **Kompetensi** | Dynamic Difficulty Adjustment, progress indicator visual |
| **Keterhubungan** | Leaderboard minat, pencapaian bersama |

### 12.2 Loop Gamifikasi

```
Aksi Belajar → XP Reward → Naik Level → Buka Konten/Karakter Baru
     ↑                                              ↓
     └──────── Tantangan Baru Disesuaikan AI ───────┘
```

### 12.3 Sistem Lencana Adaptif

Lencana tidak hanya diberikan berdasarkan penyelesaian misi. AI menganalisis pola perilaku untuk memberikan lencana kontekstual:

- **"Ninja Fokus"** → sesi tanpa interupsi ≥ 30 menit
- **"Penjelajah Konsep"** → menjelajahi ≥ 5 topik berbeda dalam seminggu
- **"Pantang Menyerah"** → melakukan revisi ≥ 3 kali sebelum benar
- **"Guru Kecil"** → skor sempurna pada topik tertentu 3 kali berturut-turut

---

## 14. Dampak & Keberlanjutan

### 13.1 Dampak Pendidikan

Platform menghancurkan rutinitas belajar kaku melalui Knowledge Tree Assessment dan Dynamic Re-routing. Siswa tidak lagi menghafal, tetapi mengembangkan berpikir analitis-logis. Keadilan distribusi pengetahuan lintas geografis tercapai melalui aksesibilitas PWA offline.

### 13.2 Dampak Psikologis

Integrasi gamifikasi dinamis meledakkan gairah eksplorasi siswa. Pause & Ask AI dan kalibrasi tingkat kesulitan otomatis mengurai beban kognitif berlebih, mentransformasi kelas maya menjadi arena perayaan intelektual.

### 13.3 Dampak Sosial

Fitur kolaboratif (pencapaian bersama, leaderboard berbasis minat) merajut solidaritas komunal. AI berperan sebagai katalis perekat empati antar pengguna.

### 13.4 Strategi Keberlanjutan

1. **Kemitraan strategis** dengan institusi akademik untuk integrasi kurikulum
2. **Pembaruan periodik** mengikuti tren teknologi pendidikan dan kebutuhan siswa
3. **Perluasan validasi** lintas sekolah dan departemen dengan data heterogen
4. **Fusi rekam jejak alumni** ke dalam kerangka AI untuk rekomendasi karir
5. **PWA offline-first** untuk merobohkan hambatan geografis dan infrastruktur
6. **Privasi & audit algoritma** rutin untuk memastikan fairness rekomendasi

---

## 15. Aspek STEM

### 14.1 Science (Sains)

Fondasi psikologi kognitif dan neurosains pendidikan. Teori Determinasi Diri menjadi basis desain reward adaptif. Analisis beban kognitif real-time mencegah stagnasi mental.

### 14.2 Technology (Teknologi)

PWA dengan AI generatif dan NLP. Algoritma knowledge tracing dinamis mempersonalisasi jalur belajar secara real-time. Kompatibel lintas peramban dengan adaptasi antarmuka mandiri.

### 14.3 Engineering (Rekayasa)

Arsitektur berlapis dengan Knowledge Tree Assessor berbasis Abstract Syntax Tree. Desain antarmuka mengadopsi prinsip game mechanics. Integrasi ERD solid memungkinkan dynamic re-routing dan remedial mission.

### 14.4 Mathematics (Matematika)

- **Probabilitas:** Deteksi kebingungan via kalkulasi probabilistic
- **Statistika:** Standar deviasi dan rerata untuk ambang batas kesulitan fluktuatif
- **Regresi linear:** Kalibrasi distribusi poin XP dan level
- **Matriks performa:** Distribusi tantangan presisi sesuai ritme individual

---

## 16. Risiko & Mitigasi

| Risiko | Tingkat | Mitigasi |
|--------|---------|----------|
| Bias algoritma AI merekomendasikan konten tidak merata | Tinggi | Audit bias rutin, dataset training yang representatif dan beragam |
| Ketergantungan berlebih pada AI tanpa pemahaman siswa | Sedang | Knowledge Tree Assessment yang mengevaluasi struktur berpikir, bukan sekadar output jawaban |
| Privasi data anak di bawah umur | Tinggi | Kepatuhan UU PDP, enkripsi AES-256, kebijakan privasi ketat, tidak ada monetisasi data |
| Koneksi internet tidak stabil di daerah terpencil | Tinggi | PWA dengan Service Worker untuk mode offline penuh |
| Resistensi adopsi dari guru tradisional | Sedang | Pelatihan penggunaan, antarmuka guru yang sederhana, onboarding bertahap |
| Overengineering pada fase MVP | Sedang | Scope yang jelas, iterasi agile, prioritas fitur berdasarkan impact vs effort |
| Pertumbuhan ukuran embeddings.db tidak terkendali | Sedang | Batasan ukuran 50MB per user, pruning chunk lama setelah 6 bulan, kompresi vector |
| Kebocoran data memori pengguna dari object storage | Tinggi | Enkripsi AES-256 at-rest, akses berbasis signed URL dengan TTL pendek, audit log akses |
| Biaya Gemini API melonjak seiring skala pengguna | Sedang | Batasan token injeksi ≤ 2.000 token per request, caching respons umum via Redis |

---

## 17. Referensi

- Ditha, J. D., et al. (2026). AI-BASED GAMIFICATION IN LEARNING. *LEARNING*, 6(1), 99–110. https://doi.org/10.51878/learning.v6i1.8902
- Kadam, A. J., et al. (2025). Personalized Learning Paths for Student Progression. *Cureus Journal of Computer Science*. https://doi.org/10.7759/s44389-024-02275-z
- Niyazova, G. Z., et al. (2026). The effects of gamified AI-supported digital learning environments. *Frontiers in Education*, Volume 11-2026.
- Putri, M. V., et al. (2026). Analisis Gamifikasi Fill-in-the-Blank dengan Evaluasi Otomatis Abstract Syntax Tree. *Jutisi*, 14(3), 2281. https://doi.org/10.35889/jutisi.v14i3.3250
- Qianyu Sun, et al. (2026). Adaptive Knowledge Tracing Through Multi-Agent Reinforcement Learning. *Frontiers in Applied Physics and Mathematics*, 3(1), 16–28.
- Vadakattu, A., et al. (2026). PROGRESSIVE WEB APPLICATION (PWA) WITH A "PAUSE-AND-ASK" AI. *IJPREMS*, 6(4). https://doi.org/10.58257/IJPREMS52478

---

*Dokumen ini merupakan milik Tim NexaNode — Universitas Muria Kudus. Dibuat untuk keperluan kompetisi Samsung Solve for Tomorrow 2026.*
