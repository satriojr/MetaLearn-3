import streamlit as st
import httpx
import os
from datetime import datetime

API_BASE = os.getenv("API_BASE_URL", "http://backend:8000/api")

st.set_page_config(page_title="Students", page_icon="👥")
st.title("👥 Students")
st.markdown("Browse all students and their progress.")


def api_get(path: str) -> dict | None:
    if not st.session_state.get("token"):
        st.switch_page("admin_app.py")
        return None
    try:
        r = httpx.get(
            f"{API_BASE}{path}",
            headers={"Authorization": f"Bearer {st.session_state.token}"},
            timeout=10,
        )
        return r.json() if r.status_code == 200 else None
    except Exception:
        return None


data = api_get("/dashboard/teacher")

if data and data.get("students") is not None:
    students = data["students"]
    stats = data.get("class_stats", {})

    col1, col2, col3 = st.columns(3)
    search = col1.text_input("🔍 Search by name", placeholder="Type name...")
    min_xp = col2.number_input("Min XP", 0, 10000, 0)
    sort_by = col3.selectbox("Sort by", ["name", "xp", "level", "missions_completed"])

    filtered = [
        s for s in students
        if (not search or search.lower() in s.get("name", "").lower())
        and s.get("xp", 0) >= min_xp
    ]
    filtered.sort(key=lambda s: s.get(sort_by, 0) if sort_by != "name" else s.get("name", ""))

    st.markdown(f"**Showing {len(filtered)} of {len(students)} students**")

    for s in filtered:
        with st.container(border=True):
            col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
            col1.markdown(f"**{s['name']}**  \n*{s.get('email', '')}*")
            col2.metric("Level", s.get("level", 1))
            col3.metric("XP", s.get("xp", 0))
            col4.metric("Missions", s.get("missions_completed", 0))
            if col5.button("View", key=f"view_{s['id']}"):
                st.session_state.selected_student_id = s["id"]
                st.switch_page("pages/2_student_detail.py")
else:
    sample = [
        {"id": 1, "name": "Budi Santoso", "email": "budi@mail.com", "level": 7, "xp": 2840, "missions_completed": 12, "last_active": "2026-06-24"},
        {"id": 2, "name": "Siti Nurhaliza", "email": "siti@mail.com", "level": 9, "xp": 4150, "missions_completed": 18, "last_active": "2026-06-23"},
        {"id": 3, "name": "Ahmad Fauzi", "email": "ahmad@mail.com", "level": 5, "xp": 1890, "missions_completed": 8, "last_active": "2026-06-22"},
        {"id": 4, "name": "Dewi Lestari", "email": "dewi@mail.com", "level": 8, "xp": 3520, "missions_completed": 15, "last_active": "2026-06-24"},
        {"id": 5, "name": "Rudi Hartono", "email": "rudi@mail.com", "level": 4, "xp": 1250, "missions_completed": 6, "last_active": "2026-06-20"},
    ]

    search = st.text_input("🔍 Search by name")
    filtered = [s for s in sample if not search or search.lower() in s["name"].lower()]

    for s in filtered:
        with st.container(border=True):
            col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
            col1.markdown(f"**{s['name']}**  \n*{s.get('email', '')}*")
            col2.metric("Level", s.get("level", 1))
            col3.metric("XP", s.get("xp", 0))
            col4.metric("Missions", s.get("missions_completed", 0))
            if col5.button("View", key=f"view_{s['id']}"):
                st.session_state.selected_student_id = s["id"]
                st.switch_page("pages/2_student_detail.py")
