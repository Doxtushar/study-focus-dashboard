import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Study Focus Dashboard",
    page_icon="",
    layout="wide",
)


ACTIVITY_COLORS = {
    "Study": "#2563eb",
    "Other Work": "#06b6d4",
    "TV": "#f97316",
    "Mobile": "#ef4444",
    "Sleep": "#8b5cf6",
    "Eating": "#14b8a6",
}


def inject_styles():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700;800&family=Space+Grotesk:wght@500;700&display=swap');

        :root {
            --bg-main: #f5f7fb;
            --text-main: #0f172a;
            --text-soft: #64748b;
            --panel: rgba(255, 255, 255, 0.82);
            --border: rgba(148, 163, 184, 0.22);
            --shadow: 0 18px 40px rgba(15, 23, 42, 0.08);
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(37, 99, 235, 0.14), transparent 32%),
                radial-gradient(circle at top right, rgba(14, 165, 233, 0.16), transparent 28%),
                linear-gradient(180deg, #f8fbff 0%, #f4f7fb 48%, #eef3f8 100%);
            color: var(--text-main);
            font-family: 'Manrope', sans-serif;
        }

        header[data-testid="stHeader"] {
            display: none;
        }

        [data-testid="stToolbar"],
        .stAppDeployButton,
        button[kind="header"] {
            display: none !important;
        }

        .block-container {
            padding-top: 0.35rem;
            padding-bottom: 2rem;
        }

        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #081225 0%, #0f1d3a 100%);
            border-right: 1px solid rgba(255, 255, 255, 0.08);
        }

        section[data-testid="stSidebar"] * {
            color: #e2e8f0 !important;
        }

        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] .stMarkdown,
        section[data-testid="stSidebar"] .stTextInput,
        section[data-testid="stSidebar"] .stNumberInput,
        section[data-testid="stSidebar"] .stSlider,
        section[data-testid="stSidebar"] .stCheckbox {
            font-family: 'Manrope', sans-serif;
        }

        section[data-testid="stSidebar"] .material-icons,
        section[data-testid="stSidebar"] .material-symbols-rounded,
        section[data-testid="stSidebar"] [class*="material-symbol"],
        section[data-testid="stSidebar"] button[kind="header"] span,
        section[data-testid="stSidebar"] button[kind="header"] div,
        button[aria-label*="sidebar" i] span,
        button[aria-label*="sidebar" i] div {
            font-family: "Material Symbols Rounded", "Material Symbols Outlined", "Material Icons" !important;
            font-weight: normal !important;
            font-style: normal !important;
        }

        .hero-card {
            position: relative;
            overflow: hidden;
            padding: 2rem 2rem 1.9rem 2rem;
            border-radius: 28px;
            background:
                radial-gradient(circle at 12% 18%, rgba(125, 211, 252, 0.34), transparent 24%),
                radial-gradient(circle at 85% 20%, rgba(147, 197, 253, 0.30), transparent 22%),
                linear-gradient(135deg, #06101f 0%, #12356a 45%, #0f766e 100%);
            color: white;
            box-shadow: 0 28px 65px rgba(15, 23, 42, 0.24);
            margin-bottom: 1rem;
        }

        .hero-title {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 2.45rem;
            font-weight: 700;
            letter-spacing: -0.04em;
            margin-bottom: 0.45rem;
        }

        .hero-subtitle {
            max-width: 780px;
            font-size: 1rem;
            line-height: 1.7;
            color: rgba(255, 255, 255, 0.82);
        }

        .hero-chip-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.7rem;
            margin-top: 1.25rem;
        }

        .hero-chip {
            padding: 0.55rem 0.95rem;
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.16);
            backdrop-filter: blur(8px);
            font-size: 0.88rem;
            color: rgba(255, 255, 255, 0.92);
        }

        .glass-card {
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: 24px;
            box-shadow: var(--shadow);
            backdrop-filter: blur(14px);
            padding: 1.2rem;
        }

        .metric-card {
            min-height: 158px;
            padding: 1.2rem 1.15rem;
            border-radius: 24px;
            color: white;
            box-shadow: 0 18px 42px rgba(15, 23, 42, 0.18);
            position: relative;
            overflow: hidden;
            margin-bottom: 0.8rem;
        }

        .metric-card::after {
            content: "";
            position: absolute;
            inset: auto -45px -45px auto;
            width: 130px;
            height: 130px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.12);
        }

        .metric-label {
            font-size: 0.92rem;
            font-weight: 700;
            opacity: 0.9;
        }

        .metric-value {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 2.1rem;
            font-weight: 700;
            line-height: 1.1;
            margin-top: 0.75rem;
        }

        .metric-sub {
            margin-top: 0.45rem;
            font-size: 0.86rem;
            opacity: 0.82;
            max-width: 90%;
        }

        .section-title {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.25rem;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 0.2rem;
        }

        .section-kicker {
            color: #64748b;
            font-size: 0.95rem;
            margin-bottom: 1rem;
        }

        .insight-pill {
            display: inline-block;
            padding: 0.4rem 0.78rem;
            border-radius: 999px;
            font-size: 0.82rem;
            font-weight: 700;
            margin-bottom: 0.75rem;
        }

        .summary-panel {
            padding: 1rem 1.1rem;
            border-radius: 22px;
            background: linear-gradient(180deg, rgba(255,255,255,0.9), rgba(248,250,252,0.86));
            border: 1px solid rgba(148, 163, 184, 0.2);
            box-shadow: var(--shadow);
        }

        [data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.74);
            border: 1px solid rgba(148, 163, 184, 0.18);
            border-radius: 18px;
            padding: 0.95rem 1rem;
            box-shadow: 0 8px 22px rgba(15, 23, 42, 0.05);
        }

        [data-testid="stMetricLabel"] {
            color: #475569;
            font-weight: 700;
        }

        [data-testid="stMetricValue"] {
            color: #0f172a;
            font-family: 'Space Grotesk', sans-serif;
        }

        div[data-testid="stPlotlyChart"] {
            background: rgba(255, 255, 255, 0.68);
            border: 1px solid rgba(148, 163, 184, 0.18);
            border-radius: 22px;
            padding: 0.45rem;
            box-shadow: var(--shadow);
        }

        .footer-tip {
            /* 🚨 FORCE HIDE SIDEBAR TOGGLE ICON COMPLETELY */
            header [data-testid="collapsedControl"] {
                display: none !important;
            }

            /* Backup (in case above fails) */
            header button {
                display: none !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def metric_card(title: str, value: str, subtitle: str, gradient: str):
    st.markdown(
        f"""
        <div class="metric-card" style="background:{gradient};">
            <div class="metric-label">{title}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-sub">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def focus_score(study, other_work, tv, mobile, sleep, eating):
    score = 0

    if study < 4:
        score += max(0, study * 5)
    elif study <= 6:
        score += 20 + ((study - 4) * 7.5)
    elif study <= 8:
        score += 35
    else:
        score += max(0, 35 - ((study - 8) * 5))

    if other_work <= 2:
        score += 7 + (other_work * 4)
    elif other_work <= 3:
        score += 15
    else:
        score += max(0, 15 - ((other_work - 3) * 6))

    score += max(0, 10 - (max(tv - 1.5, 0) * 5))
    score += max(0, 15 - (max(mobile - 2, 0) * 5))
    score += max(0, 5 - (max(eating - 1.5, 0) * 4))

    if sleep < 6:
        score += max(0, 20 - ((6 - sleep) * 6))
    elif sleep <= 8:
        score += 20
    else:
        score += max(0, 20 - ((sleep - 8) * 4))

    total = study + other_work + tv + mobile + sleep + eating
    if total > 24:
        score -= (total - 24) * 8

    return max(0, min(100, round(score)))


def make_recommendation(study, other_work, tv, mobile, sleep, eating, total):
    suggestions = []
    productive = study + other_work

    if productive >= 8:
        suggestions.append("Your productive hours are strong. Keep this rhythm and protect deep-work time.")
    elif productive >= 5:
        suggestions.append("Your productive time is decent, but adding one more focused study block would lift the day.")
    else:
        suggestions.append("Productive hours are low today. Try to increase study time and reduce distractions.")

    if mobile > 4:
        suggestions.append("Mobile use is high. Keep the phone away during study and turn off non-essential notifications.")
    elif mobile > 2:
        suggestions.append("Mobile time is moderate. A stricter app limit could help you stay sharper.")

    if tv > 2:
        suggestions.append("TV time is a little high. Try moving entertainment to the end of the day.")

    if sleep < 6:
        suggestions.append("Sleep is low. Aim for at least 6 hours to improve memory, focus, and mood.")
    elif sleep > 8:
        suggestions.append("Sleep is slightly high. Keeping it in the 6 to 8 hour range can improve daily balance.")
    else:
        suggestions.append("Sleep is in a healthy range. That supports stronger concentration.")

    if eating > 2:
        suggestions.append("Eating time is stretching out. Try more mindful meals without screens nearby.")

    if total < 24:
        suggestions.append(
            f"You still have {24 - total:.1f} hours free. Use that time for revision, exercise, breaks, or reflection."
        )

    return suggestions


def score_tone(score: int):
    if score >= 80:
        return "Elite Focus", "#dcfce7", "#166534", "You are running a very balanced, high-performance day."
    if score >= 60:
        return "Building Momentum", "#fef3c7", "#92400e", "Your routine is solid, but a few adjustments can improve consistency."
    return "Needs Reset", "#fee2e2", "#b91c1c", "A few habits are pulling your focus down. Tightening your routine will help fast."


inject_styles()

st.markdown(
    """
    <div class="hero-card">
        <div class="hero-title">Study Focus Dashboard</div>
        <div class="hero-subtitle">
            Turn a simple daily routine into a polished performance dashboard with smart focus scoring,
            visual balance tracking, and beautifully structured insights for stronger study discipline.
        </div>
        <div class="hero-chip-row">
            <div class="hero-chip">24-hour planning</div>
            <div class="hero-chip">Focus scoring</div>
            <div class="hero-chip">Distraction tracking</div>
            <div class="hero-chip">Personalized recommendations</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown("## Daily Planner")
st.sidebar.caption("Adjust the hours for each activity and the dashboard updates instantly.")

name = st.sidebar.text_input("Student name", value="Student")
study = st.sidebar.slider("Study time", 0.0, 24.0, 6.0, 0.5)
other_work = st.sidebar.slider("Other work time", 0.0, 24.0, 2.0, 0.5)
tv = st.sidebar.slider("TV time", 0.0, 24.0, 1.0, 0.5)
mobile = st.sidebar.slider("Mobile time", 0.0, 24.0, 2.0, 0.5)
sleep = st.sidebar.slider("Sleep time", 0.0, 24.0, 7.0, 0.5)
eating = st.sidebar.slider("Eating time", 0.0, 24.0, 1.0, 0.5)
usual_eating = st.sidebar.number_input("Usual eating time", min_value=0.0, max_value=6.0, value=1.0, step=0.5)
show_other = st.sidebar.checkbox("Show remaining time", value=True)

current_total = study + other_work + tv + mobile + sleep + eating
remaining = 24 - current_total
score = focus_score(study, other_work, tv, mobile, sleep, eating)
productive_time = study + other_work
distraction_time = tv + mobile
ideal_focus = max(0, min(100, round((productive_time * 8) - (tv * 4) - (mobile * 5) + (sleep * 2))))

df = pd.DataFrame(
    {
        "Activity": ["Study", "Other Work", "TV", "Mobile", "Sleep", "Eating"],
        "Hours": [study, other_work, tv, mobile, sleep, eating],
    }
)
df["Color"] = df["Activity"].map(ACTIVITY_COLORS)

focus_label, pill_bg, pill_fg, focus_message = score_tone(score)

top_1, top_2, top_3, top_4 = st.columns(4)
with top_1:
    metric_card("Focus Score", f"{score}/100", "A weighted score based on study, balance, sleep, and distractions.", "linear-gradient(135deg, #0f172a, #1d4ed8)")
with top_2:
    metric_card("Productive Time", f"{productive_time:.1f} hrs", "Combined study and work hours shaping your core output.", "linear-gradient(135deg, #0f766e, #14b8a6)")
with top_3:
    metric_card("Distraction Time", f"{distraction_time:.1f} hrs", "TV and mobile together show how much focus is leaking away.", "linear-gradient(135deg, #7c2d12, #f97316)")
with top_4:
    metric_card("Sleep Balance", f"{sleep:.1f} hrs", "Recovery time directly affects memory, attention, and energy.", "linear-gradient(135deg, #581c87, #8b5cf6)")

left, right = st.columns([1.2, 0.8], gap="large")

with left:
    st.markdown('<div class="section-title">Daily Activity Design</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="section-kicker">{name}\'s day visualized across the full 24-hour cycle.</div>',
        unsafe_allow_html=True,
    )

    pie = px.pie(
        df,
        names="Activity",
        values="Hours",
        hole=0.62,
        color="Activity",
        color_discrete_map=ACTIVITY_COLORS,
    )
    pie.update_traces(
        textposition="inside",
        textinfo="percent+label",
        marker=dict(line=dict(color="rgba(255,255,255,0.75)", width=2)),
        pull=[0.04 if activity == "Study" else 0 for activity in df["Activity"]],
        hovertemplate="<b>%{label}</b><br>%{value:.1f} hrs<extra></extra>",
    )
    pie.update_layout(
        title="24-Hour Activity Split",
        title_x=0.03,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=60, l=10, r=10, b=10),
        legend_title_text="Activities",
        font=dict(family="Manrope, sans-serif", color="#0f172a"),
        annotations=[
            dict(
                text=f"<b>{score}</b><br>Focus",
                x=0.5,
                y=0.5,
                showarrow=False,
                font=dict(size=22, color="#0f172a", family="Space Grotesk, sans-serif"),
            )
        ],
    )
    st.plotly_chart(pie, width="stretch")

    bar = px.bar(
        df.sort_values("Hours", ascending=False),
        x="Hours",
        y="Activity",
        orientation="h",
        color="Activity",
        color_discrete_map=ACTIVITY_COLORS,
        text="Hours",
    )
    bar.update_traces(
        texttemplate="%{text:.1f} hrs",
        textposition="outside",
        marker=dict(line=dict(color="rgba(15,23,42,0.05)", width=1)),
        hovertemplate="<b>%{y}</b><br>%{x:.1f} hrs<extra></extra>",
    )
    bar.update_layout(
        title="Where Your Time Goes",
        title_x=0.03,
        xaxis_title="Hours",
        yaxis_title="",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=60, l=10, r=30, b=10),
        showlegend=False,
        font=dict(family="Manrope, sans-serif", color="#0f172a"),
    )
    st.plotly_chart(bar, width="stretch")

    trend = go.Figure()
    trend.add_trace(
        go.Scatterpolar(
            r=[study, other_work, tv, mobile, sleep, eating],
            theta=["Study", "Other Work", "TV", "Mobile", "Sleep", "Eating"],
            fill="toself",
            name="Routine Shape",
            line=dict(color="#2563eb", width=3),
            fillcolor="rgba(37, 99, 235, 0.22)",
        )
    )
    trend.update_layout(
        title="Routine Balance Map",
        title_x=0.03,
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Manrope, sans-serif", color="#0f172a"),
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, max(8, max(df["Hours"]) + 2)], gridcolor="rgba(148,163,184,0.25)"),
            angularaxis=dict(gridcolor="rgba(148,163,184,0.15)"),
        ),
        margin=dict(t=60, l=20, r=20, b=20),
        showlegend=False,
    )
    st.plotly_chart(trend, width="stretch")

with right:
    st.markdown('<div class="section-title">Smart Insights</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-kicker">Warnings, rhythm checks, and high-value suggestions.</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="glass-card"><div class="insight-pill" style="background:{pill_bg}; color:{pill_fg};">{focus_label}</div><div style="font-size:1.5rem; font-weight:800; color:#0f172a;">{score}/100</div><div style="color:#475569; margin-top:0.45rem;">{focus_message}</div></div>',
        unsafe_allow_html=True,
    )

    st.markdown("")
    if current_total > 24:
        st.error(f"Your total is {current_total:.1f} hours, which is above 24 hours. Reduce some activities to make the plan realistic.")
    elif current_total == 24:
        st.success("Perfect 24-hour allocation. Your day is fully planned.")
    else:
        st.info(f"You have planned {current_total:.1f} hours so far.")

    if study < 4:
        st.error("Study time is too low. Try to reach at least 4 hours.")
    elif study <= 6:
        st.warning("Study time is moderate. One extra focused session would improve your day.")
    elif study <= 8:
        st.success("Study time is strong and sustainable.")
    else:
        st.info("Study time is high. Add breaks to avoid burnout.")

    if mobile > 4:
        st.warning("Mobile time is high. Reducing it will immediately improve your focus score.")

    if tv > 3:
        st.warning("TV time is high. Keep entertainment tighter on heavy study days.")

    if eating > usual_eating:
        st.info("Eating time is above your usual pattern. More mindful, screen-free meals may help.")

    if other_work > 4:
        st.warning("Other work is taking a lot of space. Try protecting your study blocks first.")
    elif other_work >= 2:
        st.success("Other work looks fairly balanced with study.")

    st.progress(score / 100)
    st.caption("Focus progress")

    recommendations = make_recommendation(study, other_work, tv, mobile, sleep, eating, current_total)
    st.markdown("### Personalized Suggestions")
    for message in recommendations:
        st.markdown(f"- {message}")

    if show_other and remaining > 0:
        st.markdown("### Remaining Time")
        st.info(
            f"You still have {remaining:.1f} hours available. Use them for exercise, revision, prayer, meditation, creative hobbies, or rest."
        )

st.markdown("")
st.markdown('<div class="section-title">Dashboard Summary</div>', unsafe_allow_html=True)
st.markdown('<div class="section-kicker">Quick ratios that show how balanced the full day really is.</div>', unsafe_allow_html=True)

summary1, summary2, summary3 = st.columns(3)
with summary1:
    st.markdown('<div class="summary-panel">', unsafe_allow_html=True)
    st.metric("Study Ratio", f"{(study / 24) * 100:.1f}%")
    st.metric("Other Work Ratio", f"{(other_work / 24) * 100:.1f}%")
    st.metric("Distraction Ratio", f"{(distraction_time / 24) * 100:.1f}%")
    st.markdown("</div>", unsafe_allow_html=True)

with summary2:
    st.markdown('<div class="summary-panel">', unsafe_allow_html=True)
    st.metric("Sleep Ratio", f"{(sleep / 24) * 100:.1f}%")
    st.metric("Eating Ratio", f"{(eating / 24) * 100:.1f}%")
    st.metric("Planned Hours", f"{current_total:.1f} hrs")
    st.markdown("</div>", unsafe_allow_html=True)

with summary3:
    st.markdown('<div class="summary-panel">', unsafe_allow_html=True)
    st.metric("Simple Focus Index", f"{ideal_focus}")
    st.metric("Free Time", f"{max(0, remaining):.1f} hrs")
    st.metric("Deep Work Potential", f"{max(0, study - mobile / 2):.1f} hrs")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="footer-tip">
        <strong>Performance tip:</strong> The most attractive routine is not the busiest one. Aim for strong study blocks,
        controlled distraction time, healthy sleep, and enough open space in the day to stay consistent.
    </div>
    """,
    unsafe_allow_html=True,
)
