import streamlit as st
from engines.nlp.engine import GeminiNLPEngine

st.set_page_config(page_title="NLP Engine", page_icon="💬")
st.title("💬 NLP Engine — Pause & Ask AI")
st.markdown("Test Natural Language Processing features for the Pause & Ask AI system.")

engine = GeminiNLPEngine()
has_api = bool(engine.model)

tab1, tab2, tab3 = st.tabs(["Pause & Ask", "Generate Summary", "Generate Questions"])

with tab1:
    st.subheader("Ask AI a Question")
    question = st.text_area("Question", placeholder="Explain the concept of photosynthesis...")
    mission_context = st.text_area("Mission Context (optional)", height=100,
                                   placeholder="Current learning material context...")
    memory = st.text_area("Student Memory (optional)", height=100,
                          placeholder="Previous learning memory...")

    if st.button("Ask AI", type="primary", use_container_width=True):
        if not question.strip():
            st.error("Please enter a question.")
        elif not has_api:
            st.warning("GEMINI_API_KEY not configured. AI response unavailable.")
        else:
            with st.spinner("AI is thinking..."):
                try:
                    answer = engine.ask(question, {"mission_context": mission_context, "memory": memory})
                    st.success("Answer")
                    st.markdown(answer)
                except Exception as e:
                    st.error(f"Error: {e}")

with tab2:
    st.subheader("Generate Session Summary")
    col1, col2 = st.columns(2)
    with col1:
        session_data = {
            "topic": st.text_input("Topic", "Mathematics"),
            "missions_completed": st.number_input("Missions Completed", 0, 50, 3),
            "score": st.slider("Score", 0, 100, 75),
            "xp_earned": st.number_input("XP Earned", 0, 500, 120),
            "duration_minutes": st.number_input("Duration (minutes)", 0, 180, 30),
        }
    with col2:
        session_memory = st.text_area("Previous Memory (optional)", height=150,
                                      placeholder="Previous session memory...")

    if st.button("Generate Summary", type="primary", use_container_width=True):
        if not has_api:
            st.warning("GEMINI_API_KEY not configured.")
        else:
            with st.spinner("Generating summary..."):
                try:
                    summary = engine.generate_summary(session_data, session_memory)
                    st.markdown(summary)
                except Exception as e:
                    st.error(f"Error: {e}")

with tab3:
    st.subheader("Generate Questions")
    topic = st.text_input("Topic", "Algebra")
    difficulty = st.selectbox("Difficulty", ["beginner", "intermediate", "advanced"])
    count = st.slider("Number of Questions", 1, 10, 5)

    if st.button("Generate Questions", type="primary", use_container_width=True):
        if not has_api:
            st.warning("GEMINI_API_KEY not configured.")
        else:
            with st.spinner("Generating questions..."):
                try:
                    questions = engine.generate_questions(topic, difficulty, count)
                    if questions:
                        st.success(f"Generated {len(questions)} questions")
                        for i, q in enumerate(questions, 1):
                            with st.expander(f"Question {i}: {q.get('question_text', '')[:80]}..."):
                                st.json(q)
                    else:
                        st.info("No questions generated.")
                except Exception as e:
                    st.error(f"Error: {e}")
