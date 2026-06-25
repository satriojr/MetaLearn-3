import streamlit as st
import httpx
import os

API_BASE = os.getenv("API_BASE_URL", "http://backend:8000/api")

st.set_page_config(
    page_title="MetaLearn Admin Dashboard",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "token" not in st.session_state:
    st.session_state.token = None
if "user" not in st.session_state:
    st.session_state.user = None


def api_get(path: str) -> dict | None:
    if not st.session_state.token:
        return None
    try:
        r = httpx.get(
            f"{API_BASE}{path}",
            headers={"Authorization": f"Bearer {st.session_state.token}"},
            timeout=10,
        )
        if r.status_code == 401:
            st.session_state.token = None
            st.session_state.user = None
            st.rerun()
        return r.json() if r.status_code == 200 else None
    except Exception:
        return None


def login(email: str, password: str) -> bool:
    try:
        r = httpx.post(
            f"{API_BASE}/auth/login",
            json={"email": email, "password": password},
            timeout=10,
        )
        if r.status_code == 200:
            data = r.json()
            st.session_state.token = data["token"]
            st.session_state.user = data["user"]
            return True
    except Exception:
        pass
    return False


st.sidebar.image(
    "https://img.shields.io/badge/MetaLearn-Admin_Dashboard-blue?style=for-the-badge",
    use_container_width=False,
)

if not st.session_state.token:
    st.title("📚 MetaLearn Admin Dashboard")
    st.markdown("Masuk menggunakan akun guru/admin untuk mengakses dashboard.")

    with st.form("login_form"):
        email = st.text_input("Email", placeholder="teacher@metalearn.dev")
        password = st.text_input("Password", type="password", placeholder="password123")
        submitted = st.form_submit_button("Login", type="primary", use_container_width=True)

    if submitted:
        if login(email, password):
            st.success("Login berhasil!")
            st.rerun()
        else:
            st.error("Email atau password salah. Coba akun demo: teacher@metalearn.dev / password123")

    st.info("Pastikan backend Laravel berjalan di **localhost:8000**.")
    st.stop()

st.sidebar.markdown(f"**👤 {st.session_state.user.get('name', 'User')}**")
st.sidebar.markdown(f"*{st.session_state.user.get('role', '')}*")
st.sidebar.markdown("---")
st.sidebar.markdown("## Navigation")
st.sidebar.page_link("admin_app.py", label="Overview", icon="📊")
st.sidebar.page_link("pages/1_students.py", label="Students", icon="👥")
st.sidebar.page_link("pages/2_student_detail.py", label="Student Detail", icon="🔍")
st.sidebar.page_link("pages/3_reports.py", label="Reports", icon="📝")
st.sidebar.page_link("pages/4_quiz_game.py", label="Quiz Game", icon="🎮")
st.sidebar.markdown("---")
if st.sidebar.button("Logout", type="secondary", use_container_width=True):
    st.session_state.token = None
    st.session_state.user = None
    st.rerun()

data = api_get("/dashboard/teacher")

st.title("📊 Class Overview")

if data:
    stats = data.get("class_stats", {})
    students = data.get("students", [])

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Students", stats.get("total_students", 0))
    col2.metric("Avg XP", stats.get("average_xp", 0))
    col3.metric("Avg Missions Completed", stats.get("average_missions", 0))
    col4.metric("Top Student", stats.get("top_student", {}).get("name", "-")[:15] if stats.get("top_student") else "-")

    st.subheader("Student Performance Overview")
    if students:
        chart_data = [
            {"name": s["name"], "XP": s["xp"], "Missions": s["missions_completed"], "Level": s["level"]}
            for s in students
        ]
        st.bar_chart(chart_data, x="name", y=["XP", "Missions"])
    else:
        st.info("Belum ada data siswa.")
else:
    st.warning("Tidak dapat terhubung ke backend API. Pastikan backend Laravel berjalan.")

    st.subheader("Sample Data (Offline Mode)")
    sample = [
        {"name": "Budi Santoso", "level": 7, "xp": 2840, "missions_completed": 12, "last_active": "2026-06-24"},
        {"name": "Siti Nurhaliza", "level": 9, "xp": 4150, "missions_completed": 18, "last_active": "2026-06-23"},
        {"name": "Ahmad Fauzi", "level": 5, "xp": 1890, "missions_completed": 8, "last_active": "2026-06-22"},
        {"name": "Dewi Lestari", "level": 8, "xp": 3520, "missions_completed": 15, "last_active": "2026-06-24"},
        {"name": "Rudi Hartono", "level": 4, "xp": 1250, "missions_completed": 6, "last_active": "2026-06-20"},
    ]
    st.bar_chart(sample, x="name", y=["xp", "missions_completed"])
