import streamlit as st
from utils.nlp_engine import extract_startup_info
from utils.scoring import (
    calculate_scores,
    generate_risk_analysis,
    simulate_survival,
    get_competitor_insights
)
import plotly.graph_objects as go


st.set_page_config(page_title="VentureLens AI", layout="wide")

st.sidebar.title("🚀 AI FounderScore")
st.sidebar.markdown("### Investor-Grade Startup Analysis Engine")
st.sidebar.info(
    "This AI system evaluates startup feasibility using "
    "NLP, risk modeling, competitive intelligence, and survival simulation."
)
st.sidebar.markdown("---")
st.sidebar.success("Hackathon Prototype v1.0")


st.title("🚀 VentureLens AI")
st.subheader("AI-Powered Startup Feasibility Engine")

idea_input = st.text_area("Describe your startup idea:")

if st.button("Analyze Idea"):

    if idea_input.strip() == "":
        st.warning("Please enter a startup idea.")
    else:
        with st.spinner("Analyzing..."):

            # ✅ Extract NLP insights
            extracted = extract_startup_info(idea_input)

            # ✅ Pass extracted into scoring
            scores, total = calculate_scores(extracted)

            risk_analysis = generate_risk_analysis(extracted, scores)
            
            competitor_data = get_competitor_insights(extracted)

        st.success("Analysis Complete")
        
        
        
        st.header("📌 Extracted Insights")


        col1, col2 = st.columns(2)

        with col1:
            st.write("**Industry:**", extracted["industry"])
            st.write("**Business Model:**", extracted["business_model"])
            st.write("**Target Market:**", extracted["target_market"])

        with col2:
            st.write("**Problem Statement:**")
            st.info(extracted["problem_statement"])

        # -------------------------
        # Confidence Score
        # -------------------------
        st.subheader("🧠 NLP Confidence Score")
        st.progress(extracted["analysis_confidence_score"] / 100)
        st.metric("Confidence Score", f'{extracted["analysis_confidence_score"]}/100')

        # -------------------------
        # Feasibility Scores
        # -------------------------
        st.markdown("## 📊 Executive Summary")

        gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=total,
            title={'text': "Feasibility Score"},
            gauge={
                'axis': {'range': [0, 160]},
            }
        ))
        
        st.plotly_chart(gauge, use_container_width=True)        
        # -------------------------
        # Extracted Insights Section
        # -------------------------
        
            
            
        st.markdown("## 📈 Score Breakdown")                                 

        cols = st.columns(4)

        for i, (key, value) in enumerate(scores.items()):
            cols[i % 4].metric(key, value)


        # -------------------------
        # Risk Analysis Section
        # -------------------------
   

        st.markdown("## 🔍 Market & Risk Intelligence")

        col_left, col_right = st.columns(2)

        with col_left:
            st.subheader("📉 Risk Analysis")
            for risk_type, explanation in risk_analysis.items():
                st.warning(f"**{risk_type}:** {explanation}")

        with col_right:
            st.subheader("🏢 Competitor Landscape")
            for comp in competitor_data["competitors"]:
                st.write("•", comp)

            st.metric("Market Crowdedness",
                      competitor_data["market_crowdedness"])        

        # -------------------------
# Survival Simulation
# -------------------------
        st.header("📈 5-Year Survival Projection")

        survival_rates = simulate_survival(total)

        import plotly.graph_objects as go

        years = [f"Year {i+1}" for i in range(len(survival_rates))]

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=years,
            y=survival_rates,
            mode='lines+markers'
        ))

        fig.update_layout(
            title="Startup Survival Probability Over 5 Years",
            xaxis_title="Time",
            yaxis_title="Survival Probability",
            yaxis=dict(range=[0, 1])
        )

        st.plotly_chart(fig, use_container_width=True)

        final_probability = survival_rates[-1]
        st.metric("Estimated 5-Year Survival Probability", f"{round(final_probability*100, 2)}%")
        
        
        
        
        # -------------------------
# Competitor Landscape
# -------------------------
        st.header("🏢 Competitor Landscape")

        competitor_data = get_competitor_insights(extracted)

        st.subheader("Top Competitors")

        for comp in competitor_data["competitors"]:
            st.write("•", comp)

        st.subheader("Market Crowdedness Level")
        st.metric("Crowdedness", competitor_data["market_crowdedness"])

        st.metric("Competitive Pressure Score",
                  competitor_data["competitive_pressure_score"])
        
        
