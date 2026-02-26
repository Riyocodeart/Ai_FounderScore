import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import os
from utils.recommendation_engine import generate_strategic_recommendations

st.set_page_config(page_title="Strategic Advisor", layout="wide")

st.title("🧠 VentureLens AI — Strategic Advisor")

import os
import pickle

if not os.path.exists("temp_analysis.pkl"):
    st.warning("⚠ Please analyze a startup idea first on the main page.")
    st.stop()

with open("temp_analysis.pkl", "rb") as f:
    data = pickle.load(f)

idea      = data["idea"]
extracted = data["extracted"]
scores    = data["scores"]
total     = data["total"]
risks     = data["risks"]
comps     = data["comps"]
surv      = data["surv"]


strategic_data = generate_strategic_recommendations(extracted, scores)

st.markdown("## 🚀 Strategic Intelligence Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("💪 Key Strengths")
    for s in strategic_data["strengths"]:
        st.success(s)

with col2:
    st.subheader("⚠ Key Weaknesses")
    for w in strategic_data["weaknesses"]:
        st.error(w)

with col3:
    st.subheader("📈 Recommended Action Plan")
    for r in strategic_data["recommendations"]:
        st.info(r)

st.markdown("---")

st.markdown("### 📊 Strategic Context")

st.write("**Industry:**", extracted["industry"])
st.write("**Business Model:**", extracted["business_model"])

st.markdown("---")

# ── Benchmark Comparison ──────────────────────────────────────────────────────
st.markdown("## 📊 Benchmark Comparison")

@st.cache_data
def load_benchmark():
    path = os.path.join(os.path.dirname(__file__), "..", "data", "venturelens_benchmark.csv")
    return pd.read_csv(path)

bench_df       = load_benchmark()
industry       = extracted["industry"]
industry_bench = bench_df[bench_df["Industry"] == industry]
if industry_bench.empty:
    industry_bench = bench_df

bench_n         = len(industry_bench)
bench_avg_total = round(industry_bench["Total Feasibility Score"].mean(), 1)
percentile      = round((industry_bench["Total Feasibility Score"] < total).mean() * 100, 1)

st.caption(f"Your idea vs **{bench_n} startups** in the **{industry}** industry from our dataset.")

m1, m2, m3 = st.columns(3)
m1.metric("Your Feasibility Score", total,
          delta=f"{round(total - bench_avg_total, 1):+} vs industry avg")
m2.metric(f"Industry Avg ({industry})", bench_avg_total)
m3.metric("Your Percentile Rank", f"{percentile}th")

st.markdown("#### Score-by-Score vs Industry")

SCORE_COLS = ["Market Potential","Competition Density","Scalability",
              "Funding Attractiveness","Risk Level","Innovation Score",
              "Market Saturation","Execution Complexity"]
REVERSE    = {"Competition Density","Risk Level","Market Saturation","Execution Complexity"}

bcols = st.columns(4)
for i, metric in enumerate(SCORE_COLS):
    user_val  = scores.get(metric, 0)
    avg_val   = round(industry_bench[metric].mean(), 1)
    delta_val = round(user_val - avg_val, 1)
    pct       = round((industry_bench[metric] < user_val).mean() * 100, 1)

    if metric in REVERSE:
        verdict = "✅ Better than most" if pct <= 25 else ("🟡 Around average" if pct <= 50 else "🔴 Higher than most")
    else:
        verdict = "✅ Top quartile" if pct >= 75 else ("🟡 Above average" if pct >= 50 else "🔴 Below average")

    with bcols[i % 4]:
        st.metric(metric, user_val, delta=f"{delta_val:+} vs avg ({avg_val})")
        st.caption(f"{verdict} · {pct}th pct")