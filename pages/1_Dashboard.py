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

# ── Derived values ──────────────────────────────────────────────
pct       = total / 160
verdict   = "🔴 Needs Work" if pct<0.4 else ("🟡 Promising" if pct<0.7 else "🟢 Strong Viable")
conf      = ext.get("analysis_confidence_score", 80)
years_    = ["Y1","Y2","Y3","Y4","Y5"]
surv_pct  = [round(v*100,1) for v in surv]
final_s   = surv_pct[-1]
surv_c    = "#a855f7" if final_s>40 else "#ef4444"
gc        = "#ef4444" if pct<0.4 else ("#f59e0b" if pct<0.7 else "#a855f7")
SCOLS     = ["#c084fc","#a855f7","#7c3aed","#9333ea"]
RCOLS     = [("#ef4444","rgba(239,68,68,0.13)"),
             ("#f97316","rgba(249,115,22,0.13)"),
             ("#eab308","rgba(234,179,8,0.13)")]
ACOLS     = ["#7c3aed","#a855f7","#6d28d9","#9333ea","#8b5cf6"]
comp_list = comps.get("competitors", [])
crowd     = comps.get("market_crowdedness", "—")
press     = comps.get("competitive_pressure_score", "—")
crowd_c   = "#ef4444" if crowd=="Very High" else ("#f97316" if crowd=="High" else "#eab308")
T         = "rgba(0,0,0,0)"

def dl(h, **kw):
    d = dict(paper_bgcolor=T, plot_bgcolor=T,
             margin=dict(t=10,b=10,l=10,r=10), height=h,
             font=dict(family="Syne",color="#ffffff",size=14),
             showlegend=False)
    d.update(kw)
    return d

def xax(title="", sz=16, grid=True):
    return dict(tickfont=dict(color="rgba(255,255,255,0.65)",size=sz,family="JetBrains Mono"),
                gridcolor="rgba(255,255,255,0.09)" if grid else T,
                zeroline=False, showline=False,
                **({"title":dict(text=title,font=dict(size=15,color="rgba(255,255,255,0.55)"))} if title else {}))

def yax(title="", sz=16, suf=""):
    return dict(tickfont=dict(color="rgba(255,255,255,0.65)",size=sz,family="JetBrains Mono"),
                gridcolor="rgba(255,255,255,0.09)", zeroline=False, showline=False,
                **({"ticksuffix":suf} if suf else {}),
                **({"title":dict(text=title,font=dict(size=15,color="rgba(255,255,255,0.55)"))} if title else {}))

def esc(s): return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

CARD_H = 180

# ═══════════════════════════════════════════════════════════════
# LAYOUT
# ═══════════════════════════════════════════════════════════════
col_left, col_right = st.columns([1, 3.6], gap="small")

# ══ LEFT — sidebar info panel ════════════════════════════════
with col_left:
    # build info rows string first — all in ONE markdown call
    info_rows = (
        f'<div class="ir-lbl">Industry</div><div class="ir-val">{esc(ext.get("industry","—"))}</div>'
        f'<div class="ir-lbl">Business Model</div><div class="ir-val">{esc(ext.get("business_model","—"))}</div>'
        f'<div class="ir-lbl">Target Market</div><div class="ir-val">{esc(ext.get("target_market","—"))}</div>'
    )
    prob = esc(ext.get("problem_statement","—"))

    # ✅ ENTIRE sidebar as ONE st.markdown call — no split divs
    st.markdown(
        f'<div class="sc" style="height:calc(100vh - 72px);">'
        f'  <span class="lbl-w">🔮 Feasibility Score</span>'
        f'  <div class="bscore">{total}</div>'
        f'  <div class="bscore-sub">out of 160 pts</div>'
        f'  <div class="verdict">{verdict}</div>'
        f'  <div class="divline"></div>'
        f'  <span class="lbl-w">Extracted Insights</span>'
        f'  {info_rows}'
        f'  <div class="divline"></div>'
        f'  <span class="lbl-w">NLP Confidence</span>'
        f'  <div class="conf-num">{conf}<span style="font-size:17px;color:rgba(196,181,253,0.55);">/100</span></div>'
        f'  <div class="conf-bg"><div class="conf-fill" style="width:{conf}%;"></div></div>'
        f'  <div class="divline"></div>'
        f'  <span class="lbl-w">Problem Statement</span>'
        f'  <div class="prob-txt">{prob}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

# ══ RIGHT — charts area ═══════════════════════════════════════
with col_right:

    # ── Row 1a: first 4 score cards ───────────────────────────
    score_items = list(scores.items())
    SCOLS8 = ["#c084fc","#a855f7","#7c3aed","#9333ea","#e879f9","#818cf8","#6d28d9","#7c3aed"]

    sc1,sc2,sc3,sc4 = st.columns([1,1,1,1], gap="small")
    for i, (lbl,val) in enumerate(score_items[:4]):
        fill = int((val/20)*100)
        c    = SCOLS8[i]
        with [sc1,sc2,sc3,sc4][i]:
            st.markdown(
                f'<div class="gc" style="height:{CARD_H}px;">'
                f'  <span class="lbl" style="font-size:11px;">{lbl.replace(" ","<br>")}</span>'
                f'  <div class="snum" style="color:{c};margin:auto 0 6px;'
                f'    text-shadow:0 0 22px {c}BB,0 0 55px {c}55;">'
                f'    {val}<span class="sout">/20</span>'
                f'  </div>'
                f'  <div class="sbar-bg">'
                f'    <div class="sbar-fill" style="width:{fill}%;background:{c};box-shadow:0 0 12px {c}AA;"></div>'
                f'  </div>'
                f'</div>',
                unsafe_allow_html=True
            )

    st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)

    # ── Row 1b: next 4 score cards + survival chart ────────────
    sc5,sc6,sc7,sc8,sc9 = st.columns([1,1,1,1,1.6], gap="small")
    for i, (lbl,val) in enumerate(score_items[4:]):
        fill = int((val/20)*100)
        c    = SCOLS8[i+4]
        with [sc5,sc6,sc7,sc8][i]:
            st.markdown(
                f'<div class="gc" style="height:{CARD_H}px;">'
                f'  <span class="lbl" style="font-size:11px;">{lbl.replace(" ","<br>")}</span>'
                f'  <div class="snum" style="color:{c};margin:auto 0 6px;'
                f'    text-shadow:0 0 22px {c}BB,0 0 55px {c}55;">'
                f'    {val}<span class="sout">/20</span>'
                f'  </div>'
                f'  <div class="sbar-bg">'
                f'    <div class="sbar-fill" style="width:{fill}%;background:{c};box-shadow:0 0 12px {c}AA;"></div>'
                f'  </div>'
                f'</div>',
                unsafe_allow_html=True
            )

    # ── Survival chart ─────────────────────────────────────────
    with sc9:
        fig_surv = go.Figure()
        fig_surv.add_trace(go.Scatter(
            x=years_, y=surv_pct,
            fill="tozeroy", fillcolor="rgba(168,85,247,0.15)",
            line=dict(color="#a855f7",width=3.5),
            mode="lines+markers",
            marker=dict(size=11,color="#a855f7",line=dict(color="rgba(255,255,255,0.55)",width=2)),
            hovertemplate="<b>%{x}</b>  %{y}%<extra></extra>",
        ))
        fig_surv.update_layout(**dl(CARD_H-20,
            xaxis=dict(**xax("Year",15,grid=False)),
            yaxis=dict(**yax("Survival %",15,"%"), range=[0,100]),
            hovermode="x unified",
        ))
        # ✅ open div, plotly chart, close div — all three valid alone
        st.markdown(
            f'<div class="gc" style="height:{CARD_H}px;">'
            f'  <span class="lbl">📈 5-Year Survival</span>'
            f'  <div style="display:flex;align-items:baseline;gap:10px;">'
            f'    <div class="surv-big" style="color:{surv_c};text-shadow:0 0 22px {surv_c}BB;">{final_s}%</div>'
            f'    <div class="surv-sub">5-yr probability</div>'
            f'  </div>',
            unsafe_allow_html=True
        )
        st.plotly_chart(fig_surv, use_container_width=True, config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)

    # ── Benchmark Row ──────────────────────────────────────────
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
    delta_c         = "#a855f7" if delta_total >= 0 else "#ef4444"

    SCORE_COLS  = ["Market Potential","Competition Density","Scalability",
                   "Funding Attractiveness","Risk Level","Innovation Score",
                   "Market Saturation","Execution Complexity"]
    REVERSE     = {"Competition Density","Risk Level","Market Saturation","Execution Complexity"}

    user_vals   = [scores.get(m, 0) for m in SCORE_COLS]
    bench_vals  = [round(industry_bench[m].mean(), 1) for m in SCORE_COLS]
    labels_loop = SCORE_COLS + [SCORE_COLS[0]]

    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=user_vals + [user_vals[0]], theta=labels_loop,
        fill="toself", name="Your Idea",
        line=dict(color="#a855f7", width=2.5),
        fillcolor="rgba(168,85,247,0.18)",
        hovertemplate="<b>%{theta}</b>: %{r}<extra></extra>",
    ))
    fig_radar.add_trace(go.Scatterpolar(
        r=bench_vals + [bench_vals[0]], theta=labels_loop,
        fill="toself", name=f"{industry} Avg",
        line=dict(color="#c084fc", width=2, dash="dash"),
        fillcolor="rgba(192,132,252,0.07)",
        hovertemplate="<b>%{theta}</b>: %{r}<extra></extra>",
    ))
    fig_radar.update_layout(
        paper_bgcolor=T, plot_bgcolor=T,
        margin=dict(t=20, b=20, l=20, r=20), height=260,
        font=dict(family="Syne", color="#ffffff", size=13),
        showlegend=True,
        legend=dict(orientation="h", y=-0.08, x=0.5, xanchor="center",
                    font=dict(size=13, color="rgba(255,255,255,0.7)")),
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, 20],
                            tickfont=dict(size=11, color="rgba(255,255,255,0.35)"),
                            gridcolor="rgba(255,255,255,0.08)"),
            angularaxis=dict(tickfont=dict(size=12, color="rgba(255,255,255,0.6)"),
                             gridcolor="rgba(255,255,255,0.08)"),
        ),
    )

    # stat pills html
    stat_pills = (
        f'<div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:10px;">'
        f'  <div style="background:rgba(168,85,247,0.12);border:1px solid rgba(168,85,247,0.35);'
        f'    border-radius:100px;padding:5px 16px;font-size:13px;color:#c4b5fd;">'
        f'    vs {bench_n} startups in <b>{esc(industry)}</b>'
        f'  </div>'
        f'  <div style="background:rgba(168,85,247,0.12);border:1px solid rgba(168,85,247,0.35);'
        f'    border-radius:100px;padding:5px 16px;font-size:13px;color:#c4b5fd;">'
        f'    Industry avg: <b>{bench_avg_total}</b>'
        f'  </div>'
        f'  <div style="background:rgba(168,85,247,0.12);border:1px solid {delta_c}55;'
        f'    border-radius:100px;padding:5px 16px;font-size:13px;color:{delta_c};">'
        f'    {delta_sign}{delta_total} vs avg'
        f'  </div>'
        f'  <div style="background:rgba(168,85,247,0.12);border:1px solid rgba(168,85,247,0.35);'
        f'    border-radius:100px;padding:5px 16px;font-size:13px;color:#c4b5fd;">'
        f'    {percentile}th percentile'
        f'  </div>'
        f'</div>'
    )

    st.markdown(
        f'<div class="gc">'
        f'  <span class="lbl">📊 Benchmark vs {esc(industry)} Industry</span>'
        f'  {stat_pills}',
        unsafe_allow_html=True
    )
    st.plotly_chart(fig_radar, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)

    # ── Row 2: Gauge | Bar | Risk | Competitors ────────────────
    r2a,r2b,r2c,r2d = st.columns([1,1.2,1.4,1.2], gap="small")

    # ── Gauge ─────────────────────────────────────────────────
    with r2a:
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number", value=total,
            title=dict(text="Feasibility Score",
                       font=dict(size=18,color="rgba(255,255,255,0.78)",family="Syne")),
            number=dict(font=dict(size=36,color="#fff",family="Syne"), suffix=f"/{160}"),
            gauge=dict(
                axis=dict(range=[0,160],nticks=5,
                          tickfont=dict(color="rgba(255,255,255,0.52)",size=12),
                          tickwidth=1,tickcolor="rgba(255,255,255,0.28)"),
                bar=dict(color=gc,thickness=0.30),
                bgcolor=T, borderwidth=0,
                steps=[dict(range=[0,64],   color="rgba(239,68,68,0.13)"),
                       dict(range=[64,112], color="rgba(168,85,247,0.10)"),
                       dict(range=[112,160],color="rgba(16,185,129,0.13)")],
                threshold=dict(line=dict(color=gc,width=4),thickness=0.85,value=total),
            ),
        ))
        fig_gauge.update_layout(**dl(300))

        st.markdown('<div class="gc"><span class="lbl">📊 Feasibility Gauge</span>',
                    unsafe_allow_html=True)
        st.plotly_chart(fig_gauge, use_container_width=True, config={"displayModeBar":False})
        st.markdown(
            '<div style="display:flex;gap:6px;flex-wrap:wrap;margin-top:4px;padding-bottom:8px;">'
            '  <span style="font-size:13px;color:rgba(239,68,68,0.92);">🔴 0–64 Weak</span>'
            '  <span style="font-size:13px;color:rgba(168,85,247,0.92);">🟣 64–112 Fair</span>'
            '  <span style="font-size:13px;color:rgba(16,185,129,0.92);">🟢 112+ Strong</span>'
            '</div></div>',
            unsafe_allow_html=True
        )

    # ── Score bar chart ───────────────────────────────────────
    with r2b:
        fig_bar = go.Figure(go.Bar(
            x=list(scores.keys()),
            y=list(scores.values()),
            marker=dict(color=SCOLS8[:len(scores)],
                        line=dict(color="rgba(255,255,255,0.07)",width=1)),
            text=[str(v) for v in scores.values()],
            textposition="outside",
            textfont=dict(color="#ffffff",size=13,family="Syne"),
            width=0.6,
        ))
        fig_bar.update_layout(**dl(300,
            xaxis=dict(tickangle=-45,
                       tickfont=dict(color="rgba(255,255,255,0.6)",size=10,family="JetBrains Mono"),
                       gridcolor=T, zeroline=False, showline=False),
            yaxis=dict(**yax("",12), range=[0,26]),
            margin=dict(t=10,b=90,l=10,r=10),
        ))
        st.markdown('<div class="gc"><span class="lbl">📊 Score Breakdown</span>',
                    unsafe_allow_html=True)
        st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar":False})
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Risk panel ────────────────────────────────────────────
    with r2c:
        risk_html = ""
        for i,(rtype,rdesc) in enumerate(risks.items()):
            rc,rbg = RCOLS[i%len(RCOLS)]
            risk_html += (
                f'<div class="risk-row" style="background:{rbg};border:1px solid {rc}42;">'
                f'  <div class="rdot" style="background:{rc};box-shadow:0 0 10px {rc};"></div>'
                f'  <div>'
                f'    <div class="rname" style="color:{rc};text-shadow:0 0 10px {rc}99;">{esc(rtype)}</div>'
                f'    <div class="rdesc">{esc(rdesc)}</div>'
                f'  </div>'
                f'</div>'
            )
        st.markdown(
            f'<div class="gc"><span class="lbl">⚠️ Risk Intelligence</span>'
            f'{risk_html}</div>',
            unsafe_allow_html=True
        )

    # ── Competitors + donut pie ───────────────────────────────
    with r2d:
        comp_rows = ""
        for i,c in enumerate(comp_list):
            bw = max(18,100-i*17)
            comp_rows += (
                f'<div class="comp-row">'
                f'  <div class="cavatar" style="background:{ACOLS[i%len(ACOLS)]};'
                f'    box-shadow:0 0 14px {ACOLS[i%len(ACOLS)]}66;">{esc(c)[0].upper()}</div>'
                f'  <div class="cname">{esc(c)}</div>'
                f'  <div class="cbar-bg"><div class="cbar-fill" style="width:{bw}%;"></div></div>'
                f'</div>'
            )

        pie_vals = [max(10,100-i*16) for i in range(len(comp_list))]
        fig_pie  = go.Figure(go.Pie(
            labels=comp_list, values=pie_vals, hole=0.52,
            marker=dict(colors=ACOLS[:len(comp_list)],
                        line=dict(color="rgba(0,0,0,0.45)",width=2)),
            textfont=dict(size=13,color="#fff",family="Syne"),
            textposition="outside", textinfo="label",
            hovertemplate="<b>%{label}</b>  %{percent}<extra></extra>",
        ))
        fig_pie.update_layout(**dl(220,
            margin=dict(t=30,b=30,l=30,r=30),
            annotations=[dict(text=f"<b>{len(comp_list)}</b><br>rivals",
                              x=0.5,y=0.5,showarrow=False,
                              font=dict(size=18,color="#fff",family="Syne"))],
        ))

        st.markdown(
            f'<div class="gc"><span class="lbl">🏢 Competitors</span>'
            f'{comp_rows}'
            f'<span class="lbl" style="margin-top:10px;">Market Share</span>',
            unsafe_allow_html=True
        )
        st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar":False})
        st.markdown(
            f'<div class="chips">'
            f'  <div class="chip">'
            f'    <div class="chip-lbl">Crowdedness</div>'
            f'    <div class="chip-val" style="color:{crowd_c};font-size:18px;'
            f'      text-shadow:0 0 14px {crowd_c}BB;">{esc(crowd)}</div>'
            f'  </div>'
            f'  <div class="chip">'
            f'    <div class="chip-lbl">Pressure Score</div>'
            f'    <div class="chip-val">{press}'
            f'      <span style="font-size:14px;color:rgba(255,255,255,0.38);">/100</span>'
            f'    </div>'
            f'  </div>'
            f'</div></div>',
            unsafe_allow_html=True
        )
