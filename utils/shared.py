"""shared.py — CSS + navbar used by every page (white-purple theme)"""
import streamlit as st
import os, base64


def _bg(root):
    p = os.path.join(root, "assets", "bg.jpeg")
    if os.path.exists(p):
        with open(p, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        return (f'background-image:url("data:image/jpeg;base64,{b64}");'
                'background-size:cover;background-position:center;background-attachment:fixed;')
    return "background:radial-gradient(ellipse at center,#ffffff 0%,#ede0ff 22%,#c9a0f5 50%,#9b59f7 75%,#7c3aed 100%);"


def inject_css(root, scroll=False):
    st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400;1,600&family=Syne:wght@400;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');

*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0;}}
html,body,.stApp,[class*="css"]{{font-family:'Syne',sans-serif!important;}}

/* ── Background ── */
.stApp{{{_bg(root)}min-height:100vh;overflow-y:auto!important;}}
.stApp::before{{
    content:'';position:fixed;inset:0;
    background:radial-gradient(ellipse at center,
        rgba(255,255,255,0.06) 0%,
        rgba(155,89,247,0.10) 55%,
        rgba(124,58,237,0.28) 100%);
    z-index:0;pointer-events:none;
}}

section[data-testid="stSidebar"]{{display:none!important;}}
header[data-testid="stHeader"]{{display:none!important;}}
footer{{display:none!important;}}

.block-container{{
    padding:72px 20px 48px!important;
    max-width:100%!important;
    overflow:visible!important;
    position:relative;z-index:1;
}}
div[data-testid="stVerticalBlock"]>div{{gap:0!important;}}
.element-container{{margin:0!important;padding:0!important;}}
[data-testid="column"]{{padding:0 5px!important;}}

/* ═══════════════════════════════════════════
   NAVBAR — frosted glass, matches homepage
   ═══════════════════════════════════════════ */
.topnav{{
    display:flex;align-items:center;height:64px;width:100%;
    background:rgba(255,255,255,0.62);
    backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);
    border-bottom:1px solid rgba(155,89,247,0.20);
    box-shadow:0 2px 32px rgba(155,89,247,0.10);
    padding:0 48px;gap:0;
    position:fixed;top:0;z-index:9999;flex-shrink:0;
}}
.tn-logo{{
    font-family:'Cormorant Garamond',serif;
    font-size:26px;font-weight:700;letter-spacing:-0.01em;
    color:#2e0d6e;display:flex;align-items:center;gap:10px;
    margin-right:36px;white-space:nowrap;text-decoration:none;
}}
.tn-logo em{{font-style:italic;color:#9b59f7;}}
.tn-dot{{
    width:9px;height:9px;border-radius:50%;
    background:#9b59f7;flex-shrink:0;
    box-shadow:0 0 8px #9b59f7,0 0 16px #7c3aed;
    animation:ndot 1.8s ease-in-out infinite;
}}
@keyframes ndot{{0%,100%{{opacity:1}}50%{{opacity:0.25}}}}

.tn-links{{display:flex;align-items:center;gap:6px;}}
.tn-link{{
    font-family:'Syne',sans-serif;
    font-size:13px;font-weight:600;color:#5b21b6;
    padding:8px 18px;border-radius:100px;cursor:pointer;
    text-decoration:none!important;border:1px solid transparent;
    transition:all 0.18s;letter-spacing:0.08em;white-space:nowrap;
    text-transform:uppercase;opacity:0.7;
}}
.tn-link:hover{{opacity:1;background:rgba(155,89,247,0.10);border-color:rgba(155,89,247,0.25);}}
.tn-active{{
    opacity:1!important;color:#7c3aed!important;
    background:rgba(155,89,247,0.12)!important;
    border-color:rgba(155,89,247,0.35)!important;
}}
.tn-right{{margin-left:auto;display:flex;align-items:center;gap:14px;}}
.tn-cta{{
    font-family:'Syne',sans-serif;font-size:13px;font-weight:700;
    letter-spacing:0.08em;text-transform:uppercase;color:#ffffff;
    background:linear-gradient(135deg,#9b59f7 0%,#7c3aed 100%);
    padding:9px 24px;border-radius:100px;text-decoration:none!important;
    box-shadow:0 0 16px rgba(155,89,247,0.35);transition:all 0.2s;
}}
.tn-cta:hover{{box-shadow:0 0 28px rgba(155,89,247,0.55);transform:translateY(-1px);}}
.tn-idea{{
    font-family:'Syne',sans-serif;font-size:13px;
    color:rgba(75,29,149,0.55);font-style:italic;
    max-width:280px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;
}}

/* ═══════════════════════════════════════════
   GLASS CARD — opaque white
   ═══════════════════════════════════════════ */
.gc{{
    background:rgba(255,255,255,0.80)!important;
    border:1.5px solid rgba(155,89,247,0.22)!important;
    border-radius:20px!important;
    backdrop-filter:blur(20px)!important;
    -webkit-backdrop-filter:blur(20px)!important;
    box-shadow:
        0 0 0 1px rgba(155,89,247,0.07),
        0 8px 40px rgba(124,58,237,0.13),
        inset 0 1px 0 rgba(255,255,255,0.95)!important;
    overflow:hidden;position:relative;padding:16px 18px;
}}
.gc::after{{
    content:'';position:absolute;top:0;left:0;right:0;height:2px;
    background:linear-gradient(90deg,transparent,rgba(155,89,247,0.55),transparent);
    border-radius:20px 20px 0 0;
}}


/* ═══════════════════════════════════════════
   SIDEBAR CARD — opaque white, taller
   ═══════════════════════════════════════════ */
.sc{{
    background:rgba(255,255,255,0.84)!important;
    border:1.5px solid rgba(155,89,247,0.25)!important;
    border-radius:22px!important;
    backdrop-filter:blur(24px)!important;
    -webkit-backdrop-filter:blur(24px)!important;
    box-shadow:
        0 0 0 1px rgba(155,89,247,0.09),
        0 12px 60px rgba(124,58,237,0.14),
        inset 0 1px 0 rgba(255,255,255,0.95)!important;
    overflow:hidden;padding:24px 20px;
    display:flex;flex-direction:column;gap:0;
}}

/* ═══ TYPOGRAPHY ═══════════════════════════ */
.lbl{{
    font-family:'JetBrains Mono',monospace;font-size:11px;font-weight:700;
    letter-spacing:0.18em;text-transform:uppercase;color:#9b59f7;
    margin-bottom:8px;display:block;flex-shrink:0;
}}
.lbl-w{{
    font-family:'JetBrains Mono',monospace;font-size:11px;font-weight:700;
    letter-spacing:0.16em;text-transform:uppercase;color:#7c3aed;
    margin-bottom:6px;display:block;flex-shrink:0;
}}
.divline{{height:1px;background:rgba(155,89,247,0.15);margin:12px 0;flex-shrink:0;}}

/* Score big */
.bscore{{
    font-family:'Cormorant Garamond',serif;
    font-size:80px;font-weight:700;line-height:1;letter-spacing:-0.03em;
    color:#2e0d6e;margin:6px 0 2px;
}}
.bscore-sub{{
    font-family:'JetBrains Mono',monospace;font-size:14px;
    color:rgba(109,40,217,0.55);margin-bottom:12px;
}}
.verdict{{
    display:inline-block;
    background:rgba(155,89,247,0.12);
    border:1.5px solid rgba(155,89,247,0.35);
    border-radius:100px;padding:6px 18px;
    font-size:15px;font-weight:700;color:#6d28d9;
    margin-bottom:14px;
}}

/* Score mini card */
.snum{{font-size:48px;font-weight:900;line-height:1;letter-spacing:-0.04em;}}
.sout{{font-size:18px;color:rgba(46,13,110,0.35);font-weight:600;}}
.sbar-bg{{height:5px;background:rgba(155,89,247,0.12);border-radius:3px;overflow:hidden;margin-top:10px;}}
.sbar-fill{{height:100%;border-radius:3px;}}

/* Info rows */
.ir-lbl{{
    font-family:'JetBrains Mono',monospace;font-size:10px;font-weight:600;
    letter-spacing:0.14em;text-transform:uppercase;color:#9b59f7;margin-bottom:2px;
}}
.ir-val{{
    font-size:15px;font-weight:700;color:#2e0d6e;
    margin-bottom:10px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;
}}

/* Confidence */
.conf-num{{font-size:30px;font-weight:800;color:#2e0d6e;margin-bottom:5px;}}
.conf-bg{{height:6px;background:rgba(155,89,247,0.14);border-radius:3px;overflow:hidden;}}
.conf-fill{{height:100%;border-radius:3px;background:linear-gradient(90deg,#9b59f7,#c084fc);box-shadow:0 0 10px rgba(155,89,247,0.4);}}

/* Problem txt */
.prob-txt{{
    font-size:14px;color:rgba(46,13,110,0.65);line-height:1.6;flex:1;overflow:hidden;
    display:-webkit-box;-webkit-line-clamp:5;-webkit-box-orient:vertical;
}}

/* Survival */
.surv-big{{font-size:40px;font-weight:900;letter-spacing:-0.04em;line-height:1;}}
.surv-sub{{font-size:13px;color:rgba(46,13,110,0.45);}}

/* Risk rows */
.risk-row{{
    display:flex;align-items:flex-start;gap:11px;
    padding:10px 13px;border-radius:12px;margin-bottom:8px;flex-shrink:0;
}}
.rdot{{width:10px;height:10px;border-radius:50%;flex-shrink:0;margin-top:5px;}}
.rname{{
    font-family:'JetBrains Mono',monospace;font-size:12px;font-weight:700;
    text-transform:uppercase;letter-spacing:0.07em;margin-bottom:3px;
}}
.rdesc{{font-size:13px;line-height:1.5;color:rgba(46,13,110,0.72);}}

/* Competitors */
.comp-row{{
    display:flex;align-items:center;gap:10px;padding:8px 12px;border-radius:12px;
    background:rgba(155,89,247,0.07);border:1px solid rgba(155,89,247,0.18);margin-bottom:7px;
}}
.cavatar{{
    width:32px;height:32px;border-radius:8px;flex-shrink:0;
    display:flex;align-items:center;justify-content:center;
    font-size:14px;font-weight:800;color:#fff;
}}
.cname{{flex:1;font-size:14px;font-weight:700;color:#2e0d6e;}}
.cbar-bg{{width:55px;height:4px;background:rgba(155,89,247,0.15);border-radius:2px;overflow:hidden;}}
.cbar-fill{{height:100%;background:linear-gradient(90deg,#9b59f7,#c084fc);border-radius:2px;box-shadow:0 0 8px rgba(155,89,247,0.4);}}

/* Chips */
.chips{{display:flex;gap:8px;flex-shrink:0;margin-top:8px;}}
.chip{{
    flex:1;background:rgba(155,89,247,0.10);
    border:1.5px solid rgba(155,89,247,0.28);
    border-radius:14px;padding:10px;text-align:center;
}}
.chip-lbl{{
    font-family:'JetBrains Mono',monospace;font-size:10px;font-weight:600;
    color:#9b59f7;text-transform:uppercase;letter-spacing:0.10em;margin-bottom:4px;
}}
.chip-val{{font-size:20px;font-weight:800;color:#2e0d6e;}}

/* Streamlit overrides */
.stButton>button{{
    background:linear-gradient(135deg,#9b59f7,#7c3aed)!important;
    color:#fff!important;border:none!important;border-radius:100px!important;
    padding:10px 26px!important;font-family:'Syne',sans-serif!important;
    font-size:15px!important;font-weight:700!important;
    box-shadow:0 0 20px rgba(155,89,247,0.4)!important;transition:all 0.2s!important;
}}
.stButton>button:hover{{
    box-shadow:0 0 32px rgba(155,89,247,0.6)!important;
    transform:translateY(-2px)!important;
}}
textarea,.stTextInput input{{
    background:rgba(255,255,255,0.82)!important;
    border:1.5px solid rgba(155,89,247,0.35)!important;
    border-radius:14px!important;color:#2e0d6e!important;
    font-family:'Syne',sans-serif!important;font-size:18px!important;
    caret-color:#9b59f7!important;
}}
textarea:focus,.stTextInput input:focus{{
    border-color:#9b59f7!important;
    box-shadow:0 0 0 3px rgba(155,89,247,0.18)!important;
}}
[data-testid="stSpinner"] p{{font-size:20px!important;color:#6d28d9!important;}}
[data-testid="stAlert"]{{
    background:rgba(255,255,255,0.7)!important;
    border:1px solid rgba(251,191,36,0.45)!important;
    border-radius:14px!important;font-size:18px!important;color:#92400e!important;
}}
</style>
""", unsafe_allow_html=True)


def navbar(active="home", idea=""):
    def lnk(page, label, href):
        cls = "tn-link tn-active" if active == page else "tn-link"
        return f'<a class="{cls}" href="{href}" target="_self">{label}</a>'

    idea_html = (
        f'<div class="tn-idea">&ldquo;{idea[:70]}{"&hellip;" if len(idea) > 70 else ""}&rdquo;</div>'
        if idea else ""
    )
    st.markdown(f"""
<nav class="topnav">
    <a class="tn-logo" href="/" target="_self">
        <div class="tn-dot"></div>
        Venture<em>Lens</em> AI
    </a>
    <div class="tn-links">
        {lnk("home",    "Analyze",   "/")}
        {lnk("dashboard","Dashboard","/Dashboard")}
        {lnk("about",   "About",     "/About")}
    </div>
    <div class="tn-right">
        {idea_html}
        <a class="tn-cta" href="/" target="_self">New Analysis</a>
    </div>
</nav>
""", unsafe_allow_html=True)