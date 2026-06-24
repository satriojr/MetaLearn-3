import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Gamification — MetaLearn Demo", page_icon="🏆", layout="wide")

if not st.session_state.get("token") and not st.session_state.get("guest"):
    st.switch_page("demo_app.py")

SAMPLE_LEADERBOARD = [
    {"rank": 1, "name": "Alex Rivera", "xp": 12500, "level": 24, "badges": 12, "avatar": "🏆"},
    {"rank": 2, "name": "Sarah Chen", "xp": 11200, "level": 22, "badges": 10, "avatar": "🥇"},
    {"rank": 3, "name": "Marcus Johnson", "xp": 9800, "level": 20, "badges": 9, "avatar": "🥈"},
    {"rank": 4, "name": "Emily Davis", "xp": 8700, "level": 18, "badges": 8, "avatar": "🥉"},
    {"rank": 5, "name": "James Wilson", "xp": 7200, "level": 16, "badges": 7, "avatar": "⭐"},
    {"rank": 6, "name": "Lisa Park", "xp": 6500, "level": 15, "badges": 6, "avatar": "🌟"},
    {"rank": 7, "name": "David Kim", "xp": 5400, "level": 13, "badges": 5, "avatar": "💫"},
    {"rank": 8, "name": "Anna Schmidt", "xp": 4300, "level": 11, "badges": 4, "avatar": "✨"},
]

SAMPLE_BADGES = [
    {"name": "Quick Learner", "icon": "⚡", "desc": "Complete 5 missions in a day", "rarity": "Common"},
    {"name": "Math Whiz", "icon": "🧮", "desc": "Perfect score on Algebra assessment", "rarity": "Rare"},
    {"name": "Streak Master", "icon": "🔥", "desc": "7-day learning streak", "rarity": "Epic"},
    {"name": "Explorer", "icon": "🗺️", "desc": "Try all learning pathways", "rarity": "Common"},
    {"name": "Problem Solver", "icon": "💡", "desc": "Solve 50 challenges", "rarity": "Rare"},
    {"name": "Speed Demon", "icon": "⚡", "desc": "Complete a mission in under 2 min", "rarity": "Epic"},
    {"name": "Helping Hand", "icon": "🤝", "desc": "Help 10 classmates", "rarity": "Rare"},
    {"name": "Top Performer", "icon": "👑", "desc": "Rank #1 on leaderboard", "rarity": "Legendary"},
]

st.title("🏆 Gamification & Rewards")
st.caption("Level up, earn badges, and compete on the leaderboard")

col1, col2, col3, col4 = st.columns(4)
col1.metric("🏅 Total XP Earned", "74,600", "+2,100 today")
col2.metric("⬆️ Avg Level", "17.4", "+0.5 WoW")
col3.metric("🎖️ Badges Awarded", "612", "+18 today")
col4.metric("🔥 Active Streaks", "143 users", "7+ day streaks")

st.divider()
tab_leaderboard, tab_badges, tab_levels = st.tabs(["📊 Leaderboard", "🎖️ Badges", "📈 Level Progression"])

with tab_leaderboard:
    st.subheader("🏅 Top Learners This Week")
    for entry in SAMPLE_LEADERBOARD:
        with st.container(border=True):
            cols = st.columns([0.5, 0.5, 3, 1.5, 1.5, 1.5, 2])
            cols[0].markdown(f"**#{entry['rank']}**")
            cols[1].markdown(entry["avatar"])
            cols[2].markdown(f"**{entry['name']}**")
            cols[3].markdown(f"⭐ Lv.{entry['level']}")
            cols[4].markdown(f"📈 {entry['xp']:,} XP")
            cols[5].markdown(f"🎖️ {entry['badges']}")
            pct = entry["xp"] / 12500 * 100
            cols[6].progress(pct / 100, text=f"{pct:.0f}%")

    fig = go.Figure(go.Bar(
        x=[e["name"] for e in SAMPLE_LEADERBOARD],
        y=[e["xp"] for e in SAMPLE_LEADERBOARD],
        marker_color=["#FFD700" if e["rank"] == 1 else "#C0C0C0" if e["rank"] == 2 else "#CD7F32" if e["rank"] == 3 else "#90CAF9" for e in SAMPLE_LEADERBOARD],
        text=[f"{e['xp']:,}" for e in SAMPLE_LEADERBOARD],
    ))
    fig.update_layout(title="XP Distribution", xaxis_title="", yaxis_title="XP", height=400)
    st.plotly_chart(fig, use_container_width=True)

with tab_badges:
    st.subheader("🎖️ Available Badges")
    rarity_colors = {"Common": "#90CAF9", "Rare": "#CE93D8", "Epic": "#FFB74D", "Legendary": "#EF5350"}
    rcols = st.columns(4)
    for i, badge in enumerate(SAMPLE_BADGES):
        with rcols[i % 4]:
            with st.container(border=True):
                st.markdown(f"<div style='text-align:center;font-size:3rem;'>{badge['icon']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='text-align:center;font-weight:600;'>{badge['name']}</div>", unsafe_allow_html=True)
                st.caption(badge["desc"])
                st.markdown(f"<div style='text-align:center;'><span style='background:{rarity_colors[badge['rarity']]};padding:2px 10px;border-radius:8px;color:white;font-size:0.75rem;'>{badge['rarity']}</span></div>", unsafe_allow_html=True)

with tab_levels:
    st.subheader("📈 XP Required Per Level")
    levels = list(range(1, 26))
    xp_needed = [100 * lv * (1 + lv * 0.1) for lv in levels]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=levels, y=xp_needed, mode="lines+markers", fill="tozeroy", line=dict(width=3, color="#FF9800"), name="XP to next level"))
    fig.update_layout(title="Level Progression Curve", xaxis_title="Level", yaxis_title="XP Required", height=350, hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🏃 My Progress Simulation")
    cols = st.columns([2, 1])
    with cols[0]:
        current_xp = st.slider("Your current XP", 0, 20000, 4500, step=100)
    with cols[1]:
        current_lv = 1
        cumulative = 0
        for lv in range(1, 100):
            cumulative += 100 * lv * (1 + lv * 0.1)
            if cumulative > current_xp:
                current_lv = lv
                break
        next_xp = 100 * current_lv * (1 + current_lv * 0.1)
        progress_in_level = current_xp - (cumulative - next_xp)
        st.metric("Your Level", f"⭐ {current_lv}")
        st.progress(min(progress_in_level / next_xp, 1.0), text=f"{current_xp:,} XP ({(progress_in_level/next_xp*100):.0f}% to Lv.{current_lv+1})")
