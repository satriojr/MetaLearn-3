# MetaLearn 🎓

> **Platform Pembelajaran Adaptif Berbasis AI untuk Siswa Sekolah Menengah Indonesia**

[![Samsung SFT 2026](https://img.shields.io/badge/Samsung_Solve_for_Tomorrow-2026-blue?style=flat-square)](https://www.samsung.com/id/)
[![Tim NexaNode](https://img.shields.io/badge/Tim-NexaNode-green?style=flat-square)]()
[![Universitas Muria Kudus](https://img.shields.io/badge/Universitas-Muria_Kudus-orange?style=flat-square)]()
[![Status](https://img.shields.io/badge/Status-Concept_Paper-yellow?style=flat-square)]()
[![PWA](https://img.shields.io/badge/Platform-PWA-purple?style=flat-square)]()
[![Laravel](https://img.shields.io/badge/Backend-Laravel_11-red?style=flat-square)]()
[![Gemini](https://img.shields.io/badge/AI-Gemini-4285F4?style=flat-square)]()
[![License](https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square)]()

---

## Tentang MetaLearn

**MetaLearn** adalah Progressive Web Application (PWA) berbasis AI yang menggabungkan empat pilar:

- 🤖 **Adaptive Learning** — jalur belajar yang dikalibrasi AI secara real-time sesuai kecepatan kognitif individu
- 🎮 **Gamification** — poin XP, lencana adaptif, dan level yang mendukung Self-Determination Theory
- 💬 **NLP (Pause & Ask AI)** — klarifikasi kontekstual instan tanpa mengganggu alur belajar
- 🧠 **Project-Based Memory** — memori persisten berbasis file yang membuat AI mengingat konteks antar sesi

Dibangun sebagai respons terhadap posisi Indonesia di peringkat **ke-72 dari 78 negara** pada PISA 2022 (skor matematika: 379), MetaLearn hadir untuk menggantikan metode pengajaran satu arah yang kaku dengan ekosistem belajar yang personal, interaktif, dan inklusif.

---

## Daftar Isi

- [Fitur Unggulan](#fitur-unggulan)
- [Project-Based Memory System](#project-based-memory-system)
- [Demo & Wireframe](#demo--wireframe)
- [Arsitektur Sistem](#arsitektur-sistem)
- [Struktur Database](#struktur-database)
- [Instalasi & Setup](#instalasi--setup)
- [Penggunaan](#penggunaan)
- [Alur Pengguna](#alur-pengguna)
- [Kontribusi AI](#kontribusi-ai)
- [Tim Pengembang](#tim-pengembang)
- [Referensi](#referensi)
- [Lisensi](#lisensi)

---

## Fitur Unggulan

### 🔍 1. Adaptive Interest Scanner
Kuis interaktif onboarding yang memetakan minat dan gaya belajar setiap siswa. Output berupa profil `interests` dan `learning_styles` yang menjadi fondasi rekomendasi AI.

### 🗺️ 2. Knowledge Map Interaktif
Peta pengetahuan berbentuk konstelasi bintang visual. Pengguna menjelajahi "planet" topik secara non-linear, menolak urutan instruksi kaku yang mematikan kebebasan berekspresi.

### 🧠 3. AI-Driven Adaptive Pathway
AI menyusun `learning_paths` dan `missions` secara personal. Tingkat kesulitan (`difficulty_level`) disesuaikan real-time berdasarkan kecepatan dan akurasi jawaban. Jika penguasaan kurang, AI otomatis menambahkan *remedial mission*.

### ⏸️ 4. Pause & Ask AI (NLP)
Tombol instan yang membekukan sesi tanpa kehilangan progres. AI memproses pertanyaan dalam konteks materi aktif dan memberikan klarifikasi via NLP. Tidak ada disrupsi fokus.

### 🌳 5. Knowledge Tree Assessment
Evaluasi berbasis **Abstract Syntax Tree** — menguji *struktur logika berpikir*, bukan sekadar pencocokan kata kunci. Variasi jawaban dengan anatomi logika setara tetap divalidasi benar.

### 📊 6. Cognitive Trace Recorder
Setiap klik, jeda, dan revisi jawaban dicatat di tabel `cognitive_traces`. AI mendeteksi pola menebak vs pemahaman sejati untuk kalibrasi personalisasi lebih presisi.

### 🏆 7. Gamifikasi Dinamis
- **XP & Level** — akumulasi poin berdasarkan penyelesaian dan kualitas jawaban
- **Lencana Adaptif** — diberikan AI berdasarkan perilaku spesifik (bukan hanya threshold statis)
- **Karakter 2D** — avatar yang dapat dikustomisasi (costume, aura, topwear, bottomwear)
- **Leaderboard berbasis minat** — kompetisi sehat antar teman sebaya

### 🪞 8. Metacognitive Dashboard
Peta panas area kebingungan, saran strategi belajar personal, dan rekap kompetensi. Siswa belajar *cara belajar*, bukan hanya konten.

### 📝 9. AI-Generated Narrative Report
Laporan naratif personal yang dikompilasi AI dari data `users`, `missions`, `badges`, `levels`, dan `cognitive_traces`. Tersedia untuk guru dalam format ekspor.

### 📅 10. Continuous Learning Scheduler
AI menjadwalkan sesi berikutnya berdasarkan pola waktu optimal pengguna. Pengingat via push notification PWA.

### 🧠 11. Project-Based Memory System
Setiap pengguna memiliki direktori memori persisten (`.ai/`) yang berisi `memory.md` (narasi belajar), `context.json` (snapshot state), dan `embeddings.db` (vector DB lokal). AI Gemini membaca lapisan ini di setiap sesi — tidak ada lagi "perkenalan ulang" setiap kali belajar.

---

## Project-Based Memory System

Fitur pembeda terkuat MetaLearn. Platform AI konvensional bersifat stateless — AI "lupa" pengguna setiap sesi baru. MetaLearn memecah paradigma ini.

### Struktur File Memory

```
metalearn-user-{id}/
├── .ai/
│   ├── memory.md          # Narasi memori manusiawi — ringkasan progres,
│   │                      # preferensi gaya belajar, topik sulit, catatan guru
│   ├── context.json       # Snapshot konteks terstruktur — state sesi terakhir,
│   │                      # misi aktif, skor penguasaan per topik, XP terkini
│   └── embeddings.db      # Vector database ringan (SQLite + sqlite-vec) —
│                          # embedding semantik dari seluruh riwayat interaksi
│                          # untuk retrieval konteks relevan via RAG
├── progress/
│   ├── missions_log.json
│   └── traces/
└── assets/
    └── character.json
```

### `memory.md` — Memori Naratif (contoh)

```markdown
# Memori Belajar: Budi Santoso
**Terakhir diperbarui:** 2026-06-24 20:15 WIB

## Profil Singkat
- Gaya belajar dominan: Visual-Kinestetik
- Topik sulit: Trigonometri (kebingungan persisten sesi 4–6)
- Waktu belajar paling efektif: 19.00–21.00 WIB

## Progres Terkini
- Misi selesai minggu ini: 8 dari 10 target
- XP minggu ini: +340 (total: 2.840)
- Lencana baru: "Penjelajah Konsep"

## Catatan Penting
- Sesi 2026-06-20: Pause & Ask digunakan 5x pada topik sin/cos/tan
- Guru merekomendasikan remedial "Lingkaran Satuan" sebelum lanjut
```

### `context.json` — Snapshot Terstruktur (contoh)

```json
{
  "user_id": "usr_8472",
  "session_count": 14,
  "last_session": "2026-06-24T20:15:00+07:00",
  "active_learning_path": {
    "id": "lp_math_trigonometry",
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
    "streak_days": 5
  },
  "ai_flags": {
    "confusion_zones": ["trigonometri.sin_cos"],
    "learning_style_id": "visual_kinesthetic",
    "pause_ask_frequency": "high"
  }
}
```

### Alur Kerja Memory + Gemini

```
[SESI DIMULAI]
     │
     ▼
Baca context.json + memory.md  ──► Inject ke System Prompt Gemini
     │
     ▼
Similarity Search embeddings.db (top-5 chunk) ──► Masuk RAG context
     │
     ▼
[SESI BELAJAR AKTIF via Laravel Reverb WebSocket]
     │
     ▼
[SESI SELESAI — Memory Writer otomatis berjalan]
     ├──► Update context.json (state terbaru)
     ├──► Gemini generate ringkasan → append memory.md
     └──► Embed chunk baru → simpan ke embeddings.db
          └──► Sinkronisasi ke Cloudflare R2 / MinIO
```

### Storage Memory

File `.ai/` disimpan di **Cloudflare R2** atau **MinIO** (S3-compatible), terenkripsi AES-256. Pengguna dapat mengunduh atau menghapus memorinya kapan saja dari halaman profil (GDPR-compliant).

---

## Demo & Wireframe

### Mobile App Version

Antarmuka mobile dirancang dengan navigasi bawah (bottom navigation) yang intuitif:

| Beranda | Quiz | Ilmu | Arena | Profil |
|---------|------|------|-------|--------|
| Dashboard XP, misi selesai | XP, nama modul, soal, tombol Pause & Ask | Katalog modul & misi, indeks kategori | Kategori game & fitur game | Pencapaian & dashboard personal |

### Desktop App Version

Tata letak sidebar dengan konten utama di tengah. Dashboard guru tersedia di panel terpisah dengan akses analitik kelas penuh.

### Tablet Version

Layout responsif dengan grid 2-kolom untuk pengalaman belajar yang lebih luas.

---

## Arsitektur Sistem

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENT LAYER (PWA)                        │
│  React/Next.js + Tailwind + PixiJS + Service Worker         │
└─────────────────────────┬───────────────────────────────────┘
                          │ HTTPS
┌─────────────────────────▼───────────────────────────────────┐
│                    API GATEWAY                               │
│  REST API + WebSocket (real-time events)                    │
└─────┬───────────────────┬───────────────────┬───────────────┘
      │                   │                   │
┌─────▼──────┐  ┌─────────▼──────┐  ┌────────▼───────────────┐
│  Auth      │  │  Core App      │  │  AI/ML Service          │
│  Service   │  │  Service       │  │  (FastAPI/Python)       │
│  (JWT/SSO) │  │  (Node.js)     │  │  ┌──────────────────┐   │
└─────┬──────┘  └─────────┬──────┘  │  │ NLP Engine       │   │
      │                   │          │  │ Knowledge Tracer │   │
┌─────▼───────────────────▼──────┐  │  │ Pathway Gen.     │   │
│          DATABASE LAYER        │  │  │ Badge Calibrator │   │
│   PostgreSQL + Redis (cache)   │  │  └──────────────────┘   │
└────────────────────────────────┘  └────────────────────────┘
```

### Stack Teknologi

| Layer | Teknologi |
|-------|-----------|
| **Frontend** | React.js / Next.js, Tailwind CSS, PixiJS (karakter 2D), D3.js |
| **PWA** | Service Worker, IndexedDB, Web Push API |
| **Backend** | Node.js / FastAPI (Python) |
| **Database** | PostgreSQL, Redis |
| **AI/ML** | OpenAI API / Llama 3, BKT (Bayesian Knowledge Tracing), AST Parser |
| **Infrastructure** | Docker, Kubernetes, GitHub Actions, AWS/GCP |
| **Monitoring** | Prometheus + Grafana |

---

## Struktur Database

```sql
-- Manajemen Pengguna
users (id, name, email, password_hash, role_id, learning_style_id, created_at, is_active)
roles (id, name, description)
learning_styles (id, code, name, description)
interests (id, name, icon, color)
user_interests (user_id, interest_id)  -- pivot

-- Konten Pembelajaran
topics (id, name, description, icon, color_hex, category)
learning_paths (id, topic_id, name, difficulty_level, description, sequence_order, is_active)
missions (id, learning_path_id, title, type, difficulty, xp_reward, estimated_minutes, sequence_order)

-- Assessment
question_bank (id, mission_id, type, question_text, correct_answer, explanation, xp_value)
answer_options (id, question_id, option_text, is_correct)

-- Gamifikasi
badges (id, name, description, icon, criteria_type, criteria_value)
levels (id, level_number, title, min_xp, max_xp, description)
user_badges (user_id, badge_id, earned_at)  -- pivot
user_level (user_id, current_xp, level_id, updated_at)

-- Tracking & AI
user_progress (id, user_id, mission_id, status, score, xp_earned, attempts, completed_at)
cognitive_traces (id, user_id, question_id, action_type, duration_ms, payload JSON, recorded_at)
```

ERD lengkap tersedia di direktori `/docs/erd/`.

---

## Instalasi & Setup

### Prasyarat

```
Node.js >= 18.x
Python >= 3.11
PostgreSQL >= 15
Redis >= 7
Docker & Docker Compose (opsional, direkomendasikan)
```

### Clone Repository

```bash
git clone https://github.com/nexanode-umk/metalearn.git
cd metalearn
```

### Setup dengan Docker (Direkomendasikan)

```bash
# Salin environment variables
cp .env.example .env

# Edit konfigurasi
nano .env

# Jalankan semua layanan
docker-compose up -d

# Jalankan migrasi database
docker-compose exec backend npm run migrate

# Seed data awal (topics, questions, badges)
docker-compose exec backend npm run seed
```

Akses aplikasi di `http://localhost:3000`

### Setup Manual

#### Frontend

```bash
cd frontend
npm install
cp .env.local.example .env.local
npm run dev
```

#### Backend (Node.js)

```bash
cd backend
npm install
cp .env.example .env
npm run migrate
npm run seed
npm run dev
```

#### AI Service (Python)

```bash
cd ai-service
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload --port 8001
```

### Environment Variables

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/metalearn
REDIS_URL=redis://localhost:6379

# JWT
JWT_SECRET=your_super_secret_key_here
JWT_EXPIRES_IN=7d

# AI Service
OPENAI_API_KEY=sk-...
AI_SERVICE_URL=http://localhost:8001

# PWA
VAPID_PUBLIC_KEY=...
VAPID_PRIVATE_KEY=...

# Storage
AWS_S3_BUCKET=metalearn-assets
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
```

---

## Penggunaan

### Akun Default (Development)

| Role | Email | Password |
|------|-------|----------|
| Siswa | student@metalearn.dev | password123 |
| Guru | teacher@metalearn.dev | password123 |
| Admin | admin@metalearn.dev | password123 |

### API Endpoints Utama

```
# Autentikasi
POST   /api/auth/register
POST   /api/auth/login
POST   /api/auth/refresh

# Pengguna
GET    /api/users/profile
PUT    /api/users/profile
GET    /api/users/:id/progress

# Pembelajaran
GET    /api/topics
GET    /api/learning-paths?topic_id=:id
GET    /api/missions/:id
POST   /api/missions/:id/start
POST   /api/missions/:id/submit

# AI
POST   /api/ai/pause-ask          # Pause & Ask AI
POST   /api/ai/generate-pathway   # Generate adaptive pathway
GET    /api/ai/report/:user_id    # Generate narrative report

# Gamifikasi
GET    /api/users/:id/badges
GET    /api/users/:id/level
GET    /api/leaderboard?topic_id=:id

# Guru
GET    /api/teacher/class-progress
GET    /api/teacher/student/:id/traces
```

---

## Alur Pengguna

### Siswa Baru

```
1. Daftar → Verifikasi email
2. Onboarding: Adaptive Interest Scanner (kuis 10 pertanyaan)
3. Lihat Knowledge Map (konstelasi topik)
4. Pilih topik → AI generate learning path personal
5. Mulai misi pertama → Belajar adaptif
6. Gunakan Pause & Ask AI jika bingung
7. Selesaikan misi → Terima XP + lencana
8. Refleksi di Metacognitive Dashboard
9. AI jadwalkan sesi berikutnya
```

### Guru

```
1. Login → Dashboard kelas
2. Pantau progres seluruh siswa real-time
3. Filter per topik / per siswa / per waktu
4. Terima notifikasi siswa yang mengalami stagnasi
5. Unduh AI-Generated Narrative Report per siswa
6. Ekspor data batch untuk pelaporan sekolah
```

---

## Kontribusi AI

### Komponen AI dalam MetaLearn

```python
# 1. NLP untuk Pause & Ask AI
class ContextualQAEngine:
    """
    Memproses pertanyaan pengguna dalam konteks materi aktif.
    Menggunakan RAG (Retrieval-Augmented Generation) dari question_bank.
    """

# 2. Knowledge Tree Assessor
class AbstractSyntaxTreeEvaluator:
    """
    Mengevaluasi struktur logika jawaban (bukan sekadar teks).
    Mendukung variasi jawaban dengan anatomi logika setara.
    """

# 3. Adaptive Pathway Generator
class DynamicPathwayEngine:
    """
    Menghasilkan learning_paths personal berdasarkan:
    - interests & learning_style pengguna
    - Riwayat cognitive_traces
    - Skor user_progress terkini
    """

# 4. Bayesian Knowledge Tracer
class BKTKnowledgeTracer:
    """
    Memperkirakan probabilitas penguasaan konsep.
    P(mastery) dihitung dari riwayat jawaban dan cognitive_traces.
    Threshold mastery: P >= 0.80
    """

# 5. Adaptive Badge Calibrator
class DynamicBadgeEngine:
    """
    Memberikan lencana berdasarkan perilaku spesifik (bukan threshold statis).
    Menganalisis pola fokus, konsistensi, dan gaya belajar.
    """

# 6. Narrative Report Generator
class AIReportGenerator:
    """
    Kompilasi laporan naratif personal dari:
    users, missions, badges, levels, cognitive_traces
    """
```

---

## Struktur Direktori

```
metalearn/
├── frontend/                 # Next.js PWA
│   ├── app/                  # App Router
│   ├── components/           # Komponen UI
│   │   ├── quiz/             # Komponen quiz & assessment
│   │   ├── character/        # Karakter 2D (PixiJS)
│   │   ├── map/              # Knowledge Map (D3.js)
│   │   └── dashboard/        # Dashboard siswa & guru
│   ├── lib/                  # Utilities & hooks
│   ├── public/               # Aset statis
│   └── service-worker.js     # PWA offline support
│
├── backend/                  # Node.js API
│   ├── src/
│   │   ├── controllers/      # Request handlers
│   │   ├── services/         # Business logic
│   │   ├── models/           # Database models
│   │   ├── middleware/       # Auth, validation
│   │   └── routes/           # API routes
│   ├── migrations/           # Database migrations
│   └── seeds/                # Seed data
│
├── ai-service/               # Python FastAPI
│   ├── engines/              # AI engine modules
│   │   ├── nlp/              # Pause & Ask AI
│   │   ├── ast_evaluator/    # Knowledge Tree Assessment
│   │   ├── bkt/              # Bayesian Knowledge Tracing
│   │   ├── pathway/          # Adaptive Pathway Generator
│   │   └── report/           # Narrative Report Generator
│   ├── models/               # ML models
│   └── main.py               # FastAPI entrypoint
│
├── docs/                     # Dokumentasi
│   ├── erd/                  # Entity Relationship Diagram
│   ├── wireframes/           # Wireframe screenshots
│   └── api/                  # API documentation
│
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## Testing

```bash
# Unit tests frontend
cd frontend && npm run test

# Unit tests backend
cd backend && npm run test

# Integration tests
cd backend && npm run test:integration

# AI service tests
cd ai-service && pytest tests/

# E2E tests
npm run test:e2e
```

---

## Roadmap

### v1.0 (MVP — Target: Q4 2026)
- [x] Desain arsitektur & ERD
- [x] Wireframe semua layar
- [ ] Onboarding & Adaptive Interest Scanner
- [ ] Knowledge Map (konstelasi visual)
- [ ] Adaptive Learning Path (basic)
- [ ] Quiz engine dengan Knowledge Tracing
- [ ] Sistem XP & Level dasar
- [ ] PWA (offline support)

### v1.5 (Target: Q1 2027)
- [ ] Pause & Ask AI (NLP engine penuh)
- [ ] Knowledge Tree Assessment (AST evaluator)
- [ ] Cognitive Trace Recorder
- [ ] Lencana adaptif AI
- [ ] Dashboard guru

### v2.0 (Target: Q2 2027)
- [ ] Karakter 2D kustomisasi penuh
- [ ] AI-Generated Narrative Report
- [ ] Metacognitive Dashboard lengkap
- [ ] Continuous Learning Scheduler
- [ ] Integrasi alumni & rekomendasi karir

---

## Kontribusi

Kami menyambut kontribusi! Baca panduan kontribusi kami sebelum membuat pull request:

1. Fork repository ini
2. Buat branch fitur (`git checkout -b feature/nama-fitur`)
3. Commit perubahan (`git commit -m 'feat: tambahkan fitur X'`)
4. Push ke branch (`git push origin feature/nama-fitur`)
5. Buat Pull Request dengan deskripsi yang jelas

### Konvensi Commit

```
feat:     Fitur baru
fix:      Perbaikan bug
docs:     Perubahan dokumentasi
style:    Formatting (tanpa perubahan logika)
refactor: Refactoring kode
test:     Menambah atau memperbaiki tests
chore:    Update dependencies, konfigurasi
```

---

## Tim Pengembang

**Tim NexaNode — Universitas Muria Kudus**

| Nama | Peran |
|------|-------|
| Satrio Putra Agustin | Ketua Tim / Lead Developer |
| Angga Dwi Fernando | Backend Developer |
| Ismail | AI/ML Engineer |

Kompetisi: **Samsung Solve for Tomorrow 2026**
Bidang: **Education**
Institusi: **Universitas Muria Kudus (UMK), Kudus, Jawa Tengah**

---

## Referensi & Landasan Akademik

| Sumber | Relevansi |
|--------|-----------|
| Putri et al. (2026). Gamifikasi AST pada Pembelajaran Python. *Jutisi* | Dasar Knowledge Tree Assessment |
| Qianyu Sun et al. (2026). Adaptive Knowledge Tracing Multi-Agent RL. *FAPM* | Fondasi Bayesian Knowledge Tracing |
| Vadakattu et al. (2026). PWA with Pause-and-Ask AI. *IJPREMS* | Fondasi fitur Pause & Ask AI |
| Niyazova et al. (2026). Gamified AI-supported learning environments. *Frontiers in Education* | Validasi efektivitas gamifikasi AI |
| Ditha et al. (2026). AI-Based Gamification in Learning. *LEARNING* | Bukti empiris 31.3% peningkatan partisipasi |
| Kadam et al. (2025). Personalized Learning Paths with RAG + LLM. *Cureus* | Landasan Adaptive Pathway Generation |

Daftar referensi lengkap tersedia di `docs/references.md`.

---

## Lisensi

```
MIT License

Copyright (c) 2026 Tim NexaNode — Universitas Muria Kudus

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

<div align="center">

**Dibangun dengan 💙 oleh Tim NexaNode**
**Universitas Muria Kudus — Samsung Solve for Tomorrow 2026**

*"Setiap siswa berhak mendapat jalur belajar yang diciptakan untuknya sendiri."*

</div>
