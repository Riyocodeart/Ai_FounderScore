import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.navbar import show_navbar



show_navbar()

st.title("Competitor Analysis")

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



st.set_page_config(page_title="FounderScore — Competitors", layout="wide", initial_sidebar_state="collapsed")






st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;1,400&family=DM+Mono:wght@300;400;500&family=Outfit:wght@300;400;500&display=swap');
header{visibility:hidden}footer{visibility:hidden}
section[data-testid="stSidebar"]{display:none!important}
[data-testid="stAppViewContainer"]{background:#080c08}
.block-container{padding:1.8rem 2.5rem 4rem!important;max-width:1100px}
.fs-header{display:flex;align-items:center;justify-content:space-between;padding-bottom:1.2rem;border-bottom:1px solid rgba(100,160,210,.15);margin-bottom:1.8rem}
.fs-logo{font-family:'Cormorant Garamond',serif;font-size:1.65rem;font-weight:400;color:#a8ccdc}
.fs-logo em{font-style:italic;color:#7ab4d0}
.fs-badge{font-family:'DM Mono',monospace;font-size:.6rem;letter-spacing:.2em;color:#4a7a9a;border:1px solid rgba(100,160,210,.2);border-radius:999px;padding:.32rem .9rem;text-transform:uppercase}
.stTextArea label,.stNumberInput label,.stSelectbox label{font-family:'DM Mono',monospace!important;font-size:.62rem!important;letter-spacing:.2em!important;text-transform:uppercase!important;color:#4a7a9a!important}
.stTextArea textarea{background:rgba(100,160,210,.05)!important;border:1px solid rgba(100,160,210,.2)!important;border-radius:10px!important;color:#a8ccdc!important;font-family:'Outfit',sans-serif!important;font-size:.93rem!important}
.stTextArea textarea::placeholder{color:rgba(100,160,210,.22)!important}
div.action-btn .stButton>button{font-family:'DM Mono',monospace!important;font-size:.73rem!important;font-weight:500!important;letter-spacing:.22em!important;text-transform:uppercase!important;color:#080c08!important;background:#7ab4d0!important;border:none!important;border-radius:10px!important;padding:.85rem 2.2rem!important}
div.action-btn .stButton>button:hover{background:#a8ccdc!important;transform:translateY(-2px)!important;box-shadow:0 8px 24px rgba(100,160,210,.25)!important}
[data-testid="stAppViewContainer"] h1,[data-testid="stAppViewContainer"] h2,[data-testid="stAppViewContainer"] h3{color:#a8ccdc!important;font-family:'Cormorant Garamond',serif!important;font-weight:300!important}
[data-testid="stMetric"]{background:rgba(100,160,210,.06)!important;border:1px solid rgba(100,160,210,.15)!important;border-radius:14px!important;padding:1.2rem 1.4rem!important}
[data-testid="stMetricLabel"] p{color:#4a7a9a!important;font-family:'DM Mono',monospace!important;font-size:.6rem!important;letter-spacing:.18em!important;text-transform:uppercase!important}
[data-testid="stMetricValue"]{color:#a8ccdc!important;font-family:'Cormorant Garamond',serif!important;font-size:2.8rem!important}
.stSuccess{background:rgba(90,170,100,.1)!important;border:1px solid rgba(90,170,100,.28)!important;color:#7ac488!important;border-radius:10px!important}
hr{border-color:rgba(100,160,210,.1)!important}
[data-testid="stDataFrame"]{border:1px solid rgba(100,160,210,.15)!important;border-radius:12px!important}

/* ── NAV TAB BAR ── */
.nav-wrap{display:flex;align-items:center;gap:0;background:rgba(8,12,8,.97);border:1px solid rgba(143,173,106,.12);border-radius:12px;padding:.45rem .55rem;margin-bottom:1.8rem;backdrop-filter:blur(14px)}
.nav-logo{font-family:'Cormorant Garamond',serif;font-size:1.1rem;font-weight:400;color:#b8d090;padding:.1rem .7rem .1rem .4rem;margin-right:.3rem;border-right:1px solid rgba(143,173,106,.12);white-space:nowrap}
.nav-logo em{font-style:italic;color:#8fad6a}
.nav-tabs{display:flex;gap:.25rem;align-items:center;flex:1}
.nav-tab{font-family:'DM Mono',monospace;font-size:.58rem;letter-spacing:.14em;text-transform:uppercase;padding:.4rem 1rem;border-radius:8px;border:1px solid transparent;background:transparent;color:rgba(143,173,106,.35);cursor:pointer;transition:all .18s;white-space:nowrap;text-decoration:none;display:inline-block}
.nav-tab:hover{background:rgba(143,173,106,.08);color:rgba(143,173,106,.72);border-color:rgba(143,173,106,.16)}
.nav-tab.active{background:rgba(100,160,210,.14);color:#a8ccdc;border-color:rgba(100,160,210,.3)}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="fs-header">
  <div class="fs-logo">Founder<em>Score</em> AI</div>
  <div class="fs-badge">02 · Competitor Intelligence</div>
</div>
""", unsafe_allow_html=True)

# ── NAV TAB BAR ───────────────────────────────────────────────
st.markdown("""
<div class="nav-wrap">
  <div class="nav-logo">Founder<em>Score</em></div>
  <div class="nav-tabs">
    <a class="nav-tab" href="/" target="_parent">🏠 Home</a>
    <a class="nav-tab" href="/1_analysis" target="_parent">📊 Analysis</a>
    <a class="nav-tab active" href="#">🔭 Competitors</a>
    <a class="nav-tab" href="/3_riskModel" target="_parent">⚠️ Risk Model</a>
  </div>
</div>
""", unsafe_allow_html=True)

col_nav = st.columns(4)
with col_nav[0]:
    if st.button("🏠 Home", key="nav_home"):
        st.switch_page("app.py")
with col_nav[1]:
    if st.button("📊 Analysis", key="nav_analysis"):
        st.switch_page("pages/1_analysis.py")
with col_nav[2]:
    pass  # current page
with col_nav[3]:
    if st.button("⚠️ Risk Model", key="nav_risk"):
        st.switch_page("pages/3_riskModel.py")

st.markdown("""
<style>
div[data-testid="stHorizontalBlock"]:has(button[kind="secondary"]) {
    position:absolute;opacity:0;pointer-events:none;height:0;overflow:hidden;
}
</style>
""", unsafe_allow_html=True)

st.markdown("---")

# ════════════════════════════════════════════════════════════
#  COMPETITOR INTELLIGENCE — add your logic here
# ════════════════════════════════════════════════════════════
st.title("🔭 Competitor Intelligence")
st.subheader("Map your competitive landscape")

idea_input = st.text_area("Describe your startup idea:", placeholder="e.g. An AI-powered invoicing platform for freelancers…")
industry = st.selectbox("Industry", ["Technology","FinTech","HealthTech","EdTech","Food & Beverage","E-commerce","Other"])

st.markdown('<div class="action-btn">', unsafe_allow_html=True)
analyze = st.button("🔍  Analyze Competitors")
st.markdown('</div>', unsafe_allow_html=True)

if analyze:
    if idea_input.strip() == "":
        st.warning("Please enter a startup idea.")
    else:
        with st.spinner("Mapping competitive landscape..."):
            import time; time.sleep(1)
        st.success("Competitor Analysis Complete")
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("Competitors Found", "12")
        with col2: st.metric("Market Gaps", "4")
        with col3: st.metric("Saturation Level", "Medium")
        st.header("📋 Competitor Overview")
        st.info("💡 Connect your competitor analysis logic here — replace this placeholder with your `utils/` module.")
        import pandas as pd
        sample = pd.DataFrame({
            "Company": ["CompA","CompB","CompC","CompD"],
            "Stage": ["Series B","Seed","Series A","Bootstrapped"],
            "Market Share": ["28%","15%","22%","8%"],
            "Key Strength": ["Distribution","Tech","Pricing","Niche"],
        })
        st.dataframe(sample, use_container_width=True)