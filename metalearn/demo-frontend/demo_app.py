import os
import httpx
import streamlit as st

st.set_page_config(page_title="MetaLearn Demo", page_icon="🚀", layout="wide", initial_sidebar_state="expanded")

API_BASE = os.getenv("API_BASE_URL", "http://backend:8000/api")

if "token" not in st.session_state:
    st.session_state.token = None
if "user" not in st.session_state:
    st.session_state.user = None
if "guest" not in st.session_state:
    st.session_state.guest = False

def api_get(path: str) -> dict | None:
    h = {"Authorization": f"Bearer {st.session_state.token}"} if st.session_state.token else {}
    try:
        r = httpx.get(f"{API_BASE}{path}", headers=h, timeout=10)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None

def api_post(path: str, data: dict = None) -> dict | None:
    h = {"Authorization": f"Bearer {st.session_state.token}"} if st.session_state.token else {}
    try:
        r = httpx.post(f"{API_BASE}{path}", json=data or {}, headers=h, timeout=10)
        if r.status_code in (200, 201):
            return r.json()
    except Exception:
        pass
    return None

def login(email: str, password: str) -> bool:
    r = httpx.post(f"{API_BASE}/auth/login", json={"email": email, "password": password}, timeout=10)
    if r.status_code == 200:
        data = r.json()
        st.session_state.token = data.get("token")
        st.session_state.user = data.get("user", data)
        st.session_state.guest = False
        return True
    return False

def logout():
    if st.session_state.token:
        api_post("/auth/logout")
    st.session_state.token = None
    st.session_state.user = None
    st.session_state.guest = False
    st.rerun()

SAMPLE_TOPICS = [
    {"id": 1, "name": "Algebra", "description": "Linear equations, functions, and graphs", "icon": "📐"},
    {"id": 2, "name": "Geometry", "description": "Shapes, angles, and spatial reasoning", "icon": "🔷"},
    {"id": 3, "name": "Calculus", "description": "Derivatives, integrals, and limits", "icon": "∫"},
    {"id": 4, "name": "Statistics", "description": "Probability, distributions, and inference", "icon": "📊"},
    {"id": 5, "name": "Physics", "description": "Mechanics, energy, and waves", "icon": "⚛️"},
]

SAMPLE_PATHS = [
    {"id": 1, "title": "Algebra Fundamentals", "description": "Master the building blocks of algebra", "topics": ["Linear Equations", "Functions", "Graphing"], "level": "Beginner", "duration": "4 weeks"},
    {"id": 2, "title": "Geometry & Proofs", "description": "Explore geometric reasoning and formal proofs", "topics": ["Angles", "Triangles", "Circles"], "level": "Intermediate", "duration": "6 weeks"},
    {"id": 3, "title": "Introduction to Calculus", "description": "Dive into limits, derivatives, and integrals", "topics": ["Limits", "Derivatives", "Integrals"], "level": "Advanced", "duration": "8 weeks"},
    {"id": 4, "title": "Data Science Fundamentals", "description": "Statistics, probability, and data analysis", "topics": ["Probability", "Distributions", "Hypothesis Testing"], "level": "Intermediate", "duration": "6 weeks"},
]

SAMPLE_LEADERBOARD = [
    {"rank": 1, "name": "Alex Rivera", "xp": 12500, "level": 24, "avatar": "🏆"},
    {"rank": 2, "name": "Sarah Chen", "xp": 11200, "level": 22, "avatar": "🥇"},
    {"rank": 3, "name": "Marcus Johnson", "xp": 9800, "level": 20, "avatar": "🥈"},
    {"rank": 4, "name": "Emily Davis", "xp": 8700, "level": 18, "avatar": "🥉"},
    {"rank": 5, "name": "James Wilson", "xp": 7200, "level": 16, "avatar": "⭐"},
]

SAMPLE_BADGES = [
    {"name": "Quick Learner", "icon": "⚡", "desc": "Complete 5 missions in a day"},
    {"name": "Math Whiz", "icon": "🧮", "desc": "Perfect score on Algebra assessment"},
    {"name": "Streak Master", "icon": "🔥", "desc": "7-day learning streak"},
    {"name": "Explorer", "icon": "🗺️", "desc": "Try all learning pathways"},
    {"name": "Problem Solver", "icon": "💡", "desc": "Solve 50 challenges"},
]

if not st.session_state.token and not st.session_state.guest:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 style='text-align:center;'>🚀 MetaLearn</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;font-size:1.2rem;'>Adaptive Learning Platform — AI-Driven Personalization</p>", unsafe_allow_html=True)
        st.divider()
        tab1, tab2 = st.tabs(["🔐 Sign In", "👋 Continue as Guest"])
        with tab1:
            with st.form("login_form"):
                email = st.text_input("Email", placeholder="teacher@metalearn.dev")
                password = st.text_input("Password", type="password", placeholder="password123")
                if st.form_submit_button("Sign In", use_container_width=True, type="primary"):
                    if login(email, password):
                        st.success("Welcome back!")
                        st.rerun()
                    else:
                        st.error("Invalid credentials")
        with tab2:
            st.markdown("##### Explore MetaLearn without an account")
            st.markdown("View sample learning paths, topics, gamification features, and more.")
            if st.button("Continue as Guest", use_container_width=True, type="primary"):
                st.session_state.guest = True
                st.rerun()
        st.stop()

with st.sidebar:
    if st.session_state.user:
        st.markdown(f"### 👤 {st.session_state.user.get('name', 'User')}")
        st.caption(st.session_state.user.get("email", ""))
    else:
        st.markdown("### 👋 Guest Mode")
        st.caption("Some features require login")
    st.divider()
    st.page_link("demo_app.py", label="🏠 Home", icon="🏠")
    st.page_link("pages/1_overview.py", label="📊 Overview", icon="📊")
    st.page_link("pages/2_learning_paths.py", label="🛤️ Learning Paths", icon="🛤️")
    st.page_link("pages/3_knowledge_map.py", label="🧠 Knowledge Map", icon="🧠")
    st.page_link("pages/4_gamification.py", label="🏆 Gamification", icon="🏆")
    st.page_link("pages/5_quiz_game.py", label="🎮 Quiz Game", icon="🎮")
    st.divider()
    if st.session_state.token:
        if st.sidebar.button("🚪 Sign Out", use_container_width=True):
            logout()
    else:
        if st.sidebar.button("🔐 Sign In", use_container_width=True):
            st.session_state.guest = False
            st.rerun()

st.markdown("""<style>.stApp h1, .stApp h2 {font-weight:600;}.feature-card {padding:1.5rem;border-radius:12px;border:1px solid #e0e0e0;background:var(--background-color);}.hero-text {font-size:3rem;font-weight:700;line-height:1.2;}</style>""", unsafe_allow_html=True)

col_left, col_right = st.columns([3, 2])
with col_left:
    st.markdown("<div class='hero-text'>Adaptive Learning<br>Powered by AI</div>", unsafe_allow_html=True)
    st.markdown("MetaLearn personalizes every student's journey with real-time adaptation, gamification, and AI-driven insights.")
    cols = st.columns(3)
    with cols[0]:
        st.metric("Learning Paths", "12+", "adaptive")
    with cols[1]:
        st.metric("Topics", "50+", "K-12 to College")
    with cols[2]:
        st.metric("Active Learners", "1.2K", "+18% MoM")
    if st.button("Explore Learning Paths →", type="primary"):
        st.switch_page("pages/2_learning_paths.py")
with col_right:
    st.image("https://img.icons8.com/fluency/480/idea-sharing.png", width=400)

st.divider()
st.subheader("✨ Key Features")
fcols = st.columns(4)
with fcols[0]:
    st.markdown("<div class='feature-card'><h3>🧠 Adaptive Learning</h3><p>Real-time difficulty adjustment based on performance and confidence.</p></div>", unsafe_allow_html=True)
with fcols[1]:
    st.markdown("<div class='feature-card'><h3>🎮 Gamification</h3><p>XP, levels, badges, leaderboards — keep learners motivated.</p></div>", unsafe_allow_html=True)
with fcols[2]:
    st.markdown("<div class='feature-card'><h3>📊 AI Analytics</h3><p>Detailed reports on mastery, progress, and cognitive traces.</p></div>", unsafe_allow_html=True)
with fcols[3]:
    st.markdown("<div class='feature-card'><h3>🛤️ Smart Pathways</h3><p>Personalized learning paths generated by AI interest scanning.</p></div>", unsafe_allow_html=True)
