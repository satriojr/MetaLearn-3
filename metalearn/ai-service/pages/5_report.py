import streamlit as st
from engines.report.engine import NarrativeReportEngine

st.set_page_config(page_title="Report Engine", page_icon="📝")
st.title("📝 Report Engine — AI Narrative Report")
st.markdown("Generate personalized narrative reports for students.")

engine = NarrativeReportEngine()
has_api = bool(engine.model)

tab1, tab2 = st.tabs(["Narrative Report", "HTML Report"])

with tab1:
    st.subheader("Student Data")

    col1, col2 = st.columns(2)
    with col1:
        student_name = st.text_input("Student Name", "Budi Santoso")

        mastery_scores = {
            "Algebra": st.slider("Algebra Mastery", 0.0, 1.0, 0.91, 0.01),
            "Geometry": st.slider("Geometry Mastery", 0.0, 1.0, 0.87, 0.01),
            "Trigonometry": st.slider("Trigonometry Mastery", 0.0, 1.0, 0.38, 0.01),
        }

    with col2:
        gamification = {
            "total_xp": st.number_input("Total XP", 0, 10000, 2840),
            "level": st.number_input("Level", 1, 100, 7),
            "badges_earned": st.number_input("Badges", 0, 50, 5),
            "streak_days": st.number_input("Streak Days", 0, 365, 5),
        }

        recent_activity = st.text_area(
            "Recent Activity (JSON list)",
            value='[{"date": "2026-06-20", "activity": "Completed Trigonometry quiz", "score": 65}, {"date": "2026-06-22", "activity": "Practiced Algebra problems", "score": 92}]',
            height=100,
        )

    memory = st.text_area(
        "Learning Memory (optional)",
        value="Budi excels at Algebra but struggles with Trigonometry concepts. He prefers visual learning and works best in the evening.",
        height=80,
    )

    if st.button("Generate Report", type="primary", use_container_width=True):
        if not has_api:
            st.warning("GEMINI_API_KEY not configured.")
        else:
            with st.spinner("Generating narrative report..."):
                try:
                    import json
                    recent = json.loads(recent_activity) if recent_activity.strip() else []
                    report = engine.generate_report(student_name, mastery_scores, gamification, recent, memory)
                    st.success("Report Generated")
                    st.markdown(report)
                except json.JSONDecodeError:
                    st.error("Invalid JSON in Recent Activity.")
                except Exception as e:
                    st.error(f"Error: {e}")

with tab2:
    st.subheader("Generate HTML Report")
    st.markdown("Same data but rendered as HTML.")

    if st.button("Generate HTML Report", type="primary", use_container_width=True):
        if not has_api:
            st.warning("GEMINI_API_KEY not configured.")
        else:
            with st.spinner("Generating HTML report..."):
                try:
                    import json
                    recent = json.loads(recent_activity) if recent_activity.strip() else []
                    report_html = engine.generate_report_html(student_name, mastery_scores, gamification)
                    st.components.v1.html(report_html, scrolling=True, height=600)
                except json.JSONDecodeError:
                    st.error("Invalid JSON in Recent Activity.")
                except Exception as e:
                    st.error(f"Error: {e}")
