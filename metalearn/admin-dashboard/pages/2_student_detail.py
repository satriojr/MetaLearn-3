import streamlit as st
import httpx
import os
import plotly.graph_objects as go
from datetime import datetime

API_BASE = os.getenv("API_BASE_URL", "http://backend:8000/api")

st.set_page_config(page_title="Student Detail", page_icon="🔍")
st.title("🔍 Student Detail")

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


student_id = st.session_state.get("selected_student_id")

if not student_id:
    st.warning("Pilih student dari halaman Students.")
    if st.button("← Back to Students"):
        st.switch_page("pages/1_students.py")
    st.stop()


sample_students = {
    1: {
        "name": "Budi Santoso",
        "email": "budi@mail.com",
        "role": "siswa",
        "level": 7,
        "xp": 2840,
        "learning_style": "Visual-Kinesthetic",
        "mastery": {"Algebra": 91, "Geometry": 87, "Trigonometry": 38, "Physics": 72},
        "badges": [{"name": "Fast Learner", "icon": "🚀"}, {"name": "Consistent", "icon": "🔥"}],
        "missions": [
            {"title": "Algebra Basics", "score": 92, "status": "completed", "completed_at": "2026-06-20"},
            {"title": "Linear Equations", "score": 88, "status": "completed", "completed_at": "2026-06-21"},
            {"title": "Trigonometry Intro", "score": 45, "status": "completed", "completed_at": "2026-06-22"},
            {"title": "Sin/Cos/Tan", "score": 35, "status": "in_progress", "completed_at": None},
        ],
        "traces": [
            {"action_type": "pause", "recorded_at": "2026-06-22 14:30", "duration_ms": 45000},
            {"action_type": "submit", "recorded_at": "2026-06-22 14:31", "duration_ms": 12000},
            {"action_type": "pause", "recorded_at": "2026-06-22 14:35", "duration_ms": 32000},
            {"action_type": "correct", "recorded_at": "2026-06-22 14:36", "duration_ms": 8000},
        ],
        "confusion_zones": ["Trigonometry", "Sin/Cos/Tan"],
    },
    2: {
        "name": "Siti Nurhaliza",
        "email": "siti@mail.com",
        "role": "siswa",
        "level": 9,
        "xp": 4150,
        "learning_style": "Auditory",
        "mastery": {"Algebra": 95, "Geometry": 90, "Trigonometry": 82, "Physics": 88},
        "badges": [{"name": "Top Performer", "icon": "🏆"}, {"name": "Streak Master", "icon": "🔥"}],
        "missions": [
            {"title": "Algebra Basics", "score": 98, "status": "completed", "completed_at": "2026-06-18"},
            {"title": "Linear Equations", "score": 95, "status": "completed", "completed_at": "2026-06-19"},
            {"title": "Trigonometry Intro", "score": 85, "status": "completed", "completed_at": "2026-06-20"},
        ],
        "traces": [],
        "confusion_zones": [],
    },
}

sid = int(student_id) if str(student_id).isdigit() else 1
student = sample_students.get(sid, sample_students[1])

# Note: API does not support fetching individual student data by ID yet.
# Using sample data as fallback. Student detail endpoint would be added in future.

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(f"## {student['name']}")
    st.markdown(f"*{student.get('email', '')}*")

with col2:
    st.markdown(f"**Learning Style:** {student.get('learning_style', 'N/A')}")
    st.markdown(f"**Confusion Zones:** {', '.join(student.get('confusion_zones', [])) or 'None'}")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Level", student.get("level", 1))
col2.metric("Total XP", student.get("xp", 0))
col3.metric("Badges", len(student.get("badges", [])))
col4.metric("Active Zones", len(student.get("confusion_zones", [])))

tab1, tab2, tab3 = st.tabs(["📊 Mastery", "🎯 Missions", "📈 Cognitive Traces"])

with tab1:
    st.subheader("Mastery Scores by Topic")

    mastery = student.get("mastery", {})
    if mastery:
        fig = go.Figure()
        topics = list(mastery.keys())
        scores = list(mastery.values())
        colors = ["green" if s >= 80 else "orange" if s >= 60 else "red" for s in scores]

        fig.add_trace(go.Bar(
            x=topics, y=scores,
            marker_color=colors,
            text=[f"{s}%" for s in scores],
            textposition="outside",
        ))
        fig.add_hline(y=80, line_dash="dash", line_color="green", annotation_text="Mastery Target (80%)")
        fig.update_layout(
            yaxis_range=[0, 100],
            height=350,
            xaxis_title="Topic",
            yaxis_title="Mastery %",
        )
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Mission Progress")

    missions = student.get("missions", [])
    completed = [m for m in missions if m.get("status") == "completed"]
    in_progress = [m for m in missions if m.get("status") != "completed"]

    col1, col2 = st.columns(2)
    col1.metric("Completed", len(completed))
    col2.metric("In Progress", len(in_progress))

    for m in missions:
        status_icon = "✅" if m.get("status") == "completed" else "⏳"
        score = m.get("score", 0)
        score_color = "green" if score >= 80 else "orange" if score >= 60 else "red"

        with st.container(border=True):
            cols = st.columns([3, 1, 1, 1])
            cols[0].markdown(f"{status_icon} **{m['title']}**")
            cols[1].markdown(f":{score_color}[**{score}%**]")
            cols[2].markdown(f"*{m.get('status', 'unknown').replace('_', ' ').title()}*")
            cols[3].markdown(f"*{m.get('completed_at', '-')}*")

with tab3:
    st.subheader("Cognitive Traces")

    traces = student.get("traces", [])
    if traces:
        action_counts = {}
        for t in traces:
            action = t.get("action_type", "unknown")
            action_counts[action] = action_counts.get(action, 0) + 1

        fig = go.Figure(data=[
            go.Pie(
                labels=list(action_counts.keys()),
                values=list(action_counts.values()),
                hole=0.4,
            )
        ])
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Recent Traces")
        for t in traces[-5:]:
            with st.container(border=True):
                cols = st.columns(4)
                cols[0].markdown(f"**{t.get('action_type', '').replace('_', ' ').title()}**")
                cols[1].markdown(f"⏱ {t.get('duration_ms', 0)}ms")
                cols[2].markdown(f"*{t.get('recorded_at', '')}*")
    else:
        st.info("Belum ada data cognitive traces.")

st.markdown("---")
if st.button("← Back to Students"):
    st.switch_page("pages/1_students.py")
