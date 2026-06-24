import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Learning Paths — MetaLearn Demo", page_icon="🛤️", layout="wide")

if not st.session_state.get("token") and not st.session_state.get("guest"):
    st.switch_page("demo_app.py")

SAMPLE_PATHS = [
    {"id": 1, "title": "Algebra Fundamentals", "description": "Master linear equations, functions, and graphing from the ground up.", "topics": ["Linear Equations", "Functions & Relations", "Graphing & Slope", "Systems of Equations"], "level": "Beginner", "duration": "4 weeks", "enrolled": 342, "color": "#4CAF50"},
    {"id": 2, "title": "Geometry & Proofs", "description": "Explore shapes, angles, and the art of mathematical proofs.", "topics": ["Angles & Lines", "Triangles & Trig", "Circles & Spheres", "Formal Proofs"], "level": "Intermediate", "duration": "6 weeks", "enrolled": 218, "color": "#2196F3"},
    {"id": 3, "title": "Introduction to Calculus", "description": "Dive into limits, derivatives, and the fundamentals of integration.", "topics": ["Limits & Continuity", "Derivatives", "Applications of Derivatives", "Integrals"], "level": "Advanced", "duration": "8 weeks", "enrolled": 156, "color": "#FF9800"},
    {"id": 4, "title": "Data Science Fundamentals", "description": "Build a foundation in statistics, probability, and data-driven reasoning.", "topics": ["Probability Theory", "Statistical Distributions", "Hypothesis Testing", "Data Visualization"], "level": "Intermediate", "duration": "6 weeks", "enrolled": 189, "color": "#9C27B0"},
    {"id": 5, "title": "Physics: Mechanics", "description": "Understand motion, forces, energy, and the laws that govern our world.", "topics": ["Kinematics", "Dynamics & Forces", "Energy & Work", "Waves & Oscillations"], "level": "Advanced", "duration": "8 weeks", "enrolled": 134, "color": "#f44336"},
    {"id": 6, "title": "Biology Essentials", "description": "Explore cells, genetics, evolution, and the diversity of life.", "topics": ["Cell Biology", "Genetics & DNA", "Evolution", "Ecosystems"], "level": "Beginner", "duration": "5 weeks", "enrolled": 275, "color": "#009688"},
]

st.title("🛤️ Learning Paths")
st.caption("AI-generated personalized pathways adapted to each learner's interests and skill level")

levels = ["All", "Beginner", "Intermediate", "Advanced"]
selected_level = st.selectbox("Filter by level", levels, horizontal=True)
filtered = SAMPLE_PATHS if selected_level == "All" else [p for p in SAMPLE_PATHS if p["level"] == selected_level]

for path in filtered:
    with st.container(border=True):
        cols = st.columns([1, 5, 2])
        with cols[0]:
            st.markdown(f"<div style='background:{path['color']};width:60px;height:60px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:24px;color:white;font-weight:bold;'>{path['title'][0]}</div>", unsafe_allow_html=True)
        with cols[1]:
            st.markdown(f"### {path['title']}")
            st.markdown(path["description"])
            stages = ""
            for t in path["topics"]:
                stages += f"<span style='background:#f0f0f0;padding:2px 10px;border-radius:12px;margin-right:6px;font-size:0.85rem;'>{t}</span> "
            st.markdown(f"<div style='margin-top:8px;'>{stages}</div>", unsafe_allow_html=True)
        with cols[2]:
            st.markdown(f"**🎯 {path['level']}**")
            st.markdown(f"**⏱️ {path['duration']}**")
            st.markdown(f"**👥 {path['enrolled']} enrolled**")
            if st.button(f"Preview Path →", key=f"path_{path['id']}", use_container_width=True):
                st.info(f"🔍 Full preview of '{path['title']}' — register to start!")

st.divider()
st.subheader("📈 Path Comparison")
path_names = [p["title"] for p in SAMPLE_PATHS]
enrollments = [p["enrolled"] for p in SAMPLE_PATHS]
fig = go.Figure(go.Bar(x=path_names, y=enrollments, marker_color=[p["color"] for p in SAMPLE_PATHS], text=enrollments))
fig.update_layout(title="Enrollment by Path", xaxis_title="", yaxis_title="Students Enrolled", height=350)
st.plotly_chart(fig, use_container_width=True)

st.subheader("🎯 Interest Scanner Demo")
st.markdown("Tell us what excites you, and MetaLearn's AI will generate a custom learning path.")
interests = st.multiselect("What are you interested in?", ["Math", "Science", "Technology", "Art", "History", "Languages"], default=["Math", "Science"])
if st.button("Generate My Path ✨", type="primary"):
    with st.spinner("AI is analyzing your interests..."):
        import time
        time.sleep(1.5)
    st.success("Your personalized learning path is ready!")
    with st.container(border=True):
        st.markdown("### 🧑‍🎓 Your Custom Path")
        st.markdown("**Recommended Topics:** Algebra → Geometry → Physics → Data Science")
        st.markdown("**Estimated Duration:** 12 weeks")
        st.markdown("**Difficulty Progression:** Beginner → Intermediate → Advanced")
        st.markdown("---")
        st.markdown("⚡ *AI recommendation based on your interests and skill profile*")
