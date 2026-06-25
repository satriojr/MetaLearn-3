import streamlit as st
import sys
import os
import time
import json
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from engines.nlp.engine import GeminiNLPEngine
from engines.ast_evaluator.engine import ASTEvaluator
from engines.bkt.engine import BKTEngine

st.set_page_config(page_title="AI Quiz Engine", page_icon="🧪", layout="wide")

nlp = GeminiNLPEngine()
ast = ASTEvaluator()
bkt = BKTEngine()
has_api = bool(nlp.model)

if "ai_quiz" not in st.session_state:
    st.session_state.ai_quiz = {
        "questions": [],
        "index": 0,
        "results": [],
        "mastery": 0.2,
        "started": False,
        "finished": False,
    }

SAMPLE_QUESTIONS = {
    "Matematika": [
        {"question_text": "Hitung turunan pertama dari f(x) = 3x² + 2x - 5", "correct_answer": "f'(x) = 6x + 2", "type": "short_answer"},
        {"question_text": "Berapa luas lingkaran dengan jari-jari 7 cm? (π = 22/7)", "correct_answer": "154 cm²", "type": "short_answer"},
        {"question_text": "Sederhanakan: 3(x + 2) - 2(x - 1)", "correct_answer": "x + 8", "type": "short_answer"},
        {"question_text": "Jelaskan konsep limit fungsi dalam kalkulus", "correct_answer": "Limit adalah nilai yang didekati fungsi saat variabel mendekati titik tertentu", "type": "short_answer"},
        {"question_text": "Hitung determinan matriks [[2, 3], [4, 5]]", "correct_answer": "-2", "type": "short_answer"},
    ],
    "Fisika": [
        {"question_text": "Jelaskan Hukum Newton II tentang gerak", "correct_answer": "Percepatan benda sebanding dengan gaya total dan berbanding terbalik dengan massanya", "type": "short_answer"},
        {"question_text": "Berapa energi kinetik benda bermassa 2 kg bergerak 3 m/s?", "correct_answer": "9 joule", "type": "short_answer"},
        {"question_text": "Apa yang dimaksud dengan efek fotolistrik?", "correct_answer": "Efek terlepasnya elektron dari permukaan logam saat disinari cahaya", "type": "short_answer"},
        {"question_text": "Jelaskan hukum kekekalan momentum", "correct_answer": "Momentum total sistem tertutup tetap konstan jika tidak ada gaya luar", "type": "short_answer"},
        {"question_text": "Hitung hambatan total rangkaian seri: R₁=2Ω, R₂=3Ω, R₃=5Ω", "correct_answer": "10 ohm", "type": "short_answer"},
    ],
    "Biologi": [
        {"question_text": "Jelaskan proses fotosintesis pada tumbuhan", "correct_answer": "Proses pembuatan makanan oleh tumbuhan menggunakan air, CO2, dan cahaya matahari menjadi glukosa dan oksigen", "type": "short_answer"},
        {"question_text": "Apa fungsi mitokondria dalam sel?", "correct_answer": "Menghasilkan energi dalam bentuk ATP melalui respirasi seluler", "type": "short_answer"},
        {"question_text": "Jelaskan perbedaan DNA dan RNA", "correct_answer": "DNA double helix, gula deoksiribosa, basa T; RNA single strand, gula ribosa, basa U", "type": "short_answer"},
        {"question_text": "Apa yang dimaksud dengan seleksi alam?", "correct_answer": "Mekanisme evolusi di mana organisme dengan sifat adaptif lebih mampu bertahan dan bereproduksi", "type": "short_answer"},
        {"question_text": "Jelaskan sistem peredaran darah manusia", "correct_answer": "Sistem peredaran darah tertutup ganda: jantung memompa darah ke paru-paru dan ke seluruh tubuh", "type": "short_answer"},
    ],
    "Kimia": [
        {"question_text": "Apa perbedaan ikatan ionik dan kovalen?", "correct_answer": "Ionik: transfer elektron antara logam dan nonlogam. Kovalen: pemakaian bersama elektron antar nonlogam", "type": "short_answer"},
        {"question_text": "Hitung Mr H₂SO₄ (Ar H=1, S=32, O=16)", "correct_answer": "98", "type": "short_answer"},
        {"question_text": "Jelaskan teori atom Bohr", "correct_answer": "Elektron mengelilingi inti pada lintasan stasioner tertentu dengan tingkat energi tetap", "type": "short_answer"},
        {"question_text": "Apa yang dimaksud dengan reaksi redoks?", "correct_answer": "Reaksi yang melibatkan reduksi (penurunan biloks) dan oksidasi (kenaikan biloks) secara bersamaan", "type": "short_answer"},
        {"question_text": "Sebutkan 3 sifat larutan asam", "correct_answer": "pH < 7, rasanya masam, mengubah lakmus biru jadi merah, korosif", "type": "short_answer"},
    ],
}

st.markdown("""
<style>
    .eval-correct {border-left:5px solid #4CAF50;background:rgba(76,175,80,0.08);padding:1rem;border-radius:4px;margin:0.5rem 0;}
    .eval-partial {border-left:5px solid #FF9800;background:rgba(255,152,0,0.08);padding:1rem;border-radius:4px;margin:0.5rem 0;}
    .eval-wrong {border-left:5px solid #f44336;background:rgba(244,67,54,0.08);padding:1rem;border-radius:4px;margin:0.5rem 0;}
    .stApp textarea {font-size:1rem !important;}
</style>
""", unsafe_allow_html=True)

st.title("🧪 AI-Powered Quiz Engine")
st.markdown("Test kuis dengan evaluasi jawaban berbasis AI — membandingkan AST Evaluator, BKT Mastery, dan NLP feedback.")

tab_kuis, tab_eval, tab_bkt, tab_hasil = st.tabs(["🎯 Quiz", "🔍 Evaluasi Jawaban", "📊 BKT Mastery", "📈 Hasil & Analisis"])

with tab_kuis:
    st.subheader("🎯 Uji Coba Kuis")

    col1, col2, col3 = st.columns(3)
    with col1:
        topic = st.selectbox("Topik", list(SAMPLE_QUESTIONS.keys()), key="ai_topic")
    with col2:
        diff = st.select_slider("Difficulty", options=["mudah", "sedang", "sulit"], value="sedang", key="ai_diff")
    with col3:
        if st.button("🔄 Generate Soal AI", use_container_width=True, disabled=not has_api):
            with st.spinner("AI generating questions..."):
                try:
                    ai_questions = nlp.generate_questions(topic, diff, 5)
                    if ai_questions:
                        st.session_state.ai_quiz["questions"] = []
                        for q in ai_questions:
                            opts = q.get("options", [])
                            correct = q.get("correct_answer", "")
                            correct_text = ""
                            for o in opts:
                                if o.get("label", "").strip().lower() == correct.strip().lower():
                                    correct_text = o.get("text", "")
                                    break
                            st.session_state.ai_quiz["questions"].append({
                                "question_text": q.get("question_text", ""),
                                "correct_answer": correct_text or correct,
                                "type": "short_answer",
                                "explanation": q.get("explanation", ""),
                                "ai_generated": True,
                            })
                        st.success(f"AI generated {len(ai_questions)} questions!")
                        st.rerun()
                except Exception as e:
                    st.error(f"AI generation failed: {e}")

    if st.button(f"📝 Load {topic} Questions", use_container_width=True):
        qs = SAMPLE_QUESTIONS[topic]
        st.session_state.ai_quiz["questions"] = [dict(q) for q in qs]
        st.session_state.ai_quiz["index"] = 0
        st.session_state.ai_quiz["results"] = []
        st.session_state.ai_quiz["mastery"] = 0.2
        st.session_state.ai_quiz["started"] = True
        st.session_state.ai_quiz["finished"] = False
        for q in st.session_state.ai_quiz["questions"]:
            q["explanation"] = ""
            q["ai_generated"] = False
        st.rerun()

    if not st.session_state.ai_quiz["started"]:
        st.info("👈 Pilih topik dan klik **Load Questions** untuk memulai.")
    elif st.session_state.ai_quiz["finished"]:
        st.success("✅ Kuis selesai! Lihat hasil di tab **📈 Hasil & Analisis**.")
        if st.button("🔄 Mulai Ulang", use_container_width=True):
            st.session_state.ai_quiz["started"] = False
            st.session_state.ai_quiz["finished"] = False
            st.session_state.ai_quiz["results"] = []
            st.rerun()
    else:
        qs = st.session_state.ai_quiz["questions"]
        idx = st.session_state.ai_quiz["index"]
        total = len(qs)

        st.progress((idx + 1) / total)
        st.markdown(f"**Soal {idx+1} dari {total}** — *{topic}*")
        q = qs[idx]

        with st.container(border=True):
            st.markdown(f"**{q['question_text']}**")
            answer = st.text_area("Jawaban kamu:", key=f"ai_answer_{idx}", height=100)

            col_a, col_b = st.columns([1, 1])
            with col_a:
                if st.button("Submit & Evaluate", type="primary", use_container_width=True):
                    if not answer.strip():
                        st.warning("Tulis jawaban terlebih dahulu.")
                    else:
                        ast_result = ast.evaluate(answer, q["correct_answer"], q["question_text"])

                        new_mastery = bkt.update_mastery(
                            st.session_state.ai_quiz["mastery"], ast_result["is_correct"]
                        )

                        feedback = ""
                        if has_api:
                            try:
                                fb = nlp.ask(
                                    f"Berikan feedback singkat (2-3 kalimat) untuk jawaban '{answer}' terhadap soal '{q['question_text']}' dengan jawaban benar '{q['correct_answer']}'. Fokus pada apa yang kurang dan saran perbaikan.",
                                    {"mission_context": q["question_text"]},
                                )
                                feedback = fb
                            except Exception:
                                feedback = ast_result.get("feedback", "")

                        result = {
                            "question": q["question_text"],
                            "correct_answer": q["correct_answer"],
                            "student_answer": answer,
                            "ast_result": ast_result,
                            "feedback": feedback,
                            "mastery_after": new_mastery,
                        }
                        st.session_state.ai_quiz["results"].append(result)
                        st.session_state.ai_quiz["mastery"] = new_mastery

                        if ast_result["is_correct"]:
                            st.success(f"✅ **Benar!** Skor: {ast_result['score']}/100, Confidence: {ast_result['confidence']:.0%}")
                        elif ast_result["score"] >= 50:
                            st.warning(f"⚠️ **Sebagian Benar.** Skor: {ast_result['score']}/100")
                        else:
                            st.error(f"❌ **Perlu Perbaikan.** Skor: {ast_result['score']}/100")

                        st.caption(f"Jawaban benar: _{q['correct_answer']}_")
                        if feedback:
                            st.info(f"💡 **AI Feedback:** {feedback}")
                        if q.get("explanation"):
                            st.markdown(f"📖 **Penjelasan:** {q['explanation']}")
                        st.caption(f"📊 BKT Mastery: {st.session_state.ai_quiz['mastery']:.1%}")

            with col_b:
                if st.button("Skip →", use_container_width=True):
                    pass

        if st.session_state.ai_quiz["results"] and len(st.session_state.ai_quiz["results"]) > idx:
            st.divider()
            if idx < total - 1:
                if st.button("Soal Selanjutnya →", use_container_width=True, type="primary"):
                    st.session_state.ai_quiz["index"] += 1
                    st.rerun()
            else:
                st.session_state.ai_quiz["finished"] = True
                st.rerun()

with tab_eval:
    st.subheader("🔍 Uji Evaluasi AST")
    st.markdown("Bandingkan jawaban siswa dengan jawaban benar menggunakan **AST Evaluator + AI fallback**.")

    col1, col2 = st.columns(2)
    with col1:
        test_question = st.text_area("Soal", "Jelaskan hukum Ohm dalam rangkaian listrik", height=80)
        test_correct = st.text_area("Jawaban Benar", "Tegangan berbanding lurus dengan arus dan hambatan: V = IR", height=80)
    with col2:
        test_answer = st.text_area("Jawaban Siswa", "V = I × R, dimana V adalah tegangan, I arus, R hambatan", height=80)

    if st.button("🔍 Evaluasi Sekarang", type="primary", use_container_width=True):
        with st.spinner("Evaluating..."):
            result = ast.evaluate(test_answer, test_correct, test_question)

        col1, col2, col3 = st.columns(3)
        col1.metric("Status", "✅ Benar" if result["is_correct"] else "❌ Salah")
        col2.metric("Score", f"{result['score']}/100")
        col3.metric("Confidence", f"{result['confidence']:.0%}")

        s = result["score"]
        cls = "eval-correct" if s >= 80 else "eval-partial" if s >= 40 else "eval-wrong"
        st.markdown(f"<div class='{cls}'>{result.get('feedback', '')}</div>", unsafe_allow_html=True)

        if has_api:
            with st.expander("💡 AI Feedback Detail"):
                fb = nlp.ask(
                    f"Evaluasi jawaban '{test_answer}' terhadap soal '{test_question}' (jawaban benar: '{test_correct}'). "
                    "Berikan analisis konseptual mendalam dalam 3-4 kalimat.",
                )
                st.markdown(fb)

    st.divider()
    st.subheader("📊 Matrix Perbandingan")
    st.markdown("Bandingkan beberapa tipe jawaban untuk soal yang sama:")

    col1, col2 = st.columns(2)
    with col1:
        m_q = st.text_input("Soal uji", value="Apa rumus energi kinetik?", key="m_q")
        m_correct = st.text_input("Jawaban benar", value="Ek = ½ mv²", key="m_correct")

    if "m_results" not in st.session_state:
        st.session_state.m_results = []

    with col2:
        new_answer = st.text_input("Jawaban siswa baru", key="m_new")
        if st.button("➕ Tambah & Evaluasi") and new_answer.strip():
            res = ast.evaluate(new_answer, m_correct, m_q)
            st.session_state.m_results.append({"answer": new_answer, **res})
            st.rerun()

    if st.session_state.m_results:
        data = []
        for i, r in enumerate(st.session_state.m_results):
            data.append({
                "Jawaban": r["answer"][:40] + "..." if len(r["answer"]) > 40 else r["answer"],
                "Score": r["score"],
                "Confidence": round(r["confidence"], 2),
                "Benar": "✅" if r["is_correct"] else "❌",
            })
        st.dataframe(data, use_container_width=True)

        fig = go.Figure(go.Bar(
            x=[r["answer"][:30] for r in st.session_state.m_results],
            y=[r["score"] for r in st.session_state.m_results],
            marker_color=["#4CAF50" if r["is_correct"] else "#f44336" for r in st.session_state.m_results],
            text=[f"{r['score']}" for r in st.session_state.m_results],
        ))
        fig.update_layout(title="Perbandingan Score Evaluasi", yaxis_range=[0, 110], height=300)
        st.plotly_chart(fig, use_container_width=True)

        if st.button("🗑️ Hapus Semua"):
            st.session_state.m_results = []
            st.rerun()

with tab_bkt:
    st.subheader("📊 Bayesian Knowledge Tracing — Simulasi")
    st.markdown("Simulasi perkiraan mastery BKT berdasarkan jawaban benar/salah berurutan.")

    col1, col2, col3 = st.columns(3)
    with col1:
        p_init = st.slider("Initial Mastery (P-init)", 0.0, 1.0, 0.2, 0.05, help="Probabilitas awal siswa sudah menguasai")
    with col2:
        p_learn = st.slider("Learning Rate (P-learn)", 0.0, 0.5, 0.15, 0.01, help="Probabilitas belajar per kesempatan")
    with col3:
        p_guess = st.slider("Guess Rate (P-guess)", 0.0, 0.5, 0.10, 0.01, help="Probabilitas menebak benar")

    sim_bkt = BKTEngine({"p_learn": p_learn, "p_guess": p_guess, "p_slip": 0.05, "p_init": p_init})

    col1, col2 = st.columns(2)
    with col1:
        sim_correct = st.slider("Jumlah jawaban benar", 0, 20, 8, help="Simulasi jumlah jawaban benar berurutan")
    with col2:
        seq_type = st.radio("Urutan jawaban", ["Semua benar", "Bergantian B/S", "Custom"], horizontal=True)

    mastery_curve = [p_init]
    if seq_type == "Semua benar":
        for i in range(sim_correct):
            mastery_curve.append(sim_bkt.update_mastery(mastery_curve[-1], True))
    elif seq_type == "Bergantian B/S":
        for i in range(sim_correct * 2):
            mastery_curve.append(sim_bkt.update_mastery(mastery_curve[-1], i % 2 == 0))
    else:
        custom_seq = st.text_input("Custom sequence (contoh: B,S,B,B,S)", value="B,S,B,B,S,B,B,B,S,B")
        tags = [c.strip() for c in custom_seq.split(",")]
        for t in tags:
            mastery_curve.append(sim_bkt.update_mastery(mastery_curve[-1], t.upper() == "B"))

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=list(range(len(mastery_curve))),
        y=[m * 100 for m in mastery_curve],
        mode="lines+markers",
        fill="tozeroy",
        marker=dict(size=8, color="#6366f1"),
        line=dict(width=3, color="#6366f1"),
    ))
    fig.add_hline(y=80, line_dash="dash", line_color="#4CAF50", annotation_text="Mastery Target (80%)")
    fig.add_hline(y=50, line_dash="dot", line_color="#FF9800", annotation_text="Remedial Threshold (50%)")
    fig.update_layout(
        title="BKT Mastery Simulation",
        xaxis_title="Kesempatan ke-",
        yaxis_title="Mastery Probability (%)",
        height=350,
        hovermode="x unified",
    )
    st.plotly_chart(fig, use_container_width=True)

    st.caption(f"Mastery akhir: {mastery_curve[-1]*100:.1f}% | Remediasi {'✅ diperlukan' if mastery_curve[-1] < 0.5 else '❌ tidak diperlukan'}")

with tab_hasil:
    st.subheader("📈 Hasil & Analisis Kuis AI")

    if not st.session_state.ai_quiz["results"]:
        st.info("Belum ada hasil kuis. Selesaikan kuis di tab **🎯 Quiz** terlebih dahulu.")
    else:
        results = st.session_state.ai_quiz["results"]
        total = len(results)
        benar = sum(1 for r in results if r["ast_result"]["is_correct"])
        sebagian = sum(1 for r in results if not r["ast_result"]["is_correct"] and r["ast_result"]["score"] >= 50)
        salah = total - benar - sebagian
        avg_score = sum(r["ast_result"]["score"] for r in results) / total if total else 0
        avg_conf = sum(r["ast_result"]["confidence"] for r in results) / total if total else 0

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Soal", total)
        col2.metric("Benar", f"{benar} ({benar/total*100:.0f}%)")
        col3.metric("Rata-rata Score", f"{avg_score:.1f}")
        col4.metric("Rata-rata Confidence", f"{avg_conf:.0%}")

        fig = go.Figure()
        fig.add_trace(go.Bar(
            name="Benar", x=["Hasil"], y=[benar],
            marker_color="#4CAF50", text=f"{benar} ({benar/total*100:.0f}%)",
        ))
        fig.add_trace(go.Bar(
            name="Sebagian", x=["Hasil"], y=[sebagian],
            marker_color="#FF9800", text=f"{sebagian} ({sebagian/total*100:.0f}%)",
        ))
        fig.add_trace(go.Bar(
            name="Salah", x=["Hasil"], y=[salah],
            marker_color="#f44336", text=f"{salah} ({salah/total*100:.0f}%)",
        ))
        fig.update_layout(title="Distribusi Hasil Evaluasi", barmode="stack", height=250)
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("📋 Detail Per Soal")
        for i, r in enumerate(results):
            ast_r = r["ast_result"]
            icon = "✅" if ast_r["is_correct"] else "⚠️" if ast_r["score"] >= 50 else "❌"
            with st.container(border=True):
                cols = st.columns([3, 1, 1, 2])
                cols[0].markdown(f"{icon} **{r['question'][:80]}...**" if len(r['question']) > 80 else f"{icon} **{r['question']}**")
                cols[1].markdown(f"Score: **{ast_r['score']}**")
                cols[2].markdown(f"Conf: {ast_r['confidence']:.0%}")
                cols[3].markdown(f"BKT: {r.get('mastery_after', 0)*100:.0f}%")

                with st.expander("Lihat detail"):
                    st.markdown(f"**Jawaban kamu:** _{r['student_answer']}_")
                    st.markdown(f"**Jawaban benar:** _{r['correct_answer']}_")
                    st.markdown(f"**Feedback AST:** {ast_r.get('feedback', '-')}")
                    if r.get("feedback"):
                        st.markdown(f"**AI Feedback:** {r['feedback']}")
                    if r.get("mastery_after"):
                        st.caption(f"📊 BKT Mastery setelah soal ini: {r['mastery_after']*100:.1f}%")

        st.divider()

        mastery_progress = [0.2]
        for r in results:
            m = bkt.update_mastery(mastery_progress[-1], r["ast_result"]["is_correct"])
            mastery_progress.append(m)

        colors = ["#6366f1"]
        for r in results:
            colors.append("#4CAF50" if r["ast_result"]["is_correct"] else "#f44336")

        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(
            x=list(range(len(mastery_progress))),
            y=[m * 100 for m in mastery_progress],
            mode="lines+markers",
            marker=dict(size=10, color=colors),
            line=dict(width=2, color="#6366f1"),
        ))
        fig3.add_hline(y=80, line_dash="dash", line_color="#4CAF50", annotation_text="Mastery Target")
        fig3.update_layout(title="BKT Mastery Progression", xaxis_title="Soal ke-", yaxis_title="Mastery %", height=280)
        st.plotly_chart(fig3, use_container_width=True)
