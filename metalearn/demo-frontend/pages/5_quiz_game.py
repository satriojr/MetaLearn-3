import streamlit as st
import random
import time
import plotly.graph_objects as go

st.set_page_config(page_title="Quiz Game — MetaLearn Demo", page_icon="🎮", layout="wide")

if not st.session_state.get("token") and not st.session_state.get("guest"):
    st.switch_page("demo_app.py")

if "quiz_state" not in st.session_state:
    st.session_state.quiz_state = {
        "topic": None,
        "questions": [],
        "index": 0,
        "score": 0,
        "combo": 0,
        "max_combo": 0,
        "answers": [],
        "start_time": None,
        "finished": False,
        "total_time": 0,
    }
if "quiz_highscores" not in st.session_state:
    st.session_state.quiz_highscores = []

QUESTION_BANKS = {
    "Algebra": [
        {"q": "Solve for x: 2x + 6 = 14", "opts": ["x = 3", "x = 4", "x = 5", "x = 6"], "ans": 1},
        {"q": "What is the slope of y = 3x + 2?", "opts": ["2", "3", "5", "1"], "ans": 1},
        {"q": "Factor: x² + 5x + 6", "opts": ["(x+2)(x+3)", "(x+1)(x+6)", "(x+2)(x+4)", "(x+3)(x+3)"], "ans": 0},
        {"q": "What is the y-intercept of y = -2x + 7?", "opts": ["-2", "2", "5", "7"], "ans": 3},
        {"q": "If f(x) = x² - 4, find f(3)", "opts": ["3", "5", "9", "13"], "ans": 1},
        {"q": "Solve: 3(x - 4) = 21", "opts": ["x = 7", "x = 9", "x = 11", "x = 25"], "ans": 2},
        {"q": "What is the domain of √(x - 2)?", "opts": ["x > 0", "x ≥ 2", "x ≤ 2", "All reals"], "ans": 1},
        {"q": "Simplify: (x³)(x⁴)", "opts": ["x⁷", "x¹²", "2x⁷", "x"], "ans": 0},
        {"q": "What is the vertex of y = x² - 6x + 10?", "opts": ["(0, 10)", "(3, 1)", "(-3, 37)", "(6, 10)"], "ans": 1},
        {"q": "Solve the system: x + y = 10, x - y = 2", "opts": ["x=4, y=6", "x=6, y=4", "x=5, y=5", "x=8, y=2"], "ans": 1},
        {"q": "What is the range of f(x) = |x|?", "opts": ["All reals", "y ≥ 0", "y > 0", "x ≥ 0"], "ans": 1},
        {"q": "If log₂(x) = 5, find x", "opts": ["10", "25", "32", "64"], "ans": 2},
    ],
    "Geometry": [
        {"q": "Area of a circle with radius 7 cm?", "opts": ["49π cm²", "14π cm²", "7π cm²", "21π cm²"], "ans": 0},
        {"q": "Sum of interior angles in a hexagon?", "opts": ["540°", "720°", "900°", "1080°"], "ans": 1},
        {"q": "Pythagorean theorem applies to...", "opts": ["Any triangle", "Right triangles", "Equilateral", "Isosceles"], "ans": 1},
        {"q": "Volume of a sphere with radius r?", "opts": ["(4/3)πr³", "4πr²", "πr²h", "2πr"], "ans": 0},
        {"q": "A triangle with sides 3, 4, 5 is...", "opts": ["Acute", "Right", "Obtuse", "Equilateral"], "ans": 1},
        {"q": "How many faces does a cube have?", "opts": ["4", "6", "8", "12"], "ans": 1},
        {"q": "What is π to 4 decimal places?", "opts": ["3.1415", "3.1416", "3.1419", "3.1420"], "ans": 1},
        {"q": "Area of a triangle with base 10, height 6?", "opts": ["60", "30", "16", "20"], "ans": 1},
        {"q": "Circumference of circle with diameter 10?", "opts": ["31.4", "62.8", "10π", "Both a and c"], "ans": 3},
        {"q": "Shape with infinite lines of symmetry?", "opts": ["Square", "Rectangle", "Circle", "Triangle"], "ans": 2},
        {"q": "Coordinate of midpoint between (1,2) and (5,6)?", "opts": ["(2,3)", "(3,4)", "(4,5)", "(6,8)"], "ans": 1},
        {"q": "Surface area of a sphere radius 3?", "opts": ["36π", "27π", "9π", "12π"], "ans": 0},
    ],
    "Calculus": [
        {"q": "Derivative of x³?", "opts": ["3x²", "x²", "3x³", "x⁴/4"], "ans": 0},
        {"q": "∫ 2x dx from 0 to 3?", "opts": ["6", "9", "18", "3"], "ans": 1},
        {"q": "Limit as x→0 of sin(x)/x?", "opts": ["0", "1", "∞", "Undefined"], "ans": 1},
        {"q": "Derivative of eˣ?", "opts": ["xeˣ⁻¹", "eˣ", "ln(x)", "1/x"], "ans": 1},
        {"q": "∫ 1/x dx = ?", "opts": ["ln|x| + C", "1/x² + C", "x + C", "eˣ + C"], "ans": 0},
        {"q": "Second derivative of x⁴ at x=2?", "opts": ["24", "48", "12", "96"], "ans": 1},
        {"q": "Derivative of sin(x)?", "opts": ["cos(x)", "-cos(x)", "-sin(x)", "tan(x)"], "ans": 0},
        {"q": "∫ cos(x) dx = ?", "opts": ["sin(x) + C", "-sin(x) + C", "cos(x) + C", "-cos(x) + C"], "ans": 0},
        {"q": "What is a critical point?", "opts": ["Where f'(x) = 0", "Where f(x) = 0", "Where f''(x) = 0", "Max of f(x)"], "ans": 0},
        {"q": "Derivative of ln(x)?", "opts": ["1/x", "ln(x)", "x", "eˣ"], "ans": 0},
        {"q": "∫₀¹ x² dx = ?", "opts": ["1/3", "1/2", "1", "2/3"], "ans": 0},
        {"q": "Derivative using chain rule: (2x+1)³?", "opts": ["6(2x+1)²", "3(2x+1)²", "6x+3", "2(2x+1)²"], "ans": 0},
    ],
    "Physics": [
        {"q": "F = ma is which law?", "opts": ["1st", "2nd", "3rd", "Gravitational"], "ans": 1},
        {"q": "Speed of light in vacuum?", "opts": ["3×10⁶ m/s", "3×10⁸ m/s", "3×10¹⁰ m/s", "3×10⁵ m/s"], "ans": 1},
        {"q": "Unit of force?", "opts": ["Joule", "Newton", "Watt", "Pascal"], "ans": 1},
        {"q": "Kinetic energy formula?", "opts": ["mv²/2", "mgh", "mv", "ma"], "ans": 0},
        {"q": "What does a transformer change?", "opts": ["Frequency", "Voltage", "Power", "Resistance"], "ans": 1},
        {"q": "Wavelength of a wave with f=50Hz, v=340m/s?", "opts": ["6.8m", "17,000m", "0.147m", "290m"], "ans": 0},
        {"q": "Unit of electrical resistance?", "opts": ["Volt", "Ampere", "Ohm", "Watt"], "ans": 2},
        {"q": "What is the acceleration due to gravity?", "opts": ["8.9 m/s²", "9.8 m/s²", "10.8 m/s²", "11.2 m/s²"], "ans": 1},
        {"q": "Conservation of momentum applies to...", "opts": ["Elastic only", "Inelastic only", "Both", "Neither"], "ans": 2},
        {"q": "Refraction is caused by change in...", "opts": ["Frequency", "Speed", "Amplitude", "Phase"], "ans": 1},
        {"q": "Ohm's Law: V = ?", "opts": ["IR", "I/R", "R/I", "I²R"], "ans": 0},
        {"q": "Work formula?", "opts": ["Fd", "F/d", "Fd²", "ma"], "ans": 0},
    ],
    "Biology": [
        {"q": "Basic unit of life?", "opts": ["Atom", "Cell", "Tissue", "Organ"], "ans": 1},
        {"q": "DNA stands for...", "opts": ["Deoxyribonucleic Acid", "Dinitrogen Acid", "Double Nuclear Acid", "Dual Nucleic Acid"], "ans": 0},
        {"q": "Where does photosynthesis occur?", "opts": ["Nucleus", "Mitochondria", "Chloroplast", "Ribosome"], "ans": 2},
        {"q": "How many chromosomes in humans?", "opts": ["23", "46", "44", "48"], "ans": 1},
        {"q": "Blood is what type of tissue?", "opts": ["Epithelial", "Connective", "Muscle", "Nervous"], "ans": 1},
        {"q": "Organelle for energy production?", "opts": ["Nucleus", "Mitochondria", "Ribosome", "Golgi"], "ans": 1},
        {"q": "What is mitosis?", "opts": ["Cell division", "Cell death", "Cell growth", "Protein synthesis"], "ans": 0},
        {"q": "Hemoglobin contains which metal?", "opts": ["Magnesium", "Iron", "Copper", "Zinc"], "ans": 1},
        {"q": "Largest organ in human body?", "opts": ["Liver", "Brain", "Skin", "Heart"], "ans": 2},
        {"q": "Enzymes are made of...", "opts": ["Carbohydrates", "Lipids", "Proteins", "Nucleic acids"], "ans": 2},
        {"q": "pH of pure water?", "opts": ["5", "6", "7", "8"], "ans": 2},
        {"q": "Function of red blood cells?", "opts": ["Fight infection", "Carry oxygen", "Clot blood", "Produce antibodies"], "ans": 1},
    ],
}

TOPICS = [
    {"id": "Algebra", "color": "#6366f1", "icon": "📐"},
    {"id": "Geometry", "color": "#06b6d4", "icon": "🔷"},
    {"id": "Calculus", "color": "#f59e0b", "icon": "∫"},
    {"id": "Physics", "color": "#ef4444", "icon": "⚛️"},
    {"id": "Biology", "color": "#22c55e", "icon": "🧬"},
]

TIME_PER_Q = 15

qs = st.session_state.quiz_state

st.markdown("""
<style>
    .quiz-timer {font-size:3rem;font-weight:700;text-align:center;font-variant-numeric:tabular-nums;}
    .quiz-question {font-size:1.3rem;font-weight:500;padding:1rem 0;}
    .quiz-score {font-size:1.5rem;font-weight:600;}
    .quiz-combo {font-size:1.1rem;}
    .game-over {animation: pulse 1.5s infinite;}
    .st-key-opt div[data-testid="column"] {transition: transform 0.2s;}
    .st-key-opt button {height:3.5rem !important;font-size:1.1rem !important;}
    .correct-answer {border: 3px solid #4CAF50 !important;background:rgba(76,175,80,0.1) !important;}
    .wrong-answer {border: 3px solid #f44336 !important;background:rgba(244,67,54,0.1) !important;}
</style>
""", unsafe_allow_html=True)

def start_quiz(topic_name):
    bank = QUESTION_BANKS[topic_name]
    selected = random.sample(bank, min(10, len(bank)))
    qs["topic"] = topic_name
    qs["questions"] = [
        {"q": item["q"], "opts": item["opts"], "ans": item["ans"], "chosen": None, "time_taken": 0}
        for item in selected
    ]
    qs["index"] = 0
    qs["score"] = 0
    qs["combo"] = 0
    qs["max_combo"] = 0
    qs["answers"] = []
    qs["start_time"] = time.time()
    qs["finished"] = False
    qs["total_time"] = 0

def answer_question(idx):
    chosen = qs["questions"][idx]["chosen"]
    correct = qs["questions"][idx]["ans"]
    if chosen is None:
        return False
    is_correct = chosen == correct
    if is_correct:
        qs["combo"] += 1
        qs["max_combo"] = max(qs["max_combo"], qs["combo"])
        combo_bonus = min(qs["combo"] - 1, 5)
        base = 100
        time_bonus = max(0, int((TIME_PER_Q - qs["questions"][idx]["time_taken"]) * 5))
        earned = base + time_bonus + combo_bonus * 20
    else:
        qs["combo"] = 0
        earned = 0
    qs["score"] += earned
    qs["answers"].append({"correct": is_correct, "earned": earned, "time": qs["questions"][idx]["time_taken"]})

def next_question():
    qs["index"] += 1
    if qs["index"] >= len(qs["questions"]):
        qs["finished"] = True
        qs["total_time"] = time.time() - qs["start_time"]
        entry = {
            "topic": qs["topic"],
            "score": qs["score"],
            "max_combo": qs["max_combo"],
            "correct": sum(1 for a in qs["answers"] if a["correct"]),
            "total": len(qs["answers"]),
            "time": round(qs["total_time"], 1),
        }
        st.session_state.quiz_highscores.append(entry)
        st.session_state.quiz_highscores.sort(key=lambda x: x["score"], reverse=True)
        st.session_state.quiz_highscores = st.session_state.quiz_highscores[:10]

if qs["topic"] is None or qs["finished"]:
    if qs["finished"]:
        st.title("🎉 Quiz Complete!")
        st.markdown(f"<div style='text-align:center;'>", unsafe_allow_html=True)

        total = len(qs["answers"])
        correct = sum(1 for a in qs["answers"] if a["correct"])
        pct = (correct / total * 100) if total > 0 else 0

        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=pct,
            number={"suffix": "%", "font": {"size": 48}},
            delta={"reference": 80, "increasing": {"color": "#4CAF50"}, "decreasing": {"color": "#f44336"}},
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 1},
                "bar": {"color": "#4CAF50" if pct >= 80 else "#FF9800" if pct >= 60 else "#f44336"},
                "steps": [
                    {"range": [0, 40], "color": "#FFCDD2"},
                    {"range": [40, 70], "color": "#FFE0B2"},
                    {"range": [70, 100], "color": "#C8E6C9"},
                ],
                "threshold": {"line": {"color": "#2196F3", "width": 4}, "thickness": 0.75, "value": 80},
            }
        ))
        fig.update_layout(height=300, margin=dict(l=20, r=20, t=30, b=0))
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Correct", f"{correct}/{total}", f"{pct:.0f}%")
        c2.metric("Total Score", f"{qs['score']:,}")
        c3.metric("Best Combo", f"{qs['max_combo']}x🔥")
        c4.metric("Time", f"{qs['total_time']:.1f}s")

        topic_color = next(t["color"] for t in TOPICS if t["id"] == qs["topic"])
        fig2 = go.Figure()
        results = qs["answers"]
        fig2.add_trace(go.Scatter(
            x=list(range(1, len(results) + 1)),
            y=[r["earned"] for r in results],
            mode="lines+markers",
            marker=dict(
                size=12,
                color=["#4CAF50" if r["correct"] else "#f44336" for r in results],
                line=dict(width=2, color="white"),
            ),
            line=dict(color=topic_color, width=2, dash="dot"),
            name="Score per question",
        ))
        fig2.update_layout(
            title="Score per Question",
            xaxis_title="Question #",
            yaxis_title="Points Earned",
            height=250,
            hovermode="x unified",
        )
        st.plotly_chart(fig2, use_container_width=True)

        grade = "⭐" if pct >= 90 else "🌟" if pct >= 80 else "👍" if pct >= 60 else "💪"
        msg = "Outstanding! Perfect mastery!" if pct >= 90 else "Great job! Keep it up!" if pct >= 80 else "Good effort! Review the topics." if pct >= 60 else "Don't give up! Practice makes perfect."
        st.markdown(f"<div style='text-align:center;font-size:1.5rem;padding:0.5rem;'>{grade} {msg}</div>", unsafe_allow_html=True)

        if qs["max_combo"] >= 5:
            st.balloons()

        st.divider()

        if st.session_state.quiz_highscores:
            st.subheader("🏆 High Scores")
            for i, entry in enumerate(st.session_state.quiz_highscores[:5]):
                medal = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"][i] if i < 5 else f"#{i+1}"
                with st.container(border=True):
                    cols = st.columns([0.5, 1.5, 2, 1, 1, 1])
                    cols[0].markdown(f"**{medal}**")
                    cols[1].markdown(f"**{entry['topic']}**")
                    cols[2].markdown(f"📈 {entry['score']:,}")
                    cols[3].markdown(f"✅ {entry['correct']}/{entry['total']}")
                    cols[4].markdown(f"🔥 {entry['max_combo']}x")
                    cols[5].markdown(f"⏱ {entry['time']}s")

        st.divider()
        col1, col2 = st.columns(2)
        if col1.button("🔄 Play Again", use_container_width=True, type="primary"):
            qs["topic"] = None
            qs["finished"] = False
            st.rerun()
        if col2.button("🏠 Back to Home", use_container_width=True):
            qs["topic"] = None
            qs["finished"] = False
            st.switch_page("demo_app.py")
    else:
        st.title("🎮 Quiz Game")
        st.markdown("Test your knowledge with timed quizzes! Pick a topic to begin.")

        st.divider()
        st.subheader("📚 Choose a Topic")

        topic_cols = st.columns(len(TOPICS))
        for i, topic in enumerate(TOPICS):
            with topic_cols[i]:
                with st.container(border=True):
                    st.markdown(f"<div style='text-align:center;font-size:3rem;'>{topic['icon']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='text-align:center;font-weight:600;'>{topic['id']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='text-align:center;font-size:0.8rem;color:gray;'>10 questions<br>{TIME_PER_Q}s per question</div>", unsafe_allow_html=True)
                    if st.button("Play", key=f"start_{topic['id']}", use_container_width=True):
                        start_quiz(topic["id"])
                        st.rerun()

        if st.session_state.quiz_highscores:
            st.divider()
            st.subheader("🏆 High Scores")
            for i, entry in enumerate(st.session_state.quiz_highscores[:5]):
                medal = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"][i] if i < 5 else f"#{i+1}"
                with st.container(border=True):
                    cols = st.columns([0.5, 1.5, 2, 1, 1, 1])
                    cols[0].markdown(f"**{medal}**")
                    cols[1].markdown(f"**{entry['topic']}**")
                    cols[2].markdown(f"📈 {entry['score']:,}")
                    cols[3].markdown(f"✅ {entry['correct']}/{entry['total']}")
                    cols[4].markdown(f"🔥 {entry['max_combo']}x")
                    cols[5].markdown(f"⏱ {entry['time']}s")
else:
    total_q = len(qs["questions"])
    idx = qs["index"]
    q_data = qs["questions"][idx]

    elapsed = time.time() - qs["start_time"]
    elapsed_per_q = elapsed - sum(qs["questions"][i]["time_taken"] for i in range(idx))
    remaining = max(0, TIME_PER_Q - int(elapsed_per_q))

    topic_color = next(t["color"] for t in TOPICS if t["id"] == qs["topic"])

    st.markdown(f"""
    <div style='display:flex;align-items:center;gap:1rem;margin-bottom:0.5rem;'>
        <span style='font-size:2rem;'>{next(t['icon'] for t in TOPICS if t['id'] == qs['topic'])}</span>
        <span style='font-size:1.5rem;font-weight:600;'>{qs['topic']}</span>
        <span style='margin-left:auto;font-size:0.9rem;color:gray;'>Question {idx+1} of {total_q}</span>
    </div>
    """, unsafe_allow_html=True)

    st.progress((idx + 1) / total_q)

    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        timer_color = "#f44336" if remaining <= 5 else "#FF9800" if remaining <= 10 else "#4CAF50"
        st.markdown(f"<div class='quiz-timer' style='color:{timer_color};'>{remaining}s</div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='quiz-score'>💰 {qs['score']:,}</div>", unsafe_allow_html=True)
    with c3:
        combo_color = "#FF9800" if qs["combo"] >= 3 else "#90A4AE"
        st.markdown(f"<div class='quiz-combo' style='color:{combo_color};'>🔥 x{qs['combo']}</div>", unsafe_allow_html=True)

    st.markdown(f"<div class='quiz-question'>{q_data['q']}</div>", unsafe_allow_html=True)

    disabled = q_data["chosen"] is not None
    cols = st.columns(2)
    for i, opt in enumerate(q_data["opts"]):
        with cols[i % 2]:
            if disabled:
                style = ""
                if i == q_data["ans"]:
                    style = "correct-answer"
                elif i == q_data["chosen"] and i != q_data["ans"]:
                    style = "wrong-answer"
                st.markdown(f"<div class='{style}' style='padding:0.75rem;border-radius:8px;border:2px solid #e0e0e0;'>{opt}</div>", unsafe_allow_html=True)
            else:
                if st.button(opt, key=f"opt_{i}", use_container_width=True, disabled=disabled):
                    q_data["chosen"] = i
                    q_data["time_taken"] = elapsed_per_q
                    answer_question(idx)
                    st.rerun()

    if remaining <= 0 and q_data["chosen"] is None:
        q_data["chosen"] = -1
        q_data["time_taken"] = TIME_PER_Q
        answer_question(idx)
        st.rerun()

    if q_data["chosen"] is not None:
        if idx < total_q - 1:
            if st.button("Next →", use_container_width=True, type="primary"):
                next_question()
                st.rerun()
        else:
            if st.button("🎉 See Results", use_container_width=True, type="primary"):
                next_question()
                st.rerun()

    st.markdown(f"<div style='display:flex;gap:0.25rem;justify-content:center;margin-top:1rem;'>", unsafe_allow_html=True)
    dot_html = ""
    for i in range(total_q):
        a = qs["questions"][i]
        if a["chosen"] is not None:
            if a["chosen"] == a["ans"]:
                dot_html += f"<span style='width:12px;height:12px;border-radius:50%;background:#4CAF50;display:inline-block;'></span>"
            else:
                dot_html += f"<span style='width:12px;height:12px;border-radius:50%;background:#f44336;display:inline-block;'></span>"
        elif i == idx:
            dot_html += f"<span style='width:12px;height:12px;border-radius:50%;background:{topic_color};display:inline-block;box-shadow: 0 0 4px {topic_color};'></span>"
        else:
            dot_html += f"<span style='width:12px;height:12px;border-radius:50%;background:#E0E0E0;display:inline-block;'></span>"
    st.markdown(f"<div style='display:flex;gap:0.35rem;justify-content:center;'>{dot_html}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
