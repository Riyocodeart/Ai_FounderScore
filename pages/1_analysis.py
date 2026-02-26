import streamlit as st
import sys, os, base64
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils.nlp_engine import extract_startup_info
from utils.scoring import calculate_scores, generate_risk_analysis, simulate_survival, get_competitor_insights
from utils.shared import navbar

st.set_page_config(
    page_title="VentureLens AI",
    page_icon="🔮",
    layout="centered",
    initial_sidebar_state="collapsed",
)

navbar("home", "")

# ── Load background (jpeg if available, else pure black) ──────────
BG_PATH = os.path.join(os.path.dirname(__file__), "assets", "bg.jpeg")

def get_bg_css():
    if os.path.exists(BG_PATH):
        with open(BG_PATH, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        return f"""
        background-image: url("data:image/jpeg;base64,{b64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        """
    else:
        # Temporary: rich black with purple radial glow
        return """
        background: radial-gradient(ellipse at 30% 20%, #1a0533 0%, #0a0012 40%, #000000 100%);
        """

BG_CSS = get_bg_css()

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

html, body, .stApp, [class*="css"] {{
    font-family: 'Syne', sans-serif !important;
    color: #ffffff !important;
}}

.stApp {{
    {BG_CSS}
    min-height: 100vh;
}}

/* Dark overlay so text stays readable over any image */
.stApp::before {{
    content: '';
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.72);
    z-index: 0;
    pointer-events: none;
}}

section[data-testid="stSidebar"] {{ display: none !important; }}
header[data-testid="stHeader"]   {{ display: none !important; }}
footer {{ display: none !important; }}

.block-container {{
    padding: 60px 20px 80px !important;
    max-width: 760px !important;
    position: relative;
    z-index: 1;
}}

/* ── Glowing text util ── */
.glow-white {{
    color: #ffffff;
    text-shadow:
        0 0 10px rgba(255,255,255,0.9),
        0 0 30px rgba(200,180,255,0.6),
        0 0 60px rgba(160,120,255,0.4);
}}
.glow-purple {{
    color: #d8b4fe;
    text-shadow:
        0 0 8px rgba(216,180,254,0.9),
        0 0 24px rgba(168,85,247,0.7),
        0 0 50px rgba(124,58,237,0.5);
}}

/* ── Badge ── */
.live-badge {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(124,58,237,0.18);
    border: 1.5px solid rgba(168,85,247,0.45);
    border-radius: 100px;
    padding: 7px 20px;
    font-size: 13px;
    font-weight: 600;
    color: #c4b5fd;
    letter-spacing: 0.10em;
    text-transform: uppercase;
    margin-bottom: 36px;
    backdrop-filter: blur(8px);
}}
.live-dot {{
    width: 9px; height: 9px;
    background: #a855f7;
    border-radius: 50%;
    animation: blink 1.8s ease-in-out infinite;
    box-shadow: 0 0 8px #a855f7, 0 0 16px #7c3aed;
}}
@keyframes blink {{ 0%,100%{{opacity:1}} 50%{{opacity:0.3}} }}

/* ── Hero headline ── */
.hero-h1 {{
    font-size: clamp(44px, 7vw, 80px);
    font-weight: 800;
    line-height: 1.0;
    letter-spacing: -0.03em;
    text-align: center;
    margin-bottom: 20px;
    color: #ffffff;
    text-shadow:
        0 0 20px rgba(255,255,255,0.8),
        0 0 60px rgba(200,160,255,0.5),
        0 0 100px rgba(124,58,237,0.35);
}}
.hero-h1 span {{
    background: linear-gradient(135deg, #c084fc 0%, #a855f7 50%, #7c3aed 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    filter: drop-shadow(0 0 20px rgba(168,85,247,0.7));
}}
.hero-sub {{
    font-size: 22px;
    font-weight: 400;
    color: rgba(255,255,255,0.75);
    text-align: center;
    line-height: 1.55;
    margin-bottom: 52px;
    text-shadow: 0 0 20px rgba(255,255,255,0.3);
}}

/* ── Input card ── */
.input-glass {{
    background: rgba(255,255,255,0.04);
    border: 1.5px solid rgba(168,85,247,0.35);
    border-radius: 24px;
    padding: 36px 32px 28px;
    backdrop-filter: blur(20px);
    box-shadow:
        0 0 0 1px rgba(168,85,247,0.1),
        0 8px 48px rgba(0,0,0,0.6),
        inset 0 1px 0 rgba(255,255,255,0.07);
}}
.input-label {{
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #c4b5fd;
    text-shadow: 0 0 10px rgba(196,181,253,0.6);
    margin-bottom: 10px;
    font-family: 'JetBrains Mono', monospace;
}}

/* ── Streamlit textarea ── */
.stTextArea textarea {{
    font-family: 'Syne', sans-serif !important;
    font-size: 20px !important;
    line-height: 1.6 !important;
    background: rgba(0,0,0,0.45) !important;
    border: 1.5px solid rgba(168,85,247,0.4) !important;
    border-radius: 14px !important;
    color: #ffffff !important;
    caret-color: #a855f7 !important;
    backdrop-filter: blur(10px) !important;
    transition: all 0.25s ease !important;
}}
.stTextArea textarea:focus {{
    border-color: #a855f7 !important;
    box-shadow:
        0 0 0 3px rgba(168,85,247,0.2),
        0 0 20px rgba(168,85,247,0.15) !important;
    background: rgba(0,0,0,0.55) !important;
}}
.stTextArea textarea::placeholder {{
    color: rgba(255,255,255,0.25) !important;
    font-size: 18px !important;
}}
.stTextArea label {{
    display: none !important;
}}

/* ── Analyze button ── */
.stButton > button {{
    width: 100% !important;
    background: linear-gradient(135deg, #5b21b6 0%, #7c3aed 45%, #a855f7 100%) !important;
    color: #ffffff !important;
    border: 1px solid rgba(196,181,253,0.3) !important;
    border-radius: 14px !important;
    padding: 20px 40px !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 22px !important;
    font-weight: 700 !important;
    letter-spacing: 0.04em !important;
    cursor: pointer !important;
    box-shadow:
        0 0 20px rgba(124,58,237,0.5),
        0 4px 32px rgba(124,58,237,0.35),
        inset 0 1px 0 rgba(255,255,255,0.15) !important;
    transition: all 0.2s ease !important;
    text-shadow: 0 0 12px rgba(255,255,255,0.5) !important;
    margin-top: 8px !important;
}}
.stButton > button:hover {{
    transform: translateY(-3px) !important;
    box-shadow:
        0 0 35px rgba(168,85,247,0.65),
        0 8px 40px rgba(124,58,237,0.45),
        inset 0 1px 0 rgba(255,255,255,0.2) !important;
}}

/* ── Feature pills ── */
.pills-row {{
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    justify-content: center;
    margin-top: 40px;
}}
.pill {{
    background: rgba(124,58,237,0.12);
    border: 1px solid rgba(168,85,247,0.3);
    border-radius: 100px;
    padding: 8px 20px;
    font-size: 15px;
    font-weight: 600;
    color: #ddd6fe;
    backdrop-filter: blur(6px);
    text-shadow: 0 0 8px rgba(196,181,253,0.5);
    letter-spacing: 0.02em;
}}

/* ── Spinner ── */
.stSpinner > div {{ color: #a855f7 !important; }}
[data-testid="stSpinner"] p {{
    font-size: 22px !important;
    color: #c4b5fd !important;
    text-shadow: 0 0 12px rgba(196,181,253,0.6) !important;
}}

/* ── Warning ── */
[data-testid="stAlert"] {{
    background: rgba(251,191,36,0.1) !important;
    border: 1px solid rgba(251,191,36,0.35) !important;
    border-radius: 12px !important;
    color: #fcd34d !important;
    font-size: 20px !important;
}}
</style>
""", unsafe_allow_html=True)

# ─── PAGE CONTENT ───────────────────────────────────────────────────
st.markdown('<div style="text-align:center;">', unsafe_allow_html=True)

st.markdown('''
<div style="display:flex;justify-content:center;margin-bottom:36px;">
    <div class="live-badge">
        <div class="live-dot"></div>
        AI-Powered · Investor Grade · v1.0
    </div>
</div>

<div class="hero-h1">
    Turn your idea into<br><span>venture intelligence</span>
</div>

<div class="hero-sub">
    Describe your startup below — get NLP extraction, feasibility scoring,<br>
    risk intelligence & survival projections in seconds.
</div>
''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ─── Glass input card ──────────────────────────────────────────────
st.markdown('<div class="input-glass">', unsafe_allow_html=True)
st.markdown('<div class="input-label">💡 Your Startup Idea</div>', unsafe_allow_html=True)

idea = st.text_area(
    label="idea",
    placeholder="Describe the problem, target market, revenue model, and any early traction…",
    height=180,
    key="idea_input",
    label_visibility="collapsed",
)

clicked = st.button("🔮  Analyze My Startup Idea", use_container_width=True)

st.markdown('''
<div style="text-align:center;margin-top:16px;font-size:15px;color:rgba(255,255,255,0.35);
font-family:'JetBrains Mono',monospace;letter-spacing:0.06em;">
⚡ ANALYSIS COMPLETES IN UNDER 3 SECONDS
</div>
''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # close glass card

# ─── Feature pills ─────────────────────────────────────────────────
st.markdown('''
<div class="pills-row">
    <div class="pill">🧠 NLP Extraction</div>
    <div class="pill">📊 Feasibility Score</div>
    <div class="pill">⚠️ Risk Intelligence</div>
    <div class="pill">📈 Survival Simulation</div>
    <div class="pill">🏢 Competitor Mapping</div>
</div>
''', unsafe_allow_html=True)

# ─── Analysis logic ────────────────────────────────────────────────
if clicked:
    if not idea.strip():
        st.warning("⚠️  Please describe your startup idea before analyzing.")
    else:
        with st.spinner("🧠  Running NLP extraction, scoring & survival simulation…"):
            ext = extract_startup_info(idea)
            scores, total = calculate_scores(ext)
            risks = generate_risk_analysis(ext, scores)
            comps = get_competitor_insights(ext)
            surv  = simulate_survival(total)

        st.session_state.update({
            "idea": idea, "extracted": ext, "scores": scores,
            "total": total, "risks": risks, "comps": comps, "surv": surv,
        })
        st.switch_page("pages/1_Dashboard.py")