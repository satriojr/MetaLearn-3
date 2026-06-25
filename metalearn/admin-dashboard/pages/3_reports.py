import streamlit as st
import httpx
import os
import json
from datetime import datetime

API_BASE = os.getenv("API_BASE_URL", "http://backend:8000/api")

st.set_page_config(page_title="Reports", page_icon="📝")
st.title("📝 Generate Reports")
st.markdown("Generate AI-powered narrative reports for students.")

if not st.session_state.get("token"):
    st.switch_page("admin_app.py")
    st.stop()


def api_get(path: str) -> dict | None:
    try:
        r = httpx.get(
            f"{API_BASE}{path}",
            headers={"Authorization": f"Bearer {st.session_state.token}"},
            timeout=15,
        )
        return r.json() if r.status_code == 200 else None
    except Exception:
        return None


sample_students = [
    {"id": 1, "name": "Budi Santoso"},
    {"id": 2, "name": "Siti Nurhaliza"},
    {"id": 3, "name": "Ahmad Fauzi"},
    {"id": 4, "name": "Dewi Lestari"},
    {"id": 5, "name": "Rudi Hartono"},
]

students = sample_students
data = api_get("/dashboard/teacher")
if data and data.get("students"):
    students = data["students"]

student_names = {s["id"]: s["name"] for s in students}

col1, col2 = st.columns([1, 1])

with col1:
    selected_id = st.selectbox(
        "Select Student",
        options=list(student_names.keys()),
        format_func=lambda x: student_names[x],
    )

with col2:
    report_type = st.selectbox(
        "Report Type",
        ["Progress Report", "Weekly Summary", "Full Assessment"],
    )

col1, col2, col3 = st.columns(3)
with col1:
    include_mastery = st.checkbox("Mastery Scores", value=True)
with col2:
    include_gamification = st.checkbox("Gamification", value=True)
with col3:
    include_traces = st.checkbox("Cognitive Traces", value=True)

sample_reports = {
    1: """
### 📋 Progress Report: Budi Santoso

**Ringkasan Progres:**
Budi telah menunjukkan perkembangan yang baik dalam pembelajaran matematika. Dari total 4 misi yang dikerjakan, 3 telah terselesaikan dengan baik. Budi memiliki kekuatan utama di bidang Aljabar dengan skor penguasaan 91%.

**Area Kekuatan:**
- **Algebra (91%)** — Budi sangat unggul dalam konsep aljabar dasar dan persamaan linear
- **Geometry (87%)** — Pemahaman geometri bidang sangat baik

**Area Pengembangan:**
- **Trigonometry (38%)** — Budi masih kesulitan dengan konsep trigonometri dasar, terutama sin/cos/tan
- Disarankan untuk mengulang materi Lingkaran Satuan sebelum melanjutkan

**Aktivitas Terkini:**
- Menyelesaikan misi Trigonometry Intro dengan skor 45%
- Sedang mengerjakan misi Sin/Cos/Tan

**Rekomendasi:**
1. Remedial mission untuk topik Trigonometri — fokus pada Lingkaran Satuan
2. Gunakan Pause & Ask AI saat menemui konsep yang membingungkan
3. Jadwalkan sesi belajar tambahan 2x/minggu untuk topik ini

**Motivasi:**
*"Setiap tantangan adalah kesempatan untuk tumbuh. Kamu sudah hebat di Aljabar, dan kamu pasti bisa menguasai Trigonometri juga!"*
""",
    2: """
### 📋 Progress Report: Siti Nurhaliza

**Ringkasan Progres:**
Siti adalah siswa berprestasi dengan penguasaan materi yang konsisten di atas 80% di semua topik. Dari 3 misi yang dikerjakan, semuanya terselesaikan dengan nilai sangat memuaskan.

**Area Kekuatan:**
- **Algebra (95%)** — Penguasaan aljabar hampir sempurna
- **Geometry (90%)** — Pemahaman geometri sangat baik
- **Physics (88%)** — Konsep fisika dasar dikuasai dengan baik

**Aktivitas Terkini:**
- Menyelesaikan Trigonometry Intro dengan skor 85%

**Rekomendasi:**
1. Lanjutkan ke topik advanced berikutnya
2. Tantang diri dengan soal-soal higher-order thinking
3. Bantu teman sekelas yang kesulitan (peer teaching)

**Motivasi:**
*"Keunggulanmu adalah inspirasi bagi yang lain. Teruslah bersinar!"*
""",
}

st.markdown("---")

if "generated_report" not in st.session_state:
    st.session_state.generated_report = None

if st.button("Generate Report", type="primary", use_container_width=True):
    with st.spinner("Generating report..."):
        try:
            report_data = api_get("/dashboard/report")
            if report_data and report_data.get("report"):
                st.session_state.generated_report = report_data["report"]
                st.success("Report generated successfully!")
                st.markdown(report_data["report"])
                st.caption(f"Generated at: {report_data.get('generated_at', datetime.now().isoformat())}")
            else:
                st.session_state.generated_report = sample_reports.get(selected_id, sample_reports[1])
                st.success("Report generated (offline demo)!")
                st.markdown(st.session_state.generated_report)
                st.caption("⚠️ Backend tidak tersedia — menampilkan sample report.")
        except Exception as e:
            st.session_state.generated_report = sample_reports.get(selected_id, sample_reports[1])
            st.success("Report generated (offline demo)!")
            st.markdown(st.session_state.generated_report)
            st.caption("⚠️ Backend tidak tersedia — menampilkan sample report.")

st.markdown("---")
st.markdown("### Export Options")
col1, col2, col3 = st.columns(3)

with col1:
    st.download_button(
        "📥 Download as Markdown",
        data=st.session_state.generated_report or sample_reports.get(selected_id, sample_reports[1]),
        file_name=f"report_student_{selected_id}.md",
        mime="text/markdown",
        use_container_width=True,
    )
with col2:
    st.button("📄 Download as PDF", disabled=True, use_container_width=True,
              help="PDF export akan tersedia di versi berikutnya")
with col3:
    st.button("📧 Send to Email", disabled=True, use_container_width=True,
              help="Fitur email akan tersedia di versi berikutnya")
