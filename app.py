import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="VentureLens AI",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide ALL streamlit chrome
st.markdown("""
<style>
section[data-testid="stSidebar"],
header[data-testid="stHeader"],
footer,
[data-testid="collapsedControl"],
.stDeployButton { display: none !important; }
html, body, .stApp { background: #faf7ff !important; overflow: hidden !important; margin: 0 !important; padding: 0 !important; }
.block-container { padding: 0 !important; margin: 0 !important; max-width: 100vw !important; }
</style>
""", unsafe_allow_html=True)

# ── Check if START was clicked via session state ──
if st.session_state.get("go_to_analysis"):
    st.session_state["go_to_analysis"] = False
    st.switch_page("pages/1_analysis.py")

# ── Hidden Streamlit button — triggered by JS postMessage ──
col = st.columns([1, 0.01, 1])
with col[1]:
    if st.button("GO", key="hidden_start"):
        st.switch_page("pages/1_analysis.py")

# Hide the real button visually
st.markdown("""
<style>
div[data-testid="stButton"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ── Full landing page in iframe ──
components.html("""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,400&family=Cormorant+Garamond:ital,wght@1,300&family=Josefin+Sans:wght@300;400&display=swap" rel="stylesheet"/>
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  html, body {
    width: 100%; height: 100vh;
    background: #faf7ff;
    font-family: 'Josefin Sans', sans-serif;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .page {
    position: fixed; inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: #faf7ff;
  }

  /* Orbs */
  .orb { position: absolute; border-radius: 50%; filter: blur(90px); pointer-events: none; animation: drift 9s ease-in-out infinite alternate; }
  .o1 { width: 520px; height: 520px; background: #9b59f7; opacity: 0.22; top: -150px; right: -130px; }
  .o2 { width: 400px; height: 400px; background: #c4a8f0; opacity: 0.20; bottom: -130px; left: -110px; animation-delay: -4s; }
  .o3 { width: 240px; height: 240px; background: #a78bfa; opacity: 0.16; top: 35%; left: 6%; animation-delay: -7s; }
  @keyframes drift { from { transform: translate(0,0); } to { transform: translate(24px, 36px); } }

  /* Dot grid */
  .dots { position: absolute; inset: 0; background-image: radial-gradient(circle, #b89fdf 1px, transparent 1px); background-size: 54px 54px; opacity: 0.09; pointer-events: none; }

  /* Corner brackets */
  .corner { position: absolute; width: 50px; height: 50px; border-color: #c4a8f0; border-style: solid; pointer-events: none; }
  .c-tl { top: 24px; left: 24px; border-width: 2px 0 0 2px; }
  .c-tr { top: 24px; right: 24px; border-width: 2px 2px 0 0; }
  .c-bl { bottom: 24px; left: 24px; border-width: 0 0 2px 2px; }
  .c-br { bottom: 24px; right: 24px; border-width: 0 2px 2px 0; }

  /* Content */
  .content { position: relative; z-index: 5; display: flex; flex-direction: column; align-items: center; text-align: center; }

  .eyebrow {
    font-size: 0.65rem; font-weight: 300; letter-spacing: 0.38em;
    color: #9b59f7; display: flex; align-items: center; gap: 14px;
    margin-bottom: 18px; animation: fadeUp 0.8s 0.2s both;
  }
  .eyebrow::before, .eyebrow::after { content: ''; width: 32px; height: 1px; background: #c4a8f0; }

  .logo { font-family: 'Playfair Display', serif; font-size: clamp(3rem, 7vw, 6rem); font-weight: 700; line-height: 1; color: #2e0f6e; margin-bottom: 2px; animation: fadeUp 0.9s 0.35s both; }
  .logo em { font-style: italic; color: #9b59f7; }

  .logo-ai { font-family: 'Cormorant Garamond', serif; font-style: italic; font-size: clamp(1.6rem, 4vw, 3.4rem); color: #5b21b6; letter-spacing: 0.18em; margin-bottom: 24px; animation: fadeUp 0.9s 0.5s both; }

  .vline { width: 1px; height: 44px; background: linear-gradient(to bottom, #9b59f7, transparent); margin-bottom: 18px; animation: fadeUp 0.8s 0.62s both; }

  .tagline { font-size: 0.64rem; font-weight: 300; letter-spacing: 0.3em; color: #7c5cbf; margin-bottom: 42px; animation: fadeUp 0.8s 0.72s both; }

  /* Button row */
  .btn-row { display: flex; align-items: center; gap: 20px; margin-bottom: 56px; animation: fadeUp 0.8s 0.88s both; }

  .start-btn {
    background: #9b59f7; color: #fff; border: none;
    border-radius: 999px; padding: 16px 58px;
    font-family: 'Josefin Sans', sans-serif;
    font-size: 0.75rem; font-weight: 400; letter-spacing: 0.32em;
    cursor: pointer;
    box-shadow: 0 8px 30px rgba(139,92,246,0.40);
    transition: transform 0.2s ease, box-shadow 0.2s ease, background 0.2s ease;
  }
  .start-btn:hover { transform: translateY(-3px); box-shadow: 0 14px 42px rgba(139,92,246,0.58); background: #8540f0; }
  .start-btn:active { transform: translateY(0); }

  .spin-ring { width: 32px; height: 32px; border: 1.5px solid #c4a8f0; border-top-color: #9b59f7; border-radius: 50%; animation: spin 2.2s linear infinite; }
  @keyframes spin { to { transform: rotate(360deg); } }

  /* Stats */
  .stats { display: flex; border-top: 1px solid rgba(155,89,247,0.16); padding-top: 28px; animation: fadeUp 0.8s 1.05s both; }
  .stat { text-align: center; padding: 0 42px; border-right: 1px solid rgba(155,89,247,0.14); }
  .stat:last-child { border-right: none; }
  .stat-val { font-family: 'Playfair Display', serif; font-size: 1.45rem; color: #2e0f6e; display: block; margin-bottom: 4px; }
  .stat-lbl { font-size: 0.55rem; letter-spacing: 0.26em; color: #7c5cbf; }

  .version { position: absolute; bottom: 22px; font-size: 0.54rem; letter-spacing: 0.24em; color: #c4a8f0; font-weight: 300; animation: fadeUp 0.8s 1.2s both; }

  @keyframes fadeUp { from { opacity: 0; transform: translateY(18px); } to { opacity: 1; transform: translateY(0); } }
</style>
</head>
<body>
<div class="page">
  <div class="orb o1"></div>
  <div class="orb o2"></div>
  <div class="orb o3"></div>
  <div class="dots"></div>
  <div class="corner c-tl"></div>
  <div class="corner c-tr"></div>
  <div class="corner c-bl"></div>
  <div class="corner c-br"></div>

  <div class="content">
    <div class="eyebrow">DUE DILIGENCE ENGINE</div>
    <div class="logo">Venture<em>Lens</em></div>
    <div class="logo-ai">AI</div>
    <div class="vline"></div>
    <div class="tagline">AI-POWERED STARTUP FEASIBILITY INTELLIGENCE</div>

    <div class="btn-row">
      <button class="start-btn" onclick="handleStart()">START</button>
      <div class="spin-ring"></div>
    </div>

    <div class="stats">
      <div class="stat"><span class="stat-val">5</span><span class="stat-lbl">DIMENSIONS</span></div>
      <div class="stat"><span class="stat-val">100</span><span class="stat-lbl">POINT SCORE</span></div>
      <div class="stat"><span class="stat-val">AI</span><span class="stat-lbl">INSIGHTS</span></div>
    </div>
  </div>

  <div class="version">V1.0 · HACKATHON EDITION</div>
</div>

<script>
function handleStart() {
  // Click the hidden Streamlit button in the parent frame
  const btn = window.parent.document.querySelector('button[kind="secondary"]') 
           || window.parent.document.querySelector('div[data-testid="stButton"] button');
  if (btn) {
    btn.click();
  } else {
    // Fallback: navigate directly
    window.parent.location.href = window.parent.location.origin + '/1_analysis';
  }
}
</script>
</body>
</html>
""", height=800, scrolling=False)
