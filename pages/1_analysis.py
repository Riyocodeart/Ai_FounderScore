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


# ── Load background (jpeg if available, else gradient) ──────────
BG_PATH = os.path.join(os.path.dirname(__file__), "assets", "bg.jpeg    ")

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
        return """
        background: radial-gradient(ellipse at center, #ffffff 0%, #e8d5ff 25%, #c084fc 55%, #9b59f7 80%, #7c3aed 100%);
        """

BG_CSS = get_bg_css()

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400;1,600&family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

html, body, .stApp, [class*="css"] {{
    font-family: 'Syne', sans-serif !important;
}}

.stApp {{
    {BG_CSS}
    min-height: 100vh;
}}

/* Soft overlay matching homepage aesthetic */
.stApp::before {{
    content: '';
    position: fixed;
    inset: 0;
    background: radial-gradient(ellipse at center,
        rgba(255,255,255,0.08) 0%,
        rgba(155,89,247,0.12) 55%,
        rgba(124,58,237,0.32) 100%);
    z-index: 0;
    pointer-events: none;
}}

section[data-testid="stSidebar"] {{ display: none !important; }}
header[data-testid="stHeader"]   {{ display: none !important; }}
footer {{ display: none !important; }}

.block-container {{
    padding: 30px 20px 80px !important;
    max-width: 800px !important;
    position: relative;
    z-index: 1;
    margin-top: 72px !important;
}}

/* ═══════════════════════════════════════
   NAVBAR — refined, matches homepage feel
   ═══════════════════════════════════════ */
.vl-navbar {{
    position: fixed;
    top: 0; left: 0; right: 0;
    z-index: 9999;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 48px;
    height: 64px;
    background: rgba(255,255,255,0.60);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-bottom: 1px solid rgba(155,89,247,0.18);
    box-shadow: 0 2px 32px rgba(155,89,247,0.08);
}}
.vl-navbar-brand {{
    font-family: 'Cormorant Garamond', serif;
    font-size: 26px;
    font-weight: 700;
    color: #2e0d6e;
    letter-spacing: -0.01em;
    text-decoration: none;
}}
.vl-navbar-brand em {{
    font-style: italic;
    color: #9b59f7;
}}
.vl-navbar-links {{
    display: flex;
    align-items: center;
    gap: 36px;
}}
.vl-navbar-link {{
    font-family: 'Syne', sans-serif;
    font-size: 20px;
    font-weight: 600;
    letter-spacing: 0.10em;
    text-transform: uppercase;
    color: #5b21b6;
    text-decoration: none;
    opacity: 0.65;
    transition: opacity 0.2s;
}}
.vl-navbar-link:hover {{ opacity: 1; }}
.vl-navbar-link.active {{
    opacity: 1;
    color: #7c3aed;
    border-bottom: 2px solid #9b59f7;
    padding-bottom: 2px;
}}
.vl-navbar-cta {{
    font-family: 'Syne', sans-serif;
    font-size: 20px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #ffffff;
    background: linear-gradient(135deg, #9b59f7 0%, #7c3aed 100%);
    padding: 9px 24px;
    border-radius: 100px;
    text-decoration: none;
    box-shadow: 0 0 16px rgba(155,89,247,0.35);
    transition: all 0.2s;
}}
.vl-navbar-cta:hover {{
    box-shadow: 0 0 28px rgba(155,89,247,0.55);
    transform: translateY(-1px);
}}

/* ── Badge ── */
.live-badge {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(255,255,255,0.65);
    border: 1.5px solid rgba(155,89,247,0.4);
    border-radius: 100px;
    padding: 9px 24px;
    font-size: 20px;
    font-weight: 700;
    color: #6d28d9;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 32px;
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 20px rgba(155,89,247,0.15);
}}
.live-dot {{
    width: 9px; height: 9px;
    background: #9b59f7;
    border-radius: 50%;
    animation: blink 1.8s ease-in-out infinite;
    box-shadow: 0 0 8px #9b59f7, 0 0 16px #7c3aed;
    flex-shrink: 0;
}}
@keyframes blink {{ 0%,100%{{opacity:1}} 50%{{opacity:0.25}} }}

/* ── Hero headline — Cormorant Garamond like homepage ── */
.hero-h1 {{
    font-family: 'Cormorant Garamond', serif !important;
    font-size: clamp(54px, 8vw, 92px);
    font-weight: 700;
    line-height: 1.0;
    letter-spacing: -0.02em;
    text-align: center;
    margin-bottom: 20px;
    color: #1e0b4b;
}}
.hero-h1 em {{
    font-style: italic;
    color: #9b59f7;
    font-weight: 600;
}}

/* Divider line like homepage */
.hero-divider {{
    width: 1px;
    height: 48px;
    background: linear-gradient(to bottom, transparent, rgba(155,89,247,0.45), transparent);
    margin: 0 auto 28px;
}}

.hero-sub {{
    font-family: 'Syne', sans-serif;
    font-size: 21px;
    font-weight: 400;
    color: #4c1d95;
    text-align: center;
    line-height: 1.6;
    margin-bottom: 52px;
    letter-spacing: 0.01em;
}}

/* ── Input card ── */
.input-glass {{
    background: rgba(255,255,255,0.62);
    border: 1.5px solid rgba(155,89,247,0.28);
    border-radius: 28px;
    padding: 40px 36px 32px;
    backdrop-filter: blur(28px);
    -webkit-backdrop-filter: blur(28px);
    box-shadow:
        0 0 0 1px rgba(155,89,247,0.07),
        0 12px 60px rgba(124,58,237,0.13),
        inset 0 1px 0 rgba(255,255,255,0.95);
}}
.input-label {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 20px;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #9b59f7;
    margin-bottom: 14px;
    display: block;
}}

/* ── Textarea — nuclear box removal ── */
.stTextArea {{ position: relative !important; }}
.stTextArea > div {{
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}}
.stTextArea textarea {{
    font-family: 'Syne', sans-serif !important;
    font-size: 20px !important;
    line-height: 1.65 !important;
    background: rgba(255,255,255,0.82) !important;
    border: 1.5px solid rgba(155,89,247,0.32) !important;
    border-radius: 16px !important;
    color: #2e0d6e !important;
    caret-color: #9b59f7 !important;
    padding: 18px 20px !important;
    transition: all 0.25s ease !important;
    box-shadow: inset 0 2px 10px rgba(155,89,247,0.05) !important;
    resize: none !important;
}}
.stTextArea textarea:focus {{
    border-color: #9b59f7 !important;
    box-shadow:
        0 0 0 3px rgba(155,89,247,0.14),
        inset 0 2px 10px rgba(155,89,247,0.04) !important;
    background: rgba(255,255,255,0.96) !important;
    outline: none !important;
}}
.stTextArea textarea::placeholder {{
    color: rgba(109,40,217,0.32) !important;
    font-size: 18px !important;
    font-style: italic;
}}

/* ── KILL every helper / counter / instructions box ── */
.stTextArea label {{ display: none !important; }}
div[data-testid="InputInstructions"],
p[data-testid="InputInstructions"],
span[data-testid="InputInstructions"],
small[data-testid="InputInstructions"],
.stTextArea [data-testid="InputInstructions"],
.stTextArea [data-baseweb="textarea"] ~ div,
.stTextArea [data-baseweb="textarea"] + div,
.stTextArea > div > div:nth-child(n+2),
.stTextArea > div > div:last-child:not(:first-child) {{
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
    max-height: 0 !important;
    overflow: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
    position: absolute !important;
    margin: 0 !important;
    padding: 0 !important;
}}

/* ── Analyze button ── */
.stButton > button {{
    width: 100% !important;
    background: linear-gradient(135deg, #9b59f7 0%, #7c3aed 60%, #5b21b6 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 100px !important;
    padding: 20px 40px !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 20px !important;
    font-weight: 700 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    cursor: pointer !important;
    box-shadow:
        0 0 28px rgba(155,89,247,0.38),
        0 6px 32px rgba(124,58,237,0.26) !important;
    transition: all 0.22s ease !important;
    margin-top: 14px !important;
}}
.stButton > button:hover {{
    transform: translateY(-2px) !important;
    box-shadow:
        0 0 44px rgba(155,89,247,0.54),
        0 10px 40px rgba(124,58,237,0.36) !important;
}}
.stButton > button:active {{ transform: translateY(0px) !important; }}

/* ── Feature pills ── */
.pills-row {{
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    justify-content: center;
    margin-top: 44px;
}}
.pill {{
    background: rgba(255,255,255,0.65);
    border: 1px solid rgba(155,89,247,0.28);
    border-radius: 100px;
    padding: 11px 24px;
    font-family: 'Syne', sans-serif;
    font-size: 20px;
    font-weight: 600;
    color: #6d28d9;
    backdrop-filter: blur(8px);
    letter-spacing: 0.01em;
    box-shadow: 0 2px 16px rgba(155,89,247,0.10);
}}

/* ── Spinner ── */
.stSpinner > div {{ color: #9b59f7 !important; }}
[data-testid="stSpinner"] p {{
    font-size: 22px !important;
    color: #6d28d9 !important;
}}

/* ── Warning ── */
[data-testid="stAlert"] {{
    background: rgba(255,255,255,0.7) !important;
    border: 1px solid rgba(251,191,36,0.45) !important;
    border-radius: 14px !important;
    color: #92400e !important;
    font-size: 20px !important;
    backdrop-filter: blur(10px) !important;
}}
</style>

<!-- ═══ CUSTOM NAVBAR ═══ -->
<nav class="vl-navbar">
    <a class="vl-navbar-brand" href="/">Venture<em>Lens</em> AI</a>
    <div class="vl-navbar-links">
        <a class="vl-navbar-link" href="/Dashboard">Dashboard</a>
        <a class="vl-navbar-link" href="/Strategic_Advisor">Strategic Advisor</a>
        <a class="vl-navbar-cta" href="/">Get Started</a>
    </div>
</nav>
""", unsafe_allow_html=True)

# ─── PAGE CONTENT ───────────────────────────────────────────────────
st.markdown('<div style="text-align:center;">', unsafe_allow_html=True)

st.markdown('''
<div style="display:flex;justify-content:center;margin-bottom:32px;">
    <div class="live-badge">
        <div class="live-dot"></div>
        Due Diligence Engine &nbsp;·&nbsp; v1.0
    </div>
</div>

<div class="hero-h1">
    Turn your idea into<br><em>venture intelligence</em>
</div>

<div class="hero-divider"></div>

<div class="hero-sub">
    Describe your startup — get NLP extraction, feasibility scoring,<br>
    risk intelligence &amp; survival projections in seconds.
</div>
''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ─── Glass input card ──────────────────────────────────────────────

st.markdown('<span class="input-label">💡 &nbsp;Your Startup Idea</span>', unsafe_allow_html=True)

idea = st.text_area(
    label="idea",
    placeholder="Describe the problem, target market, revenue model, and any early traction…",
    height=190,
    key="idea_input",
    label_visibility="collapsed",
)

clicked = st.button("✦  Analyze My Startup Idea", use_container_width=True)

st.markdown('''
<div style="text-align:center;margin-top:18px;font-size:20px;color:rgba(109,40,217,0.42);
font-family:'JetBrains Mono',monospace;letter-spacing:0.08em;">
⚡ &nbsp;ANALYSIS COMPLETES IN UNDER 3 SECONDS
</div>
''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

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

        import pickle
        with open("temp_analysis.pkl", "wb") as f:
            pickle.dump({
                "idea": idea,
                "extracted": ext,
                "scores": scores,
                "total": total,
                "risks": risks,
                "comps": comps,
                "surv": surv
            }, f)

        st.switch_page("pages/1_Dashboard.py")