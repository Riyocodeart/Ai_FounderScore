import streamlit as st
import sys, os
import streamlit as st
from utils.navbar import show_navbar



show_navbar()

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

st.title("Risk Model")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))



st.set_page_config(page_title="FounderScore — Risk Model", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;1,400&family=DM+Mono:wght@300;400;500&family=Outfit:wght@300;400;500&display=swap');
header{visibility:hidden}footer{visibility:hidden}
section[data-testid="stSidebar"]{display:none!important}
[data-testid="stAppViewContainer"]{background:#080c08}
.block-container{padding:1.8rem 2.5rem 4rem!important;max-width:1100px}
.fs-header{display:flex;align-items:center;justify-content:space-between;padding-bottom:1.2rem;border-bottom:1px solid rgba(200,100,80,.15);margin-bottom:1.8rem}
.fs-logo{font-family:'Cormorant Garamond',serif;font-size:1.65rem;font-weight:400;color:#dcb0a8}
.fs-logo em{font-style:italic;color:#d08070}
.fs-badge{font-family:'DM Mono',monospace;font-size:.6rem;letter-spacing:.2em;color:#9a5040;border:1px solid rgba(200,100,80,.2);border-radius:999px;padding:.32rem .9rem;text-transform:uppercase}
.stTextArea label,.stNumberInput label{font-family:'DM Mono',monospace!important;font-size:.62rem!important;letter-spacing:.2em!important;text-transform:uppercase!important;color:#9a5040!important}
.stTextArea textarea{background:rgba(200,100,80,.04)!important;border:1px solid rgba(200,100,80,.18)!important;border-radius:10px!important;color:#dcb0a8!important;font-family:'Outfit',sans-serif!important;font-size:.93rem!important}
.stTextArea textarea::placeholder{color:rgba(200,100,80,.22)!important}
div.action-btn .stButton>button{font-family:'DM Mono',monospace!important;font-size:.73rem!important;font-weight:500!important;letter-spacing:.22em!important;text-transform:uppercase!important;color:#fff!important;background:#a04030!important;border:none!important;border-radius:10px!important;padding:.85rem 2.2rem!important}
div.action-btn .stButton>button:hover{background:#c05040!important;transform:translateY(-2px)!important;box-shadow:0 8px 24px rgba(200,100,80,.3)!important}
[data-testid="stAppViewContainer"] h1,[data-testid="stAppViewContainer"] h2,[data-testid="stAppViewContainer"] h3{color:#dcb0a8!important;font-family:'Cormorant Garamond',serif!important;font-weight:300!important}
[data-testid="stMetric"]{background:rgba(200,100,80,.06)!important;border:1px solid rgba(200,100,80,.15)!important;border-radius:14px!important;padding:1.2rem 1.4rem!important}
[data-testid="stMetricLabel"] p{color:#9a5040!important;font-family:'DM Mono',monospace!important;font-size:.6rem!important;letter-spacing:.18em!important;text-transform:uppercase!important}
[data-testid="stMetricValue"]{color:#dcb0a8!important;font-family:'Cormorant Garamond',serif!important;font-size:2.8rem!important}
.stSuccess{background:rgba(90,170,100,.1)!important;border:1px solid rgba(90,170,100,.28)!important;color:#7ac488!important;border-radius:10px!important}
.stError{background:rgba(200,80,60,.1)!important;border:1px solid rgba(200,80,60,.3)!important;color:#e08070!important;border-radius:10px!important}
hr{border-color:rgba(200,100,80,.1)!important}

/* ── NAV TAB BAR ── */
.nav-wrap{display:flex;align-items:center;gap:0;background:rgba(8,12,8,.97);border:1px solid rgba(143,173,106,.12);border-radius:12px;padding:.45rem .55rem;margin-bottom:1.8rem;backdrop-filter:blur(14px)}
.nav-logo{font-family:'Cormorant Garamond',serif;font-size:1.1rem;font-weight:400;color:#b8d090;padding:.1rem .7rem .1rem .4rem;margin-right:.3rem;border-right:1px solid rgba(143,173,106,.12);white-space:nowrap}
.nav-logo em{font-style:italic;color:#8fad6a}
.nav-tabs{display:flex;gap:.25rem;align-items:center;flex:1}
.nav-tab{font-family:'DM Mono',monospace;font-size:.58rem;letter-spacing:.14em;text-transform:uppercase;padding:.4rem 1rem;border-radius:8px;border:1px solid transparent;background:transparent;color:rgba(143,173,106,.35);cursor:pointer;transition:all .18s;white-space:nowrap;text-decoration:none;display:inline-block}
.nav-tab:hover{background:rgba(143,173,106,.08);color:rgba(143,173,106,.72);border-color:rgba(143,173,106,.16)}
.nav-tab.active{background:rgba(200,100,80,.14);color:#dcb0a8;border-color:rgba(200,100,80,.3)}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="fs-header">
  <div class="fs-logo">Founder<em>Score</em> AI</div>
  <div class="fs-badge">03 · Risk Model</div>
</div>
""", unsafe_allow_html=True)

# ── NAV TAB BAR ───────────────────────────────────────────────
st.markdown("""
<div class="nav-wrap">
  <div class="nav-logo">Founder<em>Score</em></div>
  <div class="nav-tabs">
    <a class="nav-tab" href="/" target="_parent">🏠 Home</a>
    <a class="nav-tab" href="/1_analysis" target="_parent">📊 Analysis</a>
    <a class="nav-tab" href="/2_competitors" target="_parent">🔭 Competitors</a>
    <a class="nav-tab active" href="#">⚠️ Risk Model</a>
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
    if st.button("🔭 Competitors", key="nav_comp"):
        st.switch_page("pages/2_competitors.py")
with col_nav[3]:
    pass  # current page

st.markdown("""
<style>
div[data-testid="stHorizontalBlock"]:has(button[kind="secondary"]) {
    position:absolute;opacity:0;pointer-events:none;height:0;overflow:hidden;
}
</style>
""", unsafe_allow_html=True)

st.markdown("---")

# ════════════════════════════════════════════════════════════
#  RISK MODEL — add your logic here
# ════════════════════════════════════════════════════════════
st.title("⚠️ Risk Model")
st.subheader("Evaluate financial runway and execution risks")

idea_input = st.text_area("Describe your startup idea:", placeholder="e.g. A subscription SaaS for SMB accounting automation…")

col1, col2 = st.columns(2)
with col1:
    capital = st.number_input("Capital Available (USD)", value=50000, min_value=0, step=5000)
with col2:
    burn = st.number_input("Monthly Burn Rate (USD)", value=5000, min_value=0, step=500)

st.markdown('<div class="action-btn">', unsafe_allow_html=True)
assess = st.button("⚠️  Assess Risk")
st.markdown('</div>', unsafe_allow_html=True)

if assess:
    if idea_input.strip() == "":
        st.warning("Please enter a startup idea.")
    else:
        with st.spinner("Running risk model..."):
            import time; time.sleep(1)
        runway = int(capital / burn) if burn > 0 else 999
        runway_status = "✅ Healthy" if runway >= 12 else "⚠️ Moderate" if runway >= 6 else "🔴 Critical"
        st.success("Risk Assessment Complete")
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("Runway", f"{runway} months")
        with col2: st.metric("Runway Status", runway_status)
        with col3: st.metric("Risk Score", "Medium")
        st.header("📋 Risk Register")
        st.info("💡 Connect your risk model logic here — replace this placeholder with your `utils/` module.")
        risks = [
            ("🔴 HIGH", "Low runway — less than 6 months" if runway < 6 else "💚 Runway is healthy"),
            ("🟡 MEDIUM", "Market timing risk — validate demand before scaling"),
            ("🟡 MEDIUM", "Team execution risk — ensure core roles are filled"),
            ("🟢 LOW", "Technology risk — well-established stack reduces build risk"),
        ]
        for level, desc in risks:
            st.markdown(f"**{level}** — {desc}")