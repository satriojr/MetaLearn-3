import streamlit as st
import plotly.graph_objects as go
from engines.bkt.engine import BKTEngine

st.set_page_config(page_title="BKT Engine", page_icon="📊")
st.title("📊 BKT Engine — Bayesian Knowledge Tracing")
st.markdown("Simulate and visualize student mastery estimation.")

with st.sidebar:
    st.subheader("BKT Parameters")
    p_init = st.slider("Initial Mastery (p_init)", 0.0, 1.0, 0.20, 0.05)
    p_learn = st.slider("Learning Rate (p_learn)", 0.0, 1.0, 0.15, 0.05)
    p_guess = st.slider("Guess Rate (p_guess)", 0.0, 1.0, 0.10, 0.05)
    p_slip = st.slider("Slip Rate (p_slip)", 0.0, 1.0, 0.05, 0.05)

engine = BKTEngine(params={"p_init": p_init, "p_learn": p_learn, "p_guess": p_guess, "p_slip": p_slip})

tab1, tab2 = st.tabs(["Step-by-Step Simulation", "Batch Evaluation"])

with tab1:
    st.subheader("Simulate Answer Sequence")
    st.markdown("Toggle correct/incorrect for each answer and see how mastery updates.")

    if "answer_history" not in st.session_state:
        st.session_state.answer_history = []
    if "mastery_history" not in st.session_state:
        st.session_state.mastery_history = [p_init]

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("✅ Correct", use_container_width=True, type="primary"):
            current = st.session_state.mastery_history[-1]
            new_mastery = engine.update_mastery(current, is_correct=True)
            st.session_state.answer_history.append(True)
            st.session_state.mastery_history.append(new_mastery)
            st.rerun()
    with col2:
        if st.button("❌ Incorrect", use_container_width=True):
            current = st.session_state.mastery_history[-1]
            new_mastery = engine.update_mastery(current, is_correct=False)
            st.session_state.answer_history.append(False)
            st.session_state.mastery_history.append(new_mastery)
            st.rerun()

    with col3:
        if st.button("Reset", use_container_width=True):
            st.session_state.answer_history = []
            st.session_state.mastery_history = [p_init]
            st.rerun()

    if st.session_state.answer_history:
        history = st.session_state.mastery_history
        answers = st.session_state.answer_history

        st.subheader("Mastery Progression")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            y=history,
            mode="lines+markers",
            name="Mastery Probability",
            line=dict(color="#636efa", width=3),
            marker=dict(
                size=10,
                color=["green" if a else "red" for a in answers],
                symbol=["check" if a else "x" for a in answers],
            ),
        ))
        fig.add_hline(y=0.8, line_dash="dash", line_color="green", annotation_text="Mastery Threshold (0.8)")
        fig.update_layout(
            xaxis_title="Attempt",
            yaxis_title="P(Mastery)",
            yaxis_range=[0, 1],
            height=400,
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Answer Log")
        for i, (a, m) in enumerate(zip(answers, history[1:]), 1):
            icon = "✅" if a else "❌"
            remediate = "⚠️ Needs remediation" if engine.should_remediate(m) else "✅ Mastered"
            st.write(f"{i}. {icon} {'Correct' if a else 'Incorrect'} → P(mastery) = **{m:.4f}** — {remediate}")
    else:
        st.info("Click **Correct** or **Incorrect** to start the simulation.")

with tab2:
    st.subheader("Batch Evaluation")

    col1, col2 = st.columns(2)
    with col1:
        correct_count = st.number_input("Correct Answers", 0, 100, 7)
    with col2:
        total_count = st.number_input("Total Questions", 1, 100, 10)

    if st.button("Estimate Mastery", type="primary", use_container_width=True):
        mastery = engine.estimate_mastery(correct_count, total_count)
        remediate = engine.should_remediate(mastery)
        difficulty = engine.get_difficulty_adjustment(mastery)

        col1, col2, col3 = st.columns(3)
        col1.metric("Estimated Mastery", f"{mastery:.1%}")
        col2.metric("Needs Remediation", "⚠️ Yes" if remediate else "✅ No")
        col3.metric("Recommended Difficulty", difficulty.capitalize())

        st.subheader("Mastery Score Breakdown")
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=mastery * 100,
            domain={"x": [0, 1], "y": [0, 1]},
            title={"text": "Mastery %"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "darkblue"},
                "steps": [
                    {"range": [0, 40], "color": "lightcoral"},
                    {"range": [40, 70], "color": "gold"},
                    {"range": [70, 100], "color": "lightgreen"},
                ],
                "threshold": {
                    "line": {"color": "red", "width": 4},
                    "thickness": 0.75,
                    "value": 80,
                },
            },
        ))
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
