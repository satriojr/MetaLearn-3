import streamlit as st
import json
from engines.ast_evaluator.engine import ASTEvaluator

st.set_page_config(page_title="AST Evaluator", page_icon="🔍")
st.title("🔍 AST Evaluator — Knowledge Tree Assessment")
st.markdown("Evaluate student answers using structural and semantic comparison.")

engine = ASTEvaluator()
has_api = bool(engine.model)

tab1, tab2 = st.tabs(["Text Evaluation", "Structure Evaluation"])

with tab1:
    st.subheader("Evaluate Text Answer")

    col1, col2 = st.columns(2)
    with col1:
        question_text = st.text_area(
            "Question",
            value="What is the result of photosynthesis?",
            height=80,
        )
        correct_answer = st.text_area(
            "Correct Answer",
            value="Plants convert sunlight into chemical energy (glucose) and release oxygen.",
            height=80,
        )
    with col2:
        student_answer = st.text_area(
            "Student Answer",
            value="Plants makes glucose from sunlight and oxygen is released.",
            height=80,
        )

    if st.button("Evaluate", type="primary", use_container_width=True):
        with st.spinner("Evaluating..."):
            try:
                result = engine.evaluate(student_answer, correct_answer, question_text)
                _display_result(result)
            except Exception as e:
                st.error(f"Error: {e}")

with tab2:
    st.subheader("Evaluate Structured Answer")

    st.markdown("Compare two structured (JSON/dict) answers.")

    col1, col2 = st.columns(2)
    with col1:
        expected_structure = st.text_area(
            "Expected Structure (JSON)",
            value=json.dumps({
                "type": "linear_equation",
                "coefficient": 2,
                "variable": "x",
                "constant": 6,
                "solution": 3,
            }, indent=2),
            height=200,
        )
    with col2:
        student_structure = st.text_area(
            "Student Structure (JSON)",
            value=json.dumps({
                "type": "linear_equation",
                "coefficient": 2,
                "variable": "x",
                "constant": 6,
                "solution": 3,
            }, indent=2),
            height=200,
        )

    if st.button("Evaluate Structure", type="primary", use_container_width=True):
        with st.spinner("Comparing structures..."):
            try:
                expected = json.loads(expected_structure)
                student = json.loads(student_structure)
                result = engine.evaluate_structure(student, expected)
                _display_result(result)
            except json.JSONDecodeError as e:
                st.error(f"Invalid JSON: {e}")
            except Exception as e:
                st.error(f"Error: {e}")


def _display_result(result: dict):
    col1, col2, col3 = st.columns(3)
    is_correct = result.get("is_correct", False)
    col1.metric("Result", "✅ Correct" if is_correct else "❌ Incorrect")
    col2.metric("Score", f"{result.get('score', 0)}/100")
    col3.metric("Confidence", f"{result.get('confidence', 0):.0%}")

    st.markdown(f"**Feedback:** {result.get('feedback', 'No feedback')}")
