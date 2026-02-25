import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.nlp_engine import extract_startup_info
from utils.scoring import calculate_scores

from utils.navbar import show_navbar


show_navbar()

st.title("Startup Analysis")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🏠 Home"):
        st.switch_page("main.py")

with col2:
    if st.button("📊 Analysis"):
        st.switch_page("pages/1_analysis.py")

with col3:
    if st.button("⚠️ Risk"):
        st.switch_page("pages/3_riskModel.py")

st.divider()

st.set_page_config(page_title="FounderScore — Analysis", layout="wide", initial_sidebar_state="collapsed")

# ── Existing page styles (unchanged) ─────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;1,400&family=DM+Mono:wght@300;400;500&family=Outfit:wght@300;400;500&display=swap');
header{visibility:hidden}footer{visibility:hidden}
section[data-testid="stSidebar"]{display:none!important}
[data-testid="stAppViewContainer"]{background:#080c08}
.block-container{padding:1.8rem 2.5rem 4rem!important;max-width:1100px}
.fs-header{display:flex;align-items:center;justify-content:space-between;padding-bottom:1.2rem;border-bottom:1px solid rgba(143,173,106,.12);margin-bottom:1.8rem}
.fs-logo{font-family:'Cormorant Garamond',serif;font-size:1.65rem;font-weight:400;color:#b8d090}
.fs-logo em{font-style:italic;color:#8fad6a}
.fs-badge{font-family:'DM Mono',monospace;font-size:.6rem;letter-spacing:.2em;color:#5a7a40;border:1px solid rgba(143,173,106,.2);border-radius:999px;padding:.32rem .9rem;text-transform:uppercase}
.stTextArea label,.stNumberInput label{font-family:'DM Mono',monospace!important;font-size:.62rem!important;letter-spacing:.2em!important;text-transform:uppercase!important;color:#5a7a40!important}
.stTextArea textarea{background:rgba(143,173,106,.05)!important;border:1px solid rgba(143,173,106,.18)!important;border-radius:10px!important;color:#b8d090!important;font-family:'Outfit',sans-serif!important;font-size:.93rem!important}
.stTextArea textarea:focus{border-color:rgba(143,173,106,.45)!important;box-shadow:0 0 0 3px rgba(143,173,106,.07)!important}
.stTextArea textarea::placeholder{color:rgba(143,173,106,.22)!important}
.stNumberInput input{background:rgba(143,173,106,.05)!important;border:1px solid rgba(143,173,106,.18)!important;border-radius:10px!important;color:#b8d090!important}
div.action-btn .stButton>button{font-family:'DM Mono',monospace!important;font-size:.73rem!important;font-weight:500!important;letter-spacing:.22em!important;text-transform:uppercase!important;color:#080c08!important;background:#8fad6a!important;border:none!important;border-radius:10px!important;padding:.85rem 2.2rem!important;transition:all .2s!important}
div.action-btn .stButton>button:hover{background:#b8d090!important;transform:translateY(-2px)!important;box-shadow:0 8px 24px rgba(143,173,106,.25)!important}
[data-testid="stAppViewContainer"] h1,[data-testid="stAppViewContainer"] h2,[data-testid="stAppViewContainer"] h3{color:#b8d090!important;font-family:'Cormorant Garamond',serif!important;font-weight:300!important}
[data-testid="stMetric"]{background:rgba(143,173,106,.06)!important;border:1px solid rgba(143,173,106,.15)!important;border-radius:14px!important;padding:1.2rem 1.4rem!important}
[data-testid="stMetricLabel"] p{color:#5a7a40!important;font-family:'DM Mono',monospace!important;font-size:.6rem!important;letter-spacing:.18em!important;text-transform:uppercase!important}
[data-testid="stMetricValue"]{color:#b8d090!important;font-family:'Cormorant Garamond',serif!important;font-size:2.8rem!important}
.stSuccess{background:rgba(90,170,100,.1)!important;border:1px solid rgba(90,170,100,.28)!important;color:#7ac488!important;border-radius:10px!important}
.stWarning{background:rgba(180,140,60,.1)!important;border:1px solid rgba(180,140,60,.28)!important;color:#d4a860!important;border-radius:10px!important}
hr{border-color:rgba(143,173,106,.1)!important}

/* ── NAV TAB BAR — scoped, never touches other buttons ── */
.nav-wrap{
    display:flex; align-items:center; gap:0;
    background:rgba(8,12,8,.97);
    border:1px solid rgba(143,173,106,.12);
    border-radius:12px; padding:.45rem .55rem;
    margin-bottom:1.8rem;
    backdrop-filter:blur(14px);
}
.nav-logo{
    font-family:'Cormorant Garamond',serif; font-size:1.1rem;
    font-weight:400; color:#b8d090; padding:.1rem .7rem .1rem .4rem;
    margin-right:.3rem; border-right:1px solid rgba(143,173,106,.12);
    white-space:nowrap;
}
.nav-logo em{font-style:italic;color:#8fad6a}
.nav-tabs{display:flex;gap:.25rem;align-items:center;flex:1}
.nav-tab{
    font-family:'DM Mono',monospace; font-size:.58rem;
    letter-spacing:.14em; text-transform:uppercase;
    padding:.4rem 1rem; border-radius:8px;
    border:1px solid transparent; background:transparent;
    color:rgba(143,173,106,.35); cursor:pointer;
    transition:all .18s; white-space:nowrap;
    text-decoration:none; display:inline-block;
}
.nav-tab:hover{
    background:rgba(143,173,106,.08);
    color:rgba(143,173,106,.72);
    border-color:rgba(143,173,106,.16);
}
.nav-tab.active{
    background:rgba(143,173,106,.14);
    color:#b8d090;
    border-color:rgba(143,173,106,.3);
}
</style>
""", unsafe_allow_html=True)

# ── Page header ───────────────────────────────────────────────
st.markdown("""
<div class="fs-header">
  <div class="fs-logo">Founder<em>Score</em> AI</div>
  <div class="fs-badge">01 · Feasibility Analysis</div>
</div>
""", unsafe_allow_html=True)

# ── NAV TAB BAR — rendered as pure HTML, no st.button conflicts ──
st.markdown("""
<div class="nav-wrap">
  <div class="nav-logo">Founder<em>Score</em></div>
  <div class="nav-tabs">
    <a class="nav-tab" href="/" target="_parent">🏠 Home</a>
    <a class="nav-tab active" href="#">📊 Analysis</a>
    <a class="nav-tab" href="/2_competitors" target="_parent">🔭 Competitors</a>
    <a class="nav-tab" href="/3_riskModel" target="_parent">⚠️ Risk Model</a>
  </div>
</div>
""", unsafe_allow_html=True)

# Streamlit switch_page buttons hidden — triggered by nav clicks via JS bridge
col_nav = st.columns(4)
with col_nav[0]:
    if st.button("🏠 Home", key="nav_home"):
        st.switch_page("app.py")
with col_nav[1]:
    pass  # current page
with col_nav[2]:
    if st.button("🔭 Competitors", key="nav_comp"):
        st.switch_page("pages/2_competitors.py")
with col_nav[3]:
    if st.button("⚠️ Risk Model", key="nav_risk"):
        st.switch_page("pages/3_riskModel.py")

# Hide the fallback st.button nav row visually — the HTML nav above is what users see
st.markdown("""
<style>
/* Hide the invisible switch_page trigger buttons */
div[data-testid="stHorizontalBlock"]:has(button[kind="secondary"]) {
    position:absolute; opacity:0; pointer-events:none; height:0; overflow:hidden;
}
</style>
""", unsafe_allow_html=True)

st.markdown("---")

# ════════════════════════════════════════════════════════════
#  ORIGINAL BACKEND LOGIC — 100% UNCHANGED
# ════════════════════════════════════════════════════════════
st.title("🚀 FounderScore")
st.subheader("AI-Powered Startup Feasibility Engine")

idea_input = st.text_area("Describe your startup idea:")

col1, col2 = st.columns(2)
with col1:
    capital_input = st.number_input("Capital Available (USD)", value=50000, min_value=0, step=5000)
with col2:
    burn_input = st.number_input("Monthly Burn Rate (USD)", value=5000, min_value=0, step=500)

st.markdown('<div class="action-btn">', unsafe_allow_html=True)
analyze = st.button("⚡  Analyze Idea")
st.markdown('</div>', unsafe_allow_html=True)

if analyze:
    if idea_input.strip() == "":
        st.warning("Please enter a startup idea.")
    else:
        with st.spinner("Analyzing..."):
            extracted = extract_startup_info(idea_input)
            scores, total = calculate_scores()

        st.success("Analysis Complete")

        st.header("📌 Extracted Insights")
        st.json(extracted)

        st.header("📊 Feasibility Scores")
        cols = st.columns(len(scores))
        for col, (dim, val) in zip(cols, scores.items()):
            with col:
                st.metric(label=dim, value=f"{val}/20")

        st.markdown("---")
        st.metric("Total Feasibility Score", total)