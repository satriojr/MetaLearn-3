import streamlit as st
import httpx
import os
import random
import time
import plotly.graph_objects as go
from datetime import datetime

API_BASE = os.getenv("API_BASE_URL", "http://backend:8000/api")

st.set_page_config(page_title="Quiz Game — Guru", page_icon="🎮", layout="wide")

if not st.session_state.get("token"):
    st.switch_page("admin_app.py")
    st.stop()

def api_get(path: str) -> dict | None:
    try:
        r = httpx.get(
            f"{API_BASE}{path}",
            headers={"Authorization": f"Bearer {st.session_state.token}"},
            timeout=10,
        )
        return r.json() if r.status_code == 200 else None
    except Exception:
        return None

if "guru_quiz" not in st.session_state:
    st.session_state.guru_quiz = {
        "mode": None,
        "questions": [],
        "index": 0,
        "score": 0,
        "combo": 0,
        "max_combo": 0,
        "answers": [],
        "start_time": None,
        "finished": False,
        "total_time": 0,
    }
if "guru_quiz_history" not in st.session_state:
    st.session_state.guru_quiz_history = []

MATA_PELAJARAN = {
    "Matematika": {"icon": "📐", "color": "#6366f1"},
    "Fisika": {"icon": "⚛️", "color": "#ef4444"},
    "Kimia": {"icon": "🧪", "color": "#8b5cf6"},
    "Biologi": {"icon": "🧬", "color": "#22c55e"},
    "Bahasa Indonesia": {"icon": "📖", "color": "#f59e0b"},
}

BANK_SOAL = {
    "Matematika": [
        {"q": "Nilai dari 2x + 5 = 15, maka x = ...", "opts": ["3", "5", "7", "10"], "ans": 1},
        {"q": "Luas lingkaran dengan jari-jari 7 cm adalah ...", "opts": ["49π cm²", "14π cm²", "7π cm²", "21π cm²"], "ans": 0},
        {"q": "Bentuk sederhana dari 3x + 2y + 5x - y adalah ...", "opts": ["8x + y", "8x + 3y", "8xy", "6x + y"], "ans": 0},
        {"q": "Hasil dari (x + 3)(x + 2) adalah ...", "opts": ["x² + 5x + 6", "x² + 6x + 6", "x² + 5x + 5", "x² + 3x + 2"], "ans": 0},
        {"q": "Nilai sin 30° adalah ...", "opts": ["1/2", "√3/2", "√2/2", "1"], "ans": 0},
        {"q": "Volume kubus dengan sisi 5 cm adalah ...", "opts": ["25 cm³", "125 cm³", "50 cm³", "100 cm³"], "ans": 1},
        {"q": "Keliling persegi panjang dengan p=8, l=6 adalah ...", "opts": ["28", "48", "24", "14"], "ans": 0},
        {"q": "Gradien garis y = 4x - 7 adalah ...", "opts": ["-7", "4", "-4", "7"], "ans": 1},
        {"q": "FPB dari 24 dan 36 adalah ...", "opts": ["6", "8", "12", "18"], "ans": 2},
        {"q": "Jika a=3, b=4, maka a² + b² = ...", "opts": ["7", "12", "25", "9"], "ans": 2},
        {"q": "Bilangan prima antara 10 dan 20 adalah ...", "opts": ["11,13,15,17", "11,13,17,19", "13,15,17,19", "11,15,17,19"], "ans": 1},
        {"q": "Hasil dari 5! adalah ...", "opts": ["60", "100", "120", "24"], "ans": 2},
        {"q": "Mean dari 6, 8, 5, 7, 9 adalah ...", "opts": ["6", "7", "8", "5"], "ans": 1},
        {"q": "25% dari 200 adalah ...", "opts": ["25", "40", "50", "75"], "ans": 2},
        {"q": "Akar dari √144 adalah ...", "opts": ["11", "12", "13", "14"], "ans": 1},
    ],
    "Fisika": [
        {"q": "Rumus Hukum Newton II adalah ...", "opts": ["F = ma", "F = mv", "F = m/a", "F = v/t"], "ans": 0},
        {"q": "Satuan gaya dalam SI adalah ...", "opts": ["Joule", "Newton", "Watt", "Pascal"], "ans": 1},
        {"q": "Energi kinetik dirumuskan sebagai ...", "opts": ["½ mv²", "mgh", "mv", "ma"], "ans": 0},
        {"q": "Cepat rambat bunyi di udara sekitar ...", "opts": ["340 m/s", "3×10⁸ m/s", "1.200 m/s", "100 m/s"], "ans": 0},
        {"q": "Alat untuk mengukur kuat arus listrik disebut ...", "opts": ["Voltmeter", "Amperemeter", "Ohmmeter", "Galvanometer"], "ans": 1},
        {"q": "Hukum Ohm menyatakan V = ...", "opts": ["IR", "I/R", "R/I", "I²R"], "ans": 0},
        {"q": "Gelombang yang memerlukan medium disebut ...", "opts": ["Elektromagnetik", "Mekanik", "Transversal", "Longitudinal"], "ans": 1},
        {"q": "Perubahan wujud padat ke gas disebut ...", "opts": ["Menguap", "Menyublin", "Membeku", "Mengembun"], "ans": 1},
        {"q": "Titik lebur es pada tekanan 1 atm adalah ...", "opts": ["0°C", "100°C", "-4°C", "4°C"], "ans": 0},
        {"q": "Cermin yang selalu menghasilkan bayangan maya adalah ...", "opts": ["Cekung", "Cembung", "Datar", "Gabungan"], "ans": 1},
        {"q": "Frekuensi dengan periode berbanding ...", "opts": ["Lurus", "Terbalik", "Kuadrat", "Setara"], "ans": 1},
        {"q": "Energi potensial gravitasi dirumuskan ...", "opts": ["mgh", "½mv²", "Fd", "ma"], "ans": 0},
        {"q": "Muatan listrik sejenis akan ...", "opts": ["Tarik-menarik", "Tolak-menolak", "Netral", "Berkurang"], "ans": 1},
        {"q": "Transformator step-up menaikkan ...", "opts": ["Frekuensi", "Tegangan", "Arus", "Daya"], "ans": 1},
        {"q": "Warna cahaya dengan frekuensi tertinggi adalah ...", "opts": ["Merah", "Ungu", "Biru", "Hijau"], "ans": 1},
    ],
    "Kimia": [
        {"q": "Lambang unsur emas adalah ...", "opts": ["Em", "Au", "Ag", "E"], "ans": 1},
        {"q": "pH larutan netral adalah ...", "opts": ["5", "6", "7", "8"], "ans": 2},
        {"q": "Rumus kimia air adalah ...", "opts": ["H₂O", "CO₂", "NaCl", "O₂"], "ans": 0},
        {"q": "Partikel terkecil dari suatu unsur adalah ...", "opts": ["Molekul", "Atom", "Elektron", "Proton"], "ans": 1},
        {"q": "Logam yang bersifat konduktor listrik terbaik adalah ...", "opts": ["Besi", "Tembaga", "Perak", "Aluminium"], "ans": 2},
        {"q": "Unsur dengan nomor atom 6 adalah ...", "opts": ["Oksigen", "Karbon", "Nitrogen", "Neon"], "ans": 1},
        {"q": "Ikatan antara logam dan non-logam umumnya adalah ...", "opts": ["Ionik", "Kovalen", "Logam", "Hidrogen"], "ans": 0},
        {"q": "Gas yang paling melimpah di atmosfer adalah ...", "opts": ["Oksigen", "Karbon dioksida", "Nitrogen", "Argon"], "ans": 2},
        {"q": "Reaksi netralisasi antara asam dan basa menghasilkan ...", "opts": ["Garam dan air", "CO₂ dan air", "Oksigen", "Hidrogen"], "ans": 0},
        {"q": "Larutan dengan pH < 7 bersifat ...", "opts": ["Basa", "Asam", "Netral", "Garam"], "ans": 1},
        {"q": "Unsur golongan gas mulia memiliki elektron valensi ...", "opts": ["1", "2", "6", "8"], "ans": 3},
        {"q": "Rumus kimia garam dapur adalah ...", "opts": ["KCl", "NaCl", "CaCl₂", "MgCl₂"], "ans": 1},
        {"q": "Proses perkaratan besi memerlukan ...", "opts": ["Air saja", "Oksigen saja", "Air dan oksigen", "Karbon dioksida"], "ans": 2},
        {"q": "Bilangan oksidasi oksigen dalam H₂O adalah ...", "opts": ["0", "-1", "-2", "+2"], "ans": 2},
        {"q": "Senyawa organik utama penyusun kayu adalah ...", "opts": ["Protein", "Selulosa", "Lemak", "Karbohidrat"], "ans": 1},
    ],
    "Biologi": [
        {"q": "Organel tempat fotosintesis adalah ...", "opts": ["Mitokondria", "Kloroplas", "Nukleus", "Ribosom"], "ans": 1},
        {"q": "Jumlah kromosom manusia adalah ...", "opts": ["23", "46", "44", "48"], "ans": 1},
        {"q": "Darah termasuk jaringan ...", "opts": ["Epitel", "Ikat", "Otot", "Syaraf"], "ans": 1},
        {"q": "Pembuluh yang membawa darah meninggalkan jantung adalah ...", "opts": ["Vena", "Arteri", "Kapiler", "Pembuluh limfa"], "ans": 1},
        {"q": "Enzim berfungsi sebagai ...", "opts": ["Sumber energi", "Katalisator", "Hormon", "Vitamin"], "ans": 1},
        {"q": "Bagian telinga yang berfungsi sebagai alat keseimbangan adalah ...", "opts": ["Rumah siput", "Kanalis semisirkularis", "Gendang telinga", "Daun telinga"], "ans": 1},
        {"q": "Hormon yang mengatur kadar gula darah adalah ...", "opts": ["Adrenalin", "Insulin", "Tiroksin", "Estrogen"], "ans": 1},
        {"q": "Proses pembelahan sel yang menghasilkan 2 sel anak identik disebut ...", "opts": ["Meiosis", "Mitosis", "Amitosis", "Fragmentasi"], "ans": 1},
        {"q": "Organ ekskresi manusia adalah ...", "opts": ["Jantung, paru-paru, ginjal, kulit", "Ginjal, kulit, paru-paru, hati", "Lambung, usus, hati, ginjal", "Paru-paru, jantung, ginjal, kulit"], "ans": 1},
        {"q": "Cacing tanah termasuk filum ...", "opts": ["Platyhelminthes", "Annelida", "Nematoda", "Mollusca"], "ans": 1},
        {"q": "Tumbuhan dikotil memiliki akar ...", "opts": ["Serabut", "Tunggang", "Napas", "Tunjang"], "ans": 1},
        {"q": "Vitamin yang larut dalam lemak adalah ...", "opts": ["Vitamin C", "Vitamin B kompleks", "Vitamin A, D, E, K", "Semua vitamin"], "ans": 2},
        {"q": "Ekosistem air tawar contohnya ...", "opts": ["Terumbu karang", "Sungai", "Laut", "Mangrove"], "ans": 1},
        {"q": "DNA berbentuk heliks ganda ditemukan oleh ...", "opts": ["Darwin", "Mendel", "Watson & Crick", "Einstein"], "ans": 2},
        {"q": "Jaringan yang mengangkut air pada tumbuhan adalah ...", "opts": ["Floem", "Xilem", "Kambium", "Epidermis"], "ans": 1},
    ],
    "Bahasa Indonesia": [
        {"q": "Kalimat yang mengandung kata kerja aktif transitif adalah ...", "opts": ["Adik tidur", "Ibu memasak nasi", "Ayah sedang membaca", "Mereka bermain"], "ans": 1},
        {"q": "Sinonim dari kata 'kompleks' adalah ...", "opts": ["Sederhana", "Rumit", "Mudah", "Ringan"], "ans": 1},
        {"q": "Teks yang berisi petunjuk melakukan sesuatu disebut ...", "opts": ["Eksposisi", "Prosedur", "Narasi", "Deskripsi"], "ans": 1},
        {"q": "Awalan 'me-' pada kata 'menulis' berfungsi sebagai ...", "opts": ["Prefiks pembentuk nomina", "Prefiks pembentuk verba", "Sufiks", "Infiks"], "ans": 1},
        {"q": "Kata baku yang tepat untuk 'ijasah' adalah ...", "opts": ["Ijzah", "Ijazah", "Ijasah", "Jiazah"], "ans": 1},
        {"q": "Anak kalimat dalam kalimat majemuk bertingkat disebut ...", "opts": ["Klausa utama", "Klausa subordinatif", "Frasa", "Kata"], "ans": 1},
        {"q": "Makna kata 'bermigrasi' adalah ...", "opts": ["Menetap", "Berpindah tempat", "Berkembang biak", "Beradaptasi"], "ans": 1},
        {"q": "Tanda baca yang digunakan setelah kata seru adalah ...", "opts": ["Titik", "Koma", "Tanda seru", "Tanda tanya"], "ans": 2},
        {"q": "Paragraf yang kalimat utamanya di awal disebut ...", "opts": ["Deduktif", "Induktif", "Campuran", "Naratif"], "ans": 0},
        {"q": "Kata tidak baku dari 'aktivitas' adalah ...", "opts": ["Aktifitas", "Aktifvitas", "Aktipitas", "Activity"], "ans": 0},
        {"q": "Cerita rakyat termasuk jenis ...", "opts": ["Dongeng", "Sejarah", "Biografi", "Legenda"], "ans": 3},
        {"q": "Ciri-ciri pantun adalah ...", "opts": ["4 baris, a-a-a-a", "4 baris, a-b-a-b", "2 baris, a-b", "8 baris, a-b-a-b"], "ans": 1},
        {"q": "Konjungsi temporal contohnya ...", "opts": ["Dan, atau, tetapi", "Kemudian, lalu, setelah", "Karena, sehingga", "Yang, di, ke"], "ans": 1},
        {"q": "Kalimat efektif adalah kalimat yang ...", "opts": ["Panjang dan rumit", "Singkat, padat, jelas", "Banyak kosa kata", "Mengandung majas"], "ans": 1},
        {"q": "Gagasan utama dalam paragraf disebut ...", "opts": ["Kalimat penjelas", "Ide pokok", "Kata kunci", "Simpulan"], "ans": 1},
    ],
}

WAKTU_PER_SOAL = 15

gq = st.session_state.guru_quiz

siswa_data = api_get("/dashboard/teacher")
if siswa_data and siswa_data.get("students"):
    daftar_siswa = [s["name"] for s in siswa_data["students"]]
else:
    daftar_siswa = ["Budi Santoso", "Siti Nurhaliza", "Ahmad Fauzi", "Dewi Lestari", "Rudi Hartono"]

st.markdown("""
<style>
    .timer-big {font-size:3rem;font-weight:700;text-align:center;font-variant-numeric:tabular-nums;}
    .soal-text {font-size:1.3rem;font-weight:500;padding:0.75rem 0;}
    .skor-display {font-size:1.5rem;font-weight:600;}
    .combo-display {font-size:1.2rem;}
    .benar {border:3px solid #4CAF50 !important;background:rgba(76,175,80,0.12) !important;border-radius:8px;padding:0.75rem;}
    .salah {border:3px solid #f44336 !important;background:rgba(244,67,54,0.12) !important;border-radius:8px;padding:0.75rem;}
    div[data-testid="stHorizontalBlock"] > div > div > button {height:3.5rem !important;font-size:1.05rem !important;}
</style>
""", unsafe_allow_html=True)

def mulai_kuis(mata_pelajaran):
    bank = BANK_SOAL[mata_pelajaran]
    terpilih = random.sample(bank, min(10, len(bank)))
    gq["mode"] = mata_pelajaran
    gq["questions"] = [
        {"q": s["q"], "opts": s["opts"], "ans": s["ans"], "chosen": None, "time_taken": 0}
        for s in terpilih
    ]
    gq["index"] = 0
    gq["score"] = 0
    gq["combo"] = 0
    gq["max_combo"] = 0
    gq["answers"] = []
    gq["start_time"] = time.time()
    gq["finished"] = False
    gq["total_time"] = 0

def jawab(idx):
    chosen = gq["questions"][idx]["chosen"]
    benar = gq["questions"][idx]["ans"]
    if chosen is None:
        return
    is_benar = chosen == benar
    if is_benar:
        gq["combo"] += 1
        gq["max_combo"] = max(gq["max_combo"], gq["combo"])
        bonus_combo = min(gq["combo"] - 1, 5)
        base = 100
        bonus_waktu = max(0, int((WAKTU_PER_SOAL - gq["questions"][idx]["time_taken"]) * 5))
        earned = base + bonus_waktu + bonus_combo * 20
    else:
        gq["combo"] = 0
        earned = 0
    gq["score"] += earned
    gq["answers"].append({"correct": is_benar, "earned": earned, "time": gq["questions"][idx]["time_taken"]})

def soal_berikutnya():
    gq["index"] += 1
    if gq["index"] >= len(gq["questions"]):
        gq["finished"] = True
        gq["total_time"] = time.time() - gq["start_time"]
        entry = {
            "mapel": gq["mode"],
            "skor": gq["score"],
            "combo": gq["max_combo"],
            "benar": sum(1 for a in gq["answers"] if a["correct"]),
            "total": len(gq["answers"]),
            "waktu": round(gq["total_time"], 1),
            "tgl": datetime.now().strftime("%H:%M %d-%m-%Y"),
        }
        st.session_state.guru_quiz_history.append(entry)
        st.session_state.guru_quiz_history.sort(key=lambda x: x["skor"], reverse=True)
        st.session_state.guru_quiz_history = st.session_state.guru_quiz_history[:20]

st.title("🎮 Quiz Interaktif untuk Kelas")
st.markdown("Demo kuis interaktif — guru dapat mendemonstrasikan soal di depan kelas.")

tab_kuis, tab_riwayat, tab_kelas = st.tabs(["🎯 Kuis Langsung", "📊 Riwayat Skor", "👥 Performa Kelas"])

with tab_kuis:
    if gq["mode"] is None or gq["finished"]:
        if gq["finished"]:
            total = len(gq["answers"])
            benar = sum(1 for a in gq["answers"] if a["correct"])
            pct = (benar / total * 100) if total > 0 else 0

            mp = MATA_PELAJARAN[gq["mode"]]
            st.markdown(f"<div style='text-align:center;'>", unsafe_allow_html=True)
            st.markdown(f"<span style='font-size:3rem;'>{mp['icon']}</span>", unsafe_allow_html=True)
            st.markdown(f"<h2>Kuis {gq['mode']} Selesai!</h2>", unsafe_allow_html=True)

            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=pct,
                number={"suffix": "%", "font": {"size": 48}},
                delta={"reference": 80, "increasing": {"color": "#4CAF50"}, "decreasing": {"color": "#f44336"}},
                gauge={
                    "axis": {"range": [0, 100], "tickwidth": 1},
                    "bar": {"color": "#4CAF50" if pct >= 80 else "#FF9800" if pct >= 60 else "#f44336"},
                    "steps": [
                        {"range": [0, 40], "color": "#FFCDD2"},
                        {"range": [40, 70], "color": "#FFE0B2"},
                        {"range": [70, 100], "color": "#C8E6C9"},
                    ],
                    "threshold": {"line": {"color": mp["color"], "width": 4}, "thickness": 0.75, "value": 80},
                }
            ))
            fig.update_layout(height=280, margin=dict(l=20, r=20, t=20, b=0))
            col_r, col_m, col_l = st.columns([1, 2, 1])
            with col_m:
                st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Benar", f"{benar}/{total}", f"{pct:.0f}%")
            c2.metric("Total Skor", f"{gq['score']:,}")
            c3.metric("Kombo Terbaik", f"{gq['max_combo']}x🔥")
            c4.metric("Waktu", f"{gq['total_time']:.1f}s")

            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(
                x=list(range(1, len(gq["answers"]) + 1)),
                y=[a["earned"] for a in gq["answers"]],
                mode="lines+markers",
                marker=dict(
                    size=12,
                    color=["#4CAF50" if a["correct"] else "#f44336" for a in gq["answers"]],
                    line=dict(width=2, color="white"),
                ),
                line=dict(color=mp["color"], width=2, dash="dot"),
            ))
            fig2.update_layout(title="Skor per Soal", xaxis_title="Soal #", yaxis_title="Poin", height=220, hovermode="x unified")
            st.plotly_chart(fig2, use_container_width=True)

            grade = "⭐⭐⭐" if pct >= 90 else "⭐⭐" if pct >= 75 else "⭐" if pct >= 60 else "💪"
            msg = "Luar biasa! Penguasaan sempurna!" if pct >= 90 else "Bagus sekali! Pertahankan!" if pct >= 75 else "Cukup baik, perlu review lagi." if pct >= 60 else "Jangan menyerah, terus berlatih!"
            st.markdown(f"<div style='text-align:center;font-size:1.4rem;padding:0.5rem;'>{grade} {msg}</div>", unsafe_allow_html=True)

            if gq["max_combo"] >= 5:
                st.balloons()

            st.divider()
            col_a, col_b = st.columns(2)
            if col_a.button("🔄 Kuis Lagi", use_container_width=True, type="primary"):
                gq["mode"] = None
                gq["finished"] = False
                st.rerun()
            if col_b.button("🏠 Ke Beranda", use_container_width=True):
                gq["mode"] = None
                gq["finished"] = False
                st.switch_page("admin_app.py")
        else:
            st.subheader("📚 Pilih Mata Pelajaran")
            st.markdown("Klik salah satu mata pelajaran untuk memulai demo kuis.")
            cols = st.columns(len(MATA_PELAJARAN))
            for i, (mp, info) in enumerate(MATA_PELAJARAN.items()):
                with cols[i]:
                    with st.container(border=True):
                        st.markdown(f"<div style='text-align:center;font-size:3rem;'>{info['icon']}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div style='text-align:center;font-weight:600;font-size:1.1rem;'>{mp}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div style='text-align:center;font-size:0.8rem;color:gray;'>10 soal<br>{WAKTU_PER_SOAL}s per soal</div>", unsafe_allow_html=True)
                        if st.button("Mulai 🎯", key=f"guru_start_{mp}", use_container_width=True):
                            mulai_kuis(mp)
                            st.rerun()
    else:
        total_q = len(gq["questions"])
        idx = gq["index"]
        q = gq["questions"][idx]
        mp_info = MATA_PELAJARAN[gq["mode"]]

        elapsed_total = time.time() - gq["start_time"]
        elapsed_soal = elapsed_total - sum(gq["questions"][i]["time_taken"] for i in range(idx))
        sisa = max(0, WAKTU_PER_SOAL - int(elapsed_soal))

        st.markdown(f"""
        <div style='display:flex;align-items:center;gap:1rem;margin-bottom:0.25rem;'>
            <span style='font-size:1.8rem;'>{mp_info['icon']}</span>
            <span style='font-size:1.3rem;font-weight:600;'>{gq['mode']}</span>
            <span style='margin-left:auto;font-size:0.9rem;color:gray;'>Soal {idx+1} dari {total_q}</span>
        </div>
        """, unsafe_allow_html=True)

        st.progress((idx + 1) / total_q)

        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            warna = "#f44336" if sisa <= 5 else "#FF9800" if sisa <= 10 else "#4CAF50"
            st.markdown(f"<div class='timer-big' style='color:{warna};'>{sisa}s</div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='skor-display'>💰 {gq['score']:,}</div>", unsafe_allow_html=True)
        with c3:
            warna_combo = "#FF9800" if gq["combo"] >= 3 else "#90A4AE"
            st.markdown(f"<div class='combo-display' style='color:{warna_combo};'>🔥 x{gq['combo']}</div>", unsafe_allow_html=True)

        st.markdown(f"<div class='soal-text'>{q['q']}</div>", unsafe_allow_html=True)

        disabled = q["chosen"] is not None
        cols = st.columns(2)
        for i, opt in enumerate(q["opts"]):
            with cols[i % 2]:
                if disabled:
                    if i == q["ans"]:
                        st.markdown(f"<div class='benar'><span style='color:#4CAF50;font-weight:600;'>{opt}</span></div>", unsafe_allow_html=True)
                    elif i == q["chosen"]:
                        st.markdown(f"<div class='salah'><span style='color:#f44336;font-weight:600;'>{opt}</span></div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div style='padding:0.75rem;border-radius:8px;border:2px solid #e0e0e0;color:#9E9E9E;'>{opt}</div>", unsafe_allow_html=True)
                else:
                    if st.button(opt, key=f"g_opt_{idx}_{i}", use_container_width=True, disabled=disabled):
                        q["chosen"] = i
                        q["time_taken"] = elapsed_soal
                        jawab(idx)
                        st.rerun()

        if sisa <= 0 and q["chosen"] is None:
            q["chosen"] = -1
            q["time_taken"] = WAKTU_PER_SOAL
            jawab(idx)
            st.rerun()

        if q["chosen"] is not None:
            st.markdown("---")
            if q["chosen"] == q["ans"]:
                st.success(f"✅ Benar! +{gq['answers'][-1]['earned'] if gq['answers'] else 0} poin")
            else:
                st.error(f"❌ Jawaban benar: {q['opts'][q['ans']]}")

            if idx < total_q - 1:
                if st.button("Selanjutnya →", use_container_width=True, type="primary"):
                    soal_berikutnya()
                    st.rerun()
            else:
                if st.button("🎉 Lihat Hasil", use_container_width=True, type="primary"):
                    soal_berikutnya()
                    st.rerun()

        st.markdown("<div style='display:flex;gap:0.3rem;justify-content:center;margin-top:0.75rem;'>", unsafe_allow_html=True)
        dot = ""
        for i in range(total_q):
            a = gq["questions"][i]
            if a["chosen"] is not None:
                w = "#4CAF50" if a["chosen"] == a["ans"] else "#f44336"
            elif i == idx:
                w = mp_info["color"]
            else:
                w = "#E0E0E0"
            s = "box-shadow:0 0 4px " + w + ";" if i == idx else ""
            dot += f"<span style='width:12px;height:12px;border-radius:50%;background:{w};display:inline-block;{s}'></span>"
        st.markdown(f"<div style='display:flex;gap:0.35rem;justify-content:center;'>{dot}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

with tab_riwayat:
    st.subheader("📊 Riwayat Skor Kuis")
    if gq["finished"] and gq["answers"]:
        st.info("💡 Skor sesi terakhir tersimpan di tabel riwayat di bawah.")

    if st.session_state.guru_quiz_history:
        for i, entry in enumerate(st.session_state.guru_quiz_history[:10]):
            medal = ["🥇", "🥈", "🥉"][i] if i < 3 else f"#{i+1}"
            with st.container(border=True):
                cols = st.columns([0.5, 1.5, 1.5, 1.5, 1, 1, 1])
                cols[0].markdown(f"**{medal}**")
                cols[1].markdown(f"**{entry.get('mapel', '-')}**")
                cols[2].markdown(f"📈 {entry['skor']:,}")
                cols[3].markdown(f"✅ {entry['benar']}/{entry['total']} ({entry['benar']/entry['total']*100:.0f}%)")
                cols[4].markdown(f"🔥 {entry['combo']}x")
                cols[5].markdown(f"⏱ {entry['waktu']}s")
                cols[6].markdown(f"`{entry.get('tgl', '')}`")

        fig_h = go.Figure()
        skor_list = [e["skor"] for e in st.session_state.guru_quiz_history]
        fig_h.add_trace(go.Scatter(
            x=list(range(1, len(skor_list) + 1)),
            y=skor_list,
            mode="lines+markers",
            marker=dict(size=10, color="#6366f1"),
            line=dict(width=2, color="#6366f1"),
        ))
        fig_h.update_layout(title="Tren Skor", xaxis_title="Sesi ke-", yaxis_title="Skor", height=250)
        st.plotly_chart(fig_h, use_container_width=True)
    else:
        st.info("Belum ada riwayat kuis. Mulai kuis di tab **🎯 Kuis Langsung**.")

    if st.button("🗑️ Hapus Riwayat", type="secondary"):
        st.session_state.guru_quiz_history = []
        st.rerun()

with tab_kelas:
    st.subheader("👥 Simulasi Performa Kelas")

    st.markdown("Data simulasi — gambaran jika seluruh siswa mengerjakan kuis yang sama.")

    st.button("🔄 Generate Simulasi Kelas", use_container_width=True, disabled=True, help="Simulasi dihasilkan secara otomatis")

    skor_siswa = {}
    for nama in daftar_siswa:
        if nama not in skor_siswa:
            skor_siswa[nama] = {
                "skor": random.randint(300, 950),
                "benar": random.randint(4, 10),
                "total": 10,
                "waktu": round(random.uniform(40, 140), 1),
                "combo": random.randint(1, 5),
            }

    fig_k = go.Figure()
    fig_k.add_trace(go.Bar(
        x=list(skor_siswa.keys()),
        y=[s["skor"] for s in skor_siswa.values()],
        marker_color=["#4CAF50" if s["skor"] >= 700 else "#FF9800" if s["skor"] >= 500 else "#f44336" for s in skor_siswa.values()],
        text=[f"{s['skor']}" for s in skor_siswa.values()],
        textposition="outside",
    ))
    fig_k.add_hline(y=700, line_dash="dash", line_color="#4CAF50", annotation_text="Target (700)")
    fig_k.update_layout(title="Skor Kuis per Siswa (Simulasi)", xaxis_title="Siswa", yaxis_title="Skor", height=350)
    st.plotly_chart(fig_k, use_container_width=True)

    c1, c2, c3, c4 = st.columns(4)
    semua_skor = [s["skor"] for s in skor_siswa.values()]
    semua_benar = [s["benar"] for s in skor_siswa.values()]
    c1.metric("Rata-rata Skor", f"{sum(semua_skor)//len(semua_skor)}")
    c2.metric("Skor Tertinggi", f"{max(semua_skor)}")
    c3.metric("Rata-rata Benar", f"{sum(semua_benar)/len(semua_benar):.1f}/{skor_siswa[daftar_siswa[0]]['total']}")
    c4.metric("Siswa di Atas Target", f"{sum(1 for s in semua_skor if s >= 700)}/{len(semua_skor)}")

    st.subheader("📋 Detail Skor Siswa")
    for nama in sorted(skor_siswa.keys(), key=lambda n: skor_siswa[n]["skor"], reverse=True):
        s = skor_siswa[nama]
        pct = s["benar"] / s["total"] * 100
        with st.container(border=True):
            cols = st.columns([2, 1.5, 1.5, 1, 1.5])
            cols[0].markdown(f"**{nama}**")
            cols[1].markdown(f"Skor: **{s['skor']}**")
            cols[2].markdown(f"Benar: {s['benar']}/{s['total']} ({pct:.0f}%)")
            cols[3].markdown(f"🔥 {s['combo']}x")
            cols[4].markdown(f"⏱ {s['waktu']}s")
