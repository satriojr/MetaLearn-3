import os
import httpx
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Overview — MetaLearn Demo", page_icon="📊", layout="wide")

API_BASE = os.getenv("API_BASE_URL", "http://backend:8000/api")

if not st.session_state.get("token") and not st.session_state.get("guest"):
    st.switch_page("demo_app.py")

def api_get(path: str) -> dict | None:
    h = {"Authorization": f"Bearer {st.session_state.token}"} if st.session_state.token else {}
    try:
        r = httpx.get(f"{API_BASE}{path}", headers=h, timeout=10)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None

st.title("📊 Platform Overview")
st.caption("High-level metrics and activity snapshot")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Students", "1,247", "+23 this week", help="Registered student accounts")
col2.metric("Active Today", "384", "31% engagement", help="Learners active in last 24h")
col3.metric("Missions Completed", "8,432", "+156 today", help="Total completed missions")
col4.metric("Avg. Mastery", "74%", "+2.1% WoW", help="Average topic mastery score")

st.divider()
tab_overview, tab_activity, tab_students = st.tabs(["📈 Progress Trends", "🕐 Recent Activity", "👥 Top Students"])

with tab_overview:
    weeks = ["Week 1", "Week 2", "Week 3", "Week 4", "Week 5", "Week 6"]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=weeks, y=[45, 52, 58, 65, 71, 78], mode="lines+markers", name="Avg Mastery %", line=dict(width=3, color="#4CAF50")))
    fig.add_trace(go.Scatter(x=weeks, y=[120, 145, 168, 192, 210, 238], mode="lines+markers", name="Active Students", line=dict(width=3, color="#2196F3"), yaxis="y2"))
    fig.update_layout(title="Platform Growth (6 Weeks)", xaxis_title="Week", yaxis_title="Mastery %", yaxis2=dict(overlaying="y", side="right", title="Students"), hovermode="x unified", height=400)
    st.plotly_chart(fig, use_container_width=True)

    topic_scores = {"Algebra": 82, "Geometry": 76, "Calculus": 58, "Statistics": 71, "Physics": 65, "Chemistry": 63, "Biology": 79}
    fig2 = go.Figure(go.Bar(x=list(topic_scores.keys()), y=list(topic_scores.values()), marker_color=["#4CAF50" if v >= 80 else "#FF9800" if v >= 65 else "#f44336" for v in topic_scores.values()]))
    fig2.add_hline(y=80, line_dash="dash", line_color="#4CAF50", annotation_text="Target 80%")
    fig2.update_layout(title="Average Mastery by Topic", xaxis_title="Topic", yaxis_title="Mastery %", height=350)
    st.plotly_chart(fig2, use_container_width=True)

with tab_activity:
    activities = [
        ("🟢", "Alex Rivera", "completed", "Linear Equations", "2 min ago"),
        ("🟡", "Sarah Chen", "started", "Geometry Proofs", "5 min ago"),
        ("🔵", "Marcus J.", "levelled up", "Level 20 🎉", "12 min ago"),
        ("🟢", "Emily Davis", "earned badge", "Streak Master 🔥", "18 min ago"),
        ("🟡", "James Wilson", "submitted", "Calculus Quiz", "25 min ago"),
        ("🔵", "Lisa Park", "joined", "MetaLearn", "1 hour ago"),
        ("🟢", "David Kim", "completed", "Statistics Module", "2 hours ago"),
        ("🟡", "Anna Schmidt", "scored 92%", "Physics Assessment", "3 hours ago"),
    ]
    for icon, name, action, detail, time in activities:
        cols = st.columns([0.5, 2, 2, 3, 1.5])
        cols[0].markdown(icon)
        cols[1].markdown(f"**{name}**")
        cols[2].markdown(action)
        cols[3].markdown(f"_{detail}_")
        cols[4].markdown(f"`{time}`")

with tab_students:
    top = [
        ("🥇", "Alex Rivera", 12500, 24, "98%"),
        ("🥈", "Sarah Chen", 11200, 22, "94%"),
        ("🥉", "Marcus Johnson", 9800, 20, "91%"),
    ]
    for rank, name, xp, lvl, mastery in top:
        with st.container(border=True):
            cols = st.columns([0.5, 3, 2, 2, 2])
            cols[0].markdown(f"**{rank}**")
            cols[1].markdown(f"**{name}**")
            cols[2].markdown(f"⭐ Level {lvl}")
            cols[3].markdown(f"📈 {xp:,} XP")
            cols[4].markdown(f"🎯 {mastery} mastery")
