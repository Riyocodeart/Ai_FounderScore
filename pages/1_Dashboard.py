import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.shared import inject_css, navbar
@st.cache_data
def load_benchmark():
    path = os.path.join(os.path.dirname(__file__), "..", "data", "venturelens_benchmark.csv")
    return pd.read_csv(path)
st.set_page_config(page_title="VentureLens · Dashboard", page_icon="📊",
                   layout="wide", initial_sidebar_state="collapsed")
ROOT = os.path.join(os.path.dirname(__file__), "..")
inject_css(ROOT, scroll=False)
if "extracted" not in st.session_state:
    st.switch_page("app.py")
ext    = st.session_state["extracted"]
scores = st.session_state["scores"]
total  = st.session_state["total"]
risks  = st.session_state["risks"]
comps  = st.session_state["comps"]
surv   = st.session_state["surv"]
idea   = st.session_state.get("idea", "")
navbar("dashboard", idea)
# ── Derived values ───────────────────────────────────────────────
pct       = total / 160
verdict   = "🔴 Needs Work" if pct < 0.4 else ("🟡 Promising" if pct < 0.7 else "🟢 Strong Viable")
conf      = ext.get("analysis_confidence_score", 80)
years_    = ["Y1", "Y2", "Y3", "Y4", "Y5"]
surv_pct  = [round(v * 100, 1) for v in surv]
final_s   = surv_pct[-1]
surv_c    = "#9b59f7" if final_s > 40 else "#ef4444"
gc        = "#ef4444" if pct < 0.4 else ("#f59e0b" if pct < 0.7 else "#9b59f7")
RCOLS     = [("#ef4444", "rgba(239,68,68,0.08)"),
             ("#f97316", "rgba(249,115,22,0.08)"),
             ("#eab308", "rgba(234,179,8,0.08)")]
ACOLS     = ["#7c3aed", "#a855f7", "#6d28d9", "#9333ea", "#8b5cf6"]
comp_list = comps.get("competitors", [])
crowd     = comps.get("market_crowdedness", "—")
press     = comps.get("competitive_pressure_score", "—")
crowd_c   = "#ef4444" if crowd == "Very High" else ("#f97316" if crowd == "High" else "#eab308")
T         = "rgba(0,0,0,0)"
WH        = "rgba(255,255,255,1)"
SCOLS8    = ["#c084fc", "#a855f7", "#7c3aed", "#9333ea", "#e879f9", "#818cf8", "#6d28d9", "#7c3aed"]
# ── Chart helpers ─────────────────────────────────────────────────
def dl(h, **kw):
    d = dict(
        paper_bgcolor=WH, plot_bgcolor=WH,
        margin=dict(t=16, b=16, l=16, r=16), height=h,
        font=dict(family="Syne", color="#2e0d6e", size=13),
        showlegend=False,
    )
    d.update(kw)
    return d
def xax(title="", sz=12, grid=True):
    return dict(
        tickfont=dict(color="rgba(46,13,110,0.60)", size=sz, family="JetBrains Mono"),
        gridcolor="rgba(155,89,247,0.12)" if grid else T,
        zeroline=False, showline=False,
        **({"title": dict(text=title, font=dict(size=13, color="rgba(46,13,110,0.50)"))} if title else {})
    )
def yax(title="", sz=12, suf=""):
    return dict(
        tickfont=dict(color="rgba(46,13,110,0.60)", size=sz, family="JetBrains Mono"),
        gridcolor="rgba(155,89,247,0.12)", zeroline=False, showline=False,
        **({"ticksuffix": suf} if suf else {}),
        **({"title": dict(text=title, font=dict(size=13, color="rgba(46,13,110,0.50)"))} if title else {})
    )
def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

# ── CSS ───────────────────────────────────────────────────────────
st.markdown("""
<style>
/* No horizontal overflow */
html, body, .stApp { overflow-x: hidden !important; }
.block-container { overflow-x: hidden !important; max-width: 100% !important; }
[data-testid="column"] { min-width: 0 !important; overflow: hidden !important; }

/* ── Score mini-card: centered ── */
.sc-mini {
    background: rgba(255,255,255,0.90);
    border: 1.5px solid rgba(155,89,247,0.22);
    border-radius: 18px;                    /* ← 18px radius */
    padding: 18px 12px 14px;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    box-shadow: 0 4px 24px rgba(124,58,237,0.10), inset 0 1px 0 rgba(255,255,255,0.95);
    position: relative;
    overflow: hidden;
}
.sc-mini .lbl {
    text-align: center;
    min-height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
}
.sc-mini .sbar-bg { width: 80%; }

/* ── Sidebar card — center text ── */
.sc { text-align: center !important; }
.sc .ir-val, .sc .conf-num, .sc .bscore, .sc .bscore-sub,
.sc .prob-txt, .sc .lbl-w, .sc .ir-lbl {
    text-align: center !important;
    display: block !important;
}
.sc .conf-bg { margin: 0 auto; }
.sc .verdict { display: block; text-align: center; }

/* ── Chart box — white, 18px radius ── */
.chart-box {
    background: #ffffff;
    border: 1.5px solid rgba(155,89,247,0.18);
    border-radius: 18px;                    /* ← 18px radius */
    padding: 16px 14px 10px;
    box-shadow: 0 4px 28px rgba(124,58,237,0.10), inset 0 1px 0 rgba(255,255,255,1);
    overflow: hidden;
    width: 100%;
}
.chart-box .lbl { text-align: left; }

/* Plotly fix */
.stPlotlyChart { width: 100% !important; }
.stPlotlyChart > div { width: 100% !important; }
iframe { max-width: 100% !important; }

/* Risk rows */
.risk-row { border-radius: 12px; margin-bottom: 9px; }
.rdesc { color: rgba(46,13,110,0.68) !important; }

/* Comp rows */
.comp-row {
    background: rgba(155,89,247,0.06) !important;
    border: 1px solid rgba(155,89,247,0.16) !important;
}
.cname { color: #2e0d6e !important; }

/* ── Chips — now fully white background ── */
.chips { display: flex; gap: 8px; flex-shrink: 0; margin-top: 10px; }
.chip {
    flex: 1;
    background: #ffffff !important;                        /* ← white */
    border: 1.5px solid rgba(155,89,247,0.28) !important;
    border-radius: 18px;                                   /* ← 18px radius */
    padding: 12px 10px;
    text-align: center;
    box-shadow: 0 2px 12px rgba(124,58,237,0.08);
}
.chip-lbl {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px; font-weight: 600;
    color: #9b59f7; text-transform: uppercase;
    letter-spacing: 0.10em; margin-bottom: 5px;
}
.chip-val {
    font-size: 20px; font-weight: 800;
    color: #2e0d6e !important;                             /* ← dark text on white */
}
</style>
""", unsafe_allow_html=True)

CARD_H = 210

# ═══════════════════════════════════════════════════════════════
# LAYOUT
# ═══════════════════════════════════════════════════════════════
col_left, col_right = st.columns([1, 4], gap="small")

# ══ LEFT — sidebar info panel ══════════════════════════════════
with col_left:
    info_rows = (
        f'<div class="ir-lbl">Industry</div>'
        f'<div class="ir-val">{esc(ext.get("industry", "—"))}</div>'
        f'<div class="ir-lbl">Business Model</div>'
        f'<div class="ir-val">{esc(ext.get("business_model", "—"))}</div>'
        f'<div class="ir-lbl">Target Market</div>'
        f'<div class="ir-val">{esc(ext.get("target_market", "—"))}</div>'
    )
    prob = esc(ext.get("problem_statement", "—"))
    st.markdown(
        f'<div class="sc" style="height:calc(100vh - 80px);overflow-y:auto;">'
        f'  <span class="lbl-w">🔮 Feasibility Score</span>'
        f'  <div class="bscore">{total}</div>'
        f'  <div class="bscore-sub">out of 160 pts</div>'
        f'  <div class="verdict">{verdict}</div>'
        f'  <div class="divline"></div>'
        f'  <span class="lbl-w">Extracted Insights</span>'
        f'  {info_rows}'
        f'  <div class="divline"></div>'
        f'  <span class="lbl-w">NLP Confidence</span>'
        f'  <div class="conf-num">{conf}'
        f'    <span style="font-size:15px;color:rgba(109,40,217,0.42);">/100</span>'
        f'  </div>'
        f'  <div class="conf-bg" style="width:90%;margin:0 auto 4px;">'
        f'    <div class="conf-fill" style="width:{conf}%;"></div>'
        f'  </div>'
        f'  <div class="divline"></div>'
        f'  <span class="lbl-w">Problem Statement</span>'
        f'  <div class="prob-txt">{prob}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

# ══ RIGHT — charts area ════════════════════════════════════════
with col_right:
    score_items = list(scores.items())

    # ── Row A: first 4 score cards ─────────────────────────────
    cols_a = st.columns(4, gap="small")
    for i, (lbl, val) in enumerate(score_items[:4]):
        fill = int((val / 20) * 100)
        c    = SCOLS8[i]
        with cols_a[i]:
            st.markdown(
                f'<div class="sc-mini" style="height:{CARD_H}px;">'
                f'  <span class="lbl" style="font-size:10px;color:{c};">'
                f'    {lbl.replace(" ", "<br>")}</span>'
                f'  <div style="color:{c};font-size:52px;font-weight:900;'
                f'    line-height:1;letter-spacing:-0.04em;margin:8px 0;text-align:center;">'
                f'    {val}<span style="font-size:18px;color:rgba(46,13,110,0.35);'
                f'    font-weight:600;">/20</span>'
                f'  </div>'
                f'  <div class="sbar-bg">'
                f'    <div class="sbar-fill" style="width:{fill}%;background:{c};'
                f'      box-shadow:0 0 10px {c}66;"></div>'
                f'  </div>'
                f'</div>',
                unsafe_allow_html=True
            )

    st.markdown('<div style="height:10px;"></div>', unsafe_allow_html=True)

    # ── Row A2: next 4 score cards ─────────────────────────────
    cols_b = st.columns(4, gap="small")
    for i, (lbl, val) in enumerate(score_items[4:]):
        fill = int((val / 20) * 100)
        c    = SCOLS8[i + 4]
        with cols_b[i]:
            st.markdown(
                f'<div class="sc-mini" style="height:{CARD_H}px;">'
                f'  <span class="lbl" style="font-size:10px;color:{c};">'
                f'    {lbl.replace(" ", "<br>")}</span>'
                f'  <div style="color:{c};font-size:52px;font-weight:900;'
                f'    line-height:1;letter-spacing:-0.04em;margin:8px 0;text-align:center;">'
                f'    {val}<span style="font-size:18px;color:rgba(46,13,110,0.35);'
                f'    font-weight:600;">/20</span>'
                f'  </div>'
                f'  <div class="sbar-bg">'
                f'    <div class="sbar-fill" style="width:{fill}%;background:{c};'
                f'      box-shadow:0 0 10px {c}66;"></div>'
                f'  </div>'
                f'</div>',
                unsafe_allow_html=True
            )

    st.markdown('<div style="height:10px;"></div>', unsafe_allow_html=True)

    # ── Row B: Survival | Gauge | Score Bar ────────────────────
    rb1, rb2, rb3 = st.columns([1.4, 1.2, 1.4], gap="small")

    with rb1:
        fig_surv = go.Figure()
        fig_surv.add_trace(go.Scatter(
            x=years_, y=surv_pct,
            fill="tozeroy", fillcolor="rgba(155,89,247,0.14)",
            line=dict(color="#9b59f7", width=3.5),
            mode="lines+markers",
            marker=dict(size=12, color="#9b59f7", line=dict(color="#ffffff", width=2.5)),
            hovertemplate="<b>%{x}</b>  %{y}%<extra></extra>",
        ))
        fig_surv.update_layout(**dl(300,
            xaxis=dict(**xax("", 13, grid=False)),
            yaxis=dict(**yax("Survival %", 12, "%"), range=[0, 105]),
            hovermode="x unified",
            margin=dict(t=14, b=14, l=46, r=14),
        ))
        st.markdown(
            f'<div class="chart-box">'
            f'  <span class="lbl">📈 5-Year Survival Projection</span>'
            f'  <div style="display:flex;align-items:baseline;gap:10px;margin-bottom:4px;">'
            f'    <div style="font-size:42px;font-weight:900;letter-spacing:-0.04em;'
            f'      line-height:1;color:{surv_c};">{final_s}%</div>'
            f'    <div style="font-size:13px;color:rgba(46,13,110,0.45);">5-yr probability</div>'
            f'  </div>',
            unsafe_allow_html=True
        )
        st.plotly_chart(fig_surv, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with rb2:
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number", value=total,
            title=dict(text="Feasibility Score",
                       font=dict(size=15, color="rgba(46,13,110,0.65)", family="Syne")),
            number=dict(font=dict(size=40, color="#2e0d6e", family="Syne"), suffix=f"/{160}"),
            gauge=dict(
                axis=dict(range=[0, 160], nticks=5,
                          tickfont=dict(color="rgba(46,13,110,0.45)", size=11),
                          tickwidth=1, tickcolor="rgba(155,89,247,0.3)"),
                bar=dict(color=gc, thickness=0.28),
                bgcolor=WH, borderwidth=0,
                steps=[
                    dict(range=[0, 64],    color="rgba(239,68,68,0.10)"),
                    dict(range=[64, 112],  color="rgba(155,89,247,0.08)"),
                    dict(range=[112, 160], color="rgba(16,185,129,0.10)")
                ],
                threshold=dict(line=dict(color=gc, width=4), thickness=0.82, value=total),
            ),
        ))
        fig_gauge.update_layout(**dl(300, margin=dict(t=16, b=8, l=16, r=16)))
        st.markdown('<div class="chart-box"><span class="lbl">📊 Feasibility Gauge</span>',
                    unsafe_allow_html=True)
        st.plotly_chart(fig_gauge, use_container_width=True, config={"displayModeBar": False})
        st.markdown(
            '<div style="display:flex;gap:8px;flex-wrap:wrap;justify-content:center;padding-bottom:6px;">'
            '  <span style="font-size:12px;color:#ef4444;font-weight:600;">🔴 0–64 Weak</span>'
            '  <span style="font-size:12px;color:#9b59f7;font-weight:600;">🟣 64–112 Fair</span>'
            '  <span style="font-size:12px;color:#10b981;font-weight:600;">🟢 112+ Strong</span>'
            '</div></div>',
            unsafe_allow_html=True
        )

    with rb3:
        fig_bar = go.Figure(go.Bar(
            x=list(scores.keys()),
            y=list(scores.values()),
            marker=dict(color=SCOLS8[:len(scores)],
                        line=dict(color="rgba(255,255,255,0.5)", width=1), opacity=0.90),
            text=[str(v) for v in scores.values()],
            textposition="outside",
            textfont=dict(color="#2e0d6e", size=13, family="Syne"),
            width=0.6,
        ))
        fig_bar.update_layout(**dl(300,
            xaxis=dict(tickangle=-38,
                       tickfont=dict(color="rgba(46,13,110,0.60)", size=10, family="JetBrains Mono"),
                       gridcolor=T, zeroline=False, showline=False),
            yaxis=dict(**yax("", 11), range=[0, 27]),
            margin=dict(t=14, b=90, l=14, r=14),
        ))
        st.markdown('<div class="chart-box"><span class="lbl">📊 Score Breakdown</span>',
                    unsafe_allow_html=True)
        st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="height:10px;"></div>', unsafe_allow_html=True)

    # ── Row C: Benchmark Radar ─────────────────────────────────
    bench_df       = load_benchmark()
    industry       = ext.get("industry", "")
    industry_bench = bench_df[bench_df["Industry"] == industry]
    if industry_bench.empty:
        industry_bench = bench_df
    bench_n         = len(industry_bench)
    bench_avg_total = round(industry_bench["Total Feasibility Score"].mean(), 1)
    percentile      = round((industry_bench["Total Feasibility Score"] < total).mean() * 100, 1)
    delta_total     = round(total - bench_avg_total, 1)
    delta_sign      = "+" if delta_total >= 0 else ""
    delta_c         = "#9b59f7" if delta_total >= 0 else "#ef4444"
    SCORE_COLS = ["Market Potential", "Competition Density", "Scalability",
                  "Funding Attractiveness", "Risk Level", "Innovation Score",
                  "Market Saturation", "Execution Complexity"]
    user_vals   = [scores.get(m, 0) for m in SCORE_COLS]
    bench_vals  = [round(industry_bench[m].mean(), 1) for m in SCORE_COLS]
    labels_loop = SCORE_COLS + [SCORE_COLS[0]]
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=user_vals + [user_vals[0]], theta=labels_loop,
        fill="toself", name="Your Idea",
        line=dict(color="#9b59f7", width=2.5),
        fillcolor="rgba(155,89,247,0.18)",
        hovertemplate="<b>%{theta}</b>: %{r}<extra></extra>",
    ))
    fig_radar.add_trace(go.Scatterpolar(
        r=bench_vals + [bench_vals[0]], theta=labels_loop,
        fill="toself", name=f"{industry} Avg",
        line=dict(color="#c084fc", width=2, dash="dash"),
        fillcolor="rgba(192,132,252,0.08)",
        hovertemplate="<b>%{theta}</b>: %{r}<extra></extra>",
    ))
    fig_radar.update_layout(
        paper_bgcolor=WH, plot_bgcolor=WH,
        margin=dict(t=30, b=30, l=30, r=30), height=380,
        font=dict(family="Syne", color="#2e0d6e", size=13),
        showlegend=True,
        legend=dict(orientation="h", y=-0.04, x=0.5, xanchor="center",
                    font=dict(size=14, color="rgba(46,13,110,0.75)")),
        polar=dict(
            bgcolor="rgba(248,244,255,1)",
            radialaxis=dict(visible=True, range=[0, 20],
                            tickfont=dict(size=11, color="rgba(46,13,110,0.42)"),
                            gridcolor="rgba(155,89,247,0.14)"),
            angularaxis=dict(tickfont=dict(size=13, color="rgba(46,13,110,0.70)"),
                             gridcolor="rgba(155,89,247,0.14)"),
        ),
    )
    pill_s = ("background:rgba(155,89,247,0.10);border:1px solid rgba(155,89,247,0.28);"
              "border-radius:100px;padding:5px 16px;font-size:13px;color:#6d28d9;font-weight:600;")
    stat_pills = (
        f'<div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px;">'
        f'  <div style="{pill_s}">vs {bench_n} startups in <b>{esc(industry)}</b></div>'
        f'  <div style="{pill_s}">Industry avg: <b>{bench_avg_total}</b></div>'
        f'  <div style="{pill_s}border-color:{delta_c}55;color:{delta_c};">'
        f'    {delta_sign}{delta_total} vs avg</div>'
        f'  <div style="{pill_s}">{percentile}th percentile</div>'
        f'</div>'
    )
    st.markdown(
        f'<div class="chart-box">'
        f'  <span class="lbl">📊 Benchmark vs {esc(industry)} Industry</span>'
        f'  {stat_pills}',
        unsafe_allow_html=True
    )
    st.plotly_chart(fig_radar, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="height:10px;"></div>', unsafe_allow_html=True)

    # ── Row D: Risk | Competitors ──────────────────────────────
    rd1, rd2 = st.columns([1.4, 1], gap="small")

    with rd1:
        risk_html = ""
        for i, (rtype, rdesc) in enumerate(risks.items()):
            rc, rbg = RCOLS[i % len(RCOLS)]
            risk_html += (
                f'<div class="risk-row" style="background:{rbg};border:1px solid {rc}38;">'
                f'  <div class="rdot" style="background:{rc};box-shadow:0 0 8px {rc};"></div>'
                f'  <div style="flex:1;">'
                f'    <div class="rname" style="color:{rc};">{esc(rtype)}</div>'
                f'    <div class="rdesc">{esc(rdesc)}</div>'
                f'  </div>'
                f'</div>'
            )
        st.markdown(
            f'<div class="chart-box" style="height:100%;">'
            f'  <span class="lbl">⚠️ Risk Intelligence</span>'
            f'  {risk_html}'
            f'</div>',
            unsafe_allow_html=True
        )

    with rd2:
        comp_rows = ""
        for i, c in enumerate(comp_list):
            bw = max(18, 100 - i * 17)
            comp_rows += (
                f'<div class="comp-row">'
                f'  <div class="cavatar" style="background:{ACOLS[i % len(ACOLS)]};'
                f'    box-shadow:0 0 12px {ACOLS[i % len(ACOLS)]}55;">'
                f'    {esc(c)[0].upper()}'
                f'  </div>'
                f'  <div class="cname">{esc(c)}</div>'
                f'  <div class="cbar-bg"><div class="cbar-fill" style="width:{bw}%;"></div></div>'
                f'</div>'
            )
        pie_vals = [max(10, 100 - i * 16) for i in range(len(comp_list))]
        fig_pie  = go.Figure(go.Pie(
            labels=comp_list, values=pie_vals, hole=0.54,
            marker=dict(colors=ACOLS[:len(comp_list)],
                        line=dict(color="rgba(255,255,255,0.7)", width=2)),
            textfont=dict(size=12, color="#fff", family="Syne"),
            textposition="outside", textinfo="label",
            hovertemplate="<b>%{label}</b>  %{percent}<extra></extra>",
        ))
        fig_pie.update_layout(**dl(260,
            margin=dict(t=28, b=28, l=28, r=28),
            annotations=[dict(
                text=f"<b>{len(comp_list)}</b><br>rivals",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=20, color="#2e0d6e", family="Syne")
            )],
        ))
        st.markdown(
            f'<div class="chart-box">'
            f'  <span class="lbl">🏢 Competitors</span>'
            f'  {comp_rows}'
            f'  <span class="lbl" style="margin-top:12px;display:block;">Market Share</span>',
            unsafe_allow_html=True
        )
        st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})
        # ── Chips — white background, 18px radius ──
        st.markdown(
            f'<div class="chips">'
            f'  <div class="chip">'
            f'    <div class="chip-lbl">Crowdedness</div>'
            f'    <div class="chip-val" style="color:{crowd_c};font-size:17px;">{esc(crowd)}</div>'
            f'  </div>'
            f'  <div class="chip">'
            f'    <div class="chip-lbl">Pressure Score</div>'
            f'    <div class="chip-val">{press}'
            f'      <span style="font-size:13px;color:rgba(46,13,110,0.38);">/100</span>'
            f'    </div>'
            f'  </div>'
            f'</div></div>',
            unsafe_allow_html=True
        )