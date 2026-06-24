import streamlit as st
import plotly.graph_objects as go
import networkx as nx

st.set_page_config(page_title="Knowledge Map — MetaLearn Demo", page_icon="🧠", layout="wide")

if not st.session_state.get("token") and not st.session_state.get("guest"):
    st.switch_page("demo_app.py")

st.title("🧠 Knowledge Map")
st.caption("Visualize how topics connect — dependencies, prerequisites, and mastery levels")

G = nx.DiGraph()
nodes = [
    ("Numbers", 0, 3, 0.9),
    ("Fractions", 1, 3, 0.85),
    ("Decimals", 1, 2, 0.75),
    ("Algebra Basics", 2, 3, 0.7),
    ("Linear Equations", 3, 3, 0.65),
    ("Functions", 3, 2, 0.55),
    ("Graphing", 4, 3, 0.5),
    ("Geometry Intro", 2, 1, 0.8),
    ("Angles & Lines", 3, 1, 0.6),
    ("Triangles", 4, 1, 0.45),
    ("Circles", 4, 2, 0.4),
    ("Statistics Intro", 2, 5, 0.75),
    ("Probability", 3, 5, 0.5),
    ("Distributions", 4, 5, 0.3),
    ("Calculus Intro", 4, 4, 0.25),
    ("Limits", 5, 4, 0.2),
    ("Derivatives", 5, 4, 0.15),
    ("Integrals", 6, 4, 0.1),
]
for name, x, y, mastery in nodes:
    G.add_node(name, x=x, y=y, mastery=mastery)

edges = [
    ("Numbers", "Fractions"),
    ("Numbers", "Decimals"),
    ("Fractions", "Algebra Basics"),
    ("Decimals", "Algebra Basics"),
    ("Algebra Basics", "Linear Equations"),
    ("Algebra Basics", "Functions"),
    ("Linear Equations", "Graphing"),
    ("Functions", "Graphing"),
    ("Numbers", "Geometry Intro"),
    ("Geometry Intro", "Angles & Lines"),
    ("Angles & Lines", "Triangles"),
    ("Angles & Lines", "Circles"),
    ("Numbers", "Statistics Intro"),
    ("Statistics Intro", "Probability"),
    ("Probability", "Distributions"),
    ("Algebra Basics", "Calculus Intro"),
    ("Calculus Intro", "Limits"),
    ("Limits", "Derivatives"),
    ("Derivatives", "Integrals"),
]
G.add_edges_from(edges)

pos = {n: (d["x"], -d["y"]) for n, d in G.nodes(data=True)}
edge_trace = go.Scatter(
    x=[], y=[], mode="lines", line=dict(width=1.5, color="#888"), hoverinfo="none"
)
for u, v in G.edges():
    x0, y0 = pos[u]
    x1, y1 = pos[v]
    edge_trace["x"] += (x0, x1, None)
    edge_trace["y"] += (y0, y1, None)

node_x = [pos[n][0] for n in G.nodes()]
node_y = [pos[n][1] for n in G.nodes()]
mastery_vals = [G.nodes[n]["mastery"] for n in G.nodes()]
node_colors = [f"rgba(76, 175, 80, {m + 0.2})" if m >= 0.6 else f"rgba(255, 152, 0, {m + 0.2})" if m >= 0.3 else f"rgba(244, 67, 54, {m + 0.2})" for m in mastery_vals]
node_sizes = [15 + m * 25 for m in mastery_vals]

node_trace = go.Scatter(
    x=node_x, y=node_y, mode="markers+text", text=[n for n in G.nodes()],
    textposition="top center", textfont=dict(size=10),
    marker=dict(size=node_sizes, color=node_colors, line=dict(width=2, color="#333")),
    hovertemplate="<b>%{text}</b><br>Mastery: %{customdata:.0%}<extra></extra>",
    customdata=mastery_vals,
)

fig = go.Figure(data=[edge_trace, node_trace])
fig.update_layout(
    title="Topic Dependency Graph (node color = mastery level)",
    showlegend=False, hovermode="closest",
    xaxis=dict(showgrid=False, zeroline=False, visible=False),
    yaxis=dict(showgrid=False, zeroline=False, visible=False),
    height=600, margin=dict(l=20, r=20, t=40, b=20),
    plot_bgcolor="rgba(0,0,0,0)",
)
st.plotly_chart(fig, use_container_width=True)

st.divider()
st.subheader("📋 Topic Details")
cols = st.columns(3)
topic_info = [
    ("🟢 Mastered (≥80%)", ["Numbers", "Fractions", "Geometry Intro", "Statistics Intro"], "#4CAF50"),
    ("🟡 In Progress (50-79%)", ["Decimals", "Algebra Basics", "Linear Equations", "Functions", "Probability", "Angles & Lines"], "#FF9800"),
    ("🔴 Needs Attention (<50%)", ["Graphing", "Triangles", "Circles", "Distributions", "Calculus Intro", "Limits", "Derivatives", "Integrals"], "#f44336"),
]
for i, (label, topics, color) in enumerate(topic_info):
    with cols[i]:
        st.markdown(f"**{label}**")
        for t in topics:
            st.markdown(f"<span style='color:{color};'>●</span> {t}", unsafe_allow_html=True)

st.divider()
st.subheader("🔍 Recommended Next Topics")
recs = [
    ("Graphing", "Complete Linear Equations first", "prerequisite"),
    ("Distributions", "Master Probability before starting", "prerequisite"),
    ("Derivatives", "You're ready — limits mastered", "ready"),
]
for topic, reason, kind in recs:
    with st.container(border=True):
        icon = "✅" if kind == "ready" else "🔗"
        st.markdown(f"**{icon} {topic}** — {reason}")
