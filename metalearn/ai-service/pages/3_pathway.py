import streamlit as st
from engines.pathway.engine import AdaptivePathwayEngine

st.set_page_config(page_title="Pathway Engine", page_icon="🗺️")
st.title("🗺️ Pathway Engine — Adaptive Learning Pathway")
st.markdown("Generate personalized learning pathways and remedial missions.")

engine = AdaptivePathwayEngine()
has_api = bool(engine.model)

tab1, tab2 = st.tabs(["Generate Pathway", "Remedial Mission"])

with tab1:
    st.subheader("Student Profile")

    col1, col2 = st.columns(2)
    with col1:
        interests = st.multiselect(
            "Interests",
            ["Mathematics", "Science", "Technology", "Language", "Arts", "History", "Sports"],
            ["Mathematics", "Science"],
        )
    with col2:
        learning_style = st.selectbox(
            "Learning Style",
            ["visual", "auditory", "read/write", "kinesthetic", "visual_kinesthetic"],
        )

    with st.expander("Advanced: Mastery Scores & Completed Missions"):
        col1, col2 = st.columns(2)
        with col1:
            mastery_json = st.text_area(
                "Mastery Scores (JSON)", height=100,
                value='{"algebra": 0.9, "geometry": 0.6, "trigonometry": 0.3}',
            )
        with col2:
            missions_json = st.text_area(
                "Completed Missions (JSON)", height=100,
                value='["msn_algebra_intro", "msn_algebra_advanced"]',
            )

    if st.button("Generate Pathway", type="primary", use_container_width=True):
        if not has_api:
            st.warning("GEMINI_API_KEY not configured. Cannot generate pathway.")
        else:
            with st.spinner("Generating adaptive pathway..."):
                try:
                    mastery = {}
                    missions = []
                    if mastery_json.strip():
                        import json
                        mastery = json.loads(mastery_json)
                    if missions_json.strip():
                        import json
                        missions = json.loads(missions_json)

                    result = engine.generate_pathway(interests, learning_style, mastery, missions)

                    if result.get("overall_reasoning"):
                        st.info(result["overall_reasoning"])

                    for p in result.get("pathways", []):
                        with st.expander(f"📚 {p['name']} ({p['difficulty'].capitalize()})", expanded=True):
                            st.markdown(f"**{p.get('description', '')}**")
                            st.markdown(f"*Reason:* {p.get('reason', '')}")
                            st.markdown("**Missions:**")
                            for m in p.get("missions", []):
                                st.markdown(
                                    f"- **{m['title']}** — ⏱ {m.get('estimated_minutes', '?')} min "
                                    f"| 🎯 Difficulty: {'⭐' * m.get('difficulty', 1)} "
                                    f"| ✨ {m.get('xp', 50)} XP"
                                )
                except Exception as e:
                    st.error(f"Error: {e}")

with tab2:
    st.subheader("Remedial Mission Generator")

    weak_topics = st.text_area(
        "Weak Topics (comma separated)",
        "Trigonometry, Linear Equations",
        help="Topics the student is struggling with",
    )

    remedial_style = st.selectbox(
        "Learning Style",
        ["visual", "auditory", "read/write", "kinesthetic", "visual_kinesthetic"],
        key="remedial_style",
    )

    if st.button("Generate Remedial Mission", type="primary", use_container_width=True):
        if not has_api:
            st.warning("GEMINI_API_KEY not configured.")
        else:
            with st.spinner("Creating remedial mission..."):
                try:
                    topics = [t.strip() for t in weak_topics.split(",") if t.strip()]
                    result = engine.generate_remedial_mission(topics, remedial_style)

                    for m in result.get("remedial_missions", []):
                        st.success(f"🎯 {m['title']}")
                        st.markdown(f"**{m.get('description', '')}**")
                        st.markdown(f"Type: {m.get('type', 'quiz').capitalize()} | "
                                    f"Difficulty: {'⭐' * m.get('difficulty', 1)} | "
                                    f"✨ {m.get('xp_reward', 60)} XP | "
                                    f"⏱ {m.get('estimated_minutes', 15)} min")
                        if m.get("tips"):
                            st.markdown("**Tips:**")
                            for tip in m["tips"]:
                                st.markdown(f"- 💡 {tip}")
                except Exception as e:
                    st.error(f"Error: {e}")
