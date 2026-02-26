"""shared.py — CSS + purple navbar used by every page"""
import streamlit as st
import os, base64

def _bg(root):
    p = os.path.join(root, "assets", "bg.jpeg")
    if os.path.exists(p):
        with open(p,"rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        return (f'background-image:url("data:image/jpeg;base64,{b64}");'
                'background-size:cover;background-position:center;background-attachment:fixed;')
    return "background:radial-gradient(ellipse at 20% 20%,#1e0040 0%,#0a0015 50%,#000000 100%);"

def inject_css(root, scroll=False):
    st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0;}}
html,body,.stApp,[class*="css"]{{font-family:'Syne',sans-serif!important;color:#fff!important;}}
.stApp{{{_bg(root)}min-height:100vh;overflow-y:auto!important;}}
.stApp::before{{content:'';position:fixed;inset:0;background:rgba(0,0,0,0.83);z-index:0;pointer-events:none;}}
section[data-testid="stSidebar"]{{display:none!important;}}
header[data-testid="stHeader"]{{display:none!important;}}
footer{{display:none!important;}}
.block-container{{padding:0!important;max-width:100%!important;overflow:visible!important;position:relative;z-index:1;}}
div[data-testid="stVerticalBlock"]>div{{gap:0!important;}}
.element-container{{margin:0!important;padding:0!important;}}
[data-testid="column"]{{padding:0 5px!important;}}

/* ═══ PURPLE TOP NAVBAR ═══════════════════════════════ */
.topnav{{
    display:flex;align-items:center;height:56px;width:100%;
    background:linear-gradient(90deg,#3b0082 0%,#5b21b6 45%,#7c3aed 100%);
    border-bottom:1.5px solid rgba(196,181,253,0.40);
    box-shadow:0 3px 28px rgba(124,58,237,0.50);
    padding:0 24px;gap:0;position:sticky;top:0;z-index:9999;
    flex-shrink:0;
}}
.tn-logo{{
    font-size:22px;font-weight:900;letter-spacing:-0.02em;color:#fff;
    text-shadow:0 0 18px rgba(255,255,255,0.9),0 0 45px rgba(196,181,253,0.6);
    display:flex;align-items:center;gap:10px;margin-right:28px;white-space:nowrap;
}}
.tn-dot{{
    width:11px;height:11px;border-radius:50%;background:#e9d5ff;flex-shrink:0;
    box-shadow:0 0 12px #e9d5ff,0 0 28px #c084fc;
    animation:ndot 2s ease-in-out infinite;
}}
@keyframes ndot{{0%,100%{{opacity:1;transform:scale(1)}}50%{{opacity:.35;transform:scale(.72)}}}}
.tn-links{{display:flex;align-items:center;gap:4px;}}
.tn-link{{
    font-size:17px;font-weight:700;color:rgba(255,255,255,0.78);
    padding:7px 20px;border-radius:10px;cursor:pointer;
    text-decoration:none!important;border:1px solid transparent;
    transition:all 0.18s;letter-spacing:0.01em;white-space:nowrap;
}}
.tn-link:hover{{color:#fff;background:rgba(255,255,255,0.14);border-color:rgba(255,255,255,0.24);}}
.tn-active{{color:#fff!important;background:rgba(255,255,255,0.20)!important;border-color:rgba(255,255,255,0.35)!important;text-shadow:0 0 12px rgba(255,255,255,0.55)!important;}}
.tn-right{{margin-left:auto;display:flex;align-items:center;gap:12px;}}
.tn-idea{{font-size:14px;color:rgba(255,255,255,0.45);font-style:italic;max-width:300px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}}

/* ═══ GLASS CARD ══════════════════════════════════════ */
.gc{{background:rgba(255,255,255,0.045);border:1px solid rgba(168,85,247,0.30);border-radius:16px;
    backdrop-filter:blur(20px);box-shadow:0 4px 30px rgba(0,0,0,0.60),inset 0 1px 0 rgba(255,255,255,0.07);
    overflow:hidden;position:relative;padding:13px 15px;}}
.gc::after{{content:'';position:absolute;top:0;left:0;right:0;height:2px;
    background:linear-gradient(90deg,transparent,rgba(168,85,247,0.75),transparent);border-radius:16px 16px 0 0;}}

/* ═══ SIDEBAR CARD ════════════════════════════════════ */
.sc{{background:rgba(76,29,149,0.26);border:1px solid rgba(168,85,247,0.42);border-radius:16px;
    backdrop-filter:blur(24px);box-shadow:0 0 60px rgba(124,58,237,0.22),inset 0 1px 0 rgba(255,255,255,0.09);
    overflow:hidden;padding:18px 16px;display:flex;flex-direction:column;}}

/* ═══ TYPOGRAPHY ══════════════════════════════════════ */
.lbl{{font-family:'JetBrains Mono',monospace;font-size:12px;font-weight:600;letter-spacing:0.17em;
    text-transform:uppercase;color:#a855f7;text-shadow:0 0 10px rgba(168,85,247,0.85);
    margin-bottom:7px;display:block;flex-shrink:0;}}
.lbl-w{{font-family:'JetBrains Mono',monospace;font-size:12px;font-weight:600;letter-spacing:0.17em;
    text-transform:uppercase;color:#c4b5fd;text-shadow:0 0 8px rgba(196,181,253,0.65);
    margin-bottom:5px;display:block;flex-shrink:0;}}
.divline{{height:1px;background:rgba(255,255,255,0.11);margin:10px 0;flex-shrink:0;}}
.bscore{{font-size:80px;font-weight:900;line-height:1;letter-spacing:-0.05em;color:#fff;
    text-shadow:0 0 24px rgba(255,255,255,0.92),0 0 60px rgba(196,181,253,0.68),0 0 95px rgba(168,85,247,0.45);
    margin:4px 0 2px;}}
.bscore-sub{{font-family:'JetBrains Mono',monospace;font-size:17px;color:rgba(196,181,253,0.65);
    margin-bottom:12px;text-shadow:0 0 8px rgba(196,181,253,0.45);}}
.verdict{{display:inline-block;background:rgba(255,255,255,0.12);border:1px solid rgba(255,255,255,0.24);
    border-radius:100px;padding:5px 18px;font-size:18px;font-weight:700;color:#fff;
    text-shadow:0 0 12px rgba(255,255,255,0.55);margin-bottom:12px;}}
.snum{{font-size:52px;font-weight:900;line-height:1;letter-spacing:-0.04em;}}
.sout{{font-size:20px;color:rgba(255,255,255,0.35);font-weight:600;}}
.sbar-bg{{height:5px;background:rgba(255,255,255,0.10);border-radius:3px;overflow:hidden;margin-top:8px;}}
.sbar-fill{{height:100%;border-radius:3px;}}
.ir-lbl{{font-family:'JetBrains Mono',monospace;font-size:10px;font-weight:600;letter-spacing:0.14em;
    text-transform:uppercase;color:#c4b5fd;text-shadow:0 0 5px rgba(196,181,253,0.55);margin-bottom:1px;}}
.ir-val{{font-size:20px;font-weight:700;color:#fff;text-shadow:0 0 14px rgba(255,255,255,0.60);
    margin-bottom:9px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}}
.conf-num{{font-size:30px;font-weight:800;color:#fff;text-shadow:0 0 18px rgba(255,255,255,0.75);margin-bottom:5px;}}
.conf-bg{{height:6px;background:rgba(255,255,255,0.13);border-radius:3px;overflow:hidden;}}
.conf-fill{{height:100%;border-radius:3px;background:linear-gradient(90deg,#7c3aed,#c084fc);
    box-shadow:0 0 12px rgba(196,181,253,0.55);}}
.prob-txt{{font-size:16px;color:rgba(255,255,255,0.62);line-height:1.55;flex:1;overflow:hidden;
    display:-webkit-box;-webkit-line-clamp:4;-webkit-box-orient:vertical;}}
.surv-big{{font-size:44px;font-weight:900;letter-spacing:-0.04em;line-height:1;}}
.surv-sub{{font-size:18px;color:rgba(255,255,255,0.40);}}
.risk-row{{display:flex;align-items:flex-start;gap:11px;padding:10px 12px;border-radius:11px;margin-bottom:7px;flex-shrink:0;}}
.rdot{{width:10px;height:10px;border-radius:50%;flex-shrink:0;margin-top:6px;}}
.rname{{font-family:'JetBrains Mono',monospace;font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:0.07em;margin-bottom:3px;}}
.rdesc{{font-size:15px;line-height:1.50;color:rgba(255,255,255,0.70);}}
.comp-row{{display:flex;align-items:center;gap:10px;padding:8px 11px;border-radius:10px;
    background:rgba(255,255,255,0.045);border:1px solid rgba(168,85,247,0.22);margin-bottom:6px;}}
.cavatar{{width:32px;height:32px;border-radius:8px;flex-shrink:0;display:flex;align-items:center;
    justify-content:center;font-size:14px;font-weight:800;color:#fff;}}
.cname{{flex:1;font-size:20px;font-weight:700;color:#fff;text-shadow:0 0 10px rgba(255,255,255,0.40);}}
.cbar-bg{{width:55px;height:4px;background:rgba(255,255,255,0.11);border-radius:2px;overflow:hidden;}}
.cbar-fill{{height:100%;background:linear-gradient(90deg,#7c3aed,#a855f7);border-radius:2px;box-shadow:0 0 8px rgba(168,85,247,0.55);}}
.chips{{display:flex;gap:8px;flex-shrink:0;}}
.chip{{flex:1;background:rgba(124,58,237,0.20);border:1px solid rgba(168,85,247,0.36);border-radius:11px;padding:9px 10px;text-align:center;}}
.chip-lbl{{font-family:'JetBrains Mono',monospace;font-size:10px;font-weight:600;color:#a855f7;
    text-transform:uppercase;letter-spacing:0.10em;text-shadow:0 0 7px rgba(168,85,247,0.65);margin-bottom:3px;}}
.chip-val{{font-size:22px;font-weight:800;color:#fff;text-shadow:0 0 12px rgba(255,255,255,0.55);}}
.stButton>button{{background:rgba(124,58,237,0.25)!important;color:#c4b5fd!important;
    border:1px solid rgba(168,85,247,0.45)!important;border-radius:10px!important;
    padding:8px 22px!important;font-family:'Syne',sans-serif!important;font-size:17px!important;
    font-weight:700!important;text-shadow:0 0 8px rgba(196,181,253,0.55)!important;
    backdrop-filter:blur(8px)!important;transition:all 0.2s!important;box-shadow:none!important;}}
.stButton>button:hover{{background:rgba(124,58,237,0.60)!important;color:#fff!important;
    border-color:#a855f7!important;box-shadow:0 0 20px rgba(168,85,247,0.50)!important;}}
textarea,.stTextInput input{{background:rgba(0,0,0,0.50)!important;border:1.5px solid rgba(168,85,247,0.42)!important;
    border-radius:12px!important;color:#fff!important;font-family:'Syne',sans-serif!important;font-size:20px!important;
    caret-color:#a855f7!important;}}
textarea:focus,.stTextInput input:focus{{border-color:#a855f7!important;box-shadow:0 0 0 3px rgba(168,85,247,0.20)!important;}}
textarea::placeholder{{color:rgba(255,255,255,0.28)!important;}}
.stTextArea label{{font-size:20px!important;font-weight:700!important;color:#c4b5fd!important;
    text-shadow:0 0 8px rgba(196,181,253,0.5)!important;}}
[data-testid="stSpinner"] p{{font-size:20px!important;color:#c4b5fd!important;}}
[data-testid="stAlert"]{{background:rgba(251,191,36,0.10)!important;border:1px solid rgba(251,191,36,0.35)!important;
    border-radius:12px!important;font-size:20px!important;}}
</style>
""", unsafe_allow_html=True)

def navbar(active="home", idea=""):
    def lnk(page, label, href):
        cls = "tn-link tn-active" if active==page else "tn-link"
        return f'<a class="{cls}" href="{href}" target="_self">{label}</a>'
    idea_html = f'<div class="tn-idea">&ldquo;{idea[:75]}{"&hellip;" if len(idea)>75 else ""}&rdquo;</div>' if idea else ""
    st.markdown(f"""
<div class="topnav">
    <div class="tn-logo"><div class="tn-dot"></div>VentureLens AI</div>
    <div class="tn-links">
        {lnk("home","🏠 Home","/")}
        {lnk("dashboard","📊 Dashboard","/Dashboard")}
        {lnk("about","ℹ️ About","/About")}
    </div>
    <div class="tn-right">{idea_html}</div>
</div>
""", unsafe_allow_html=True)
