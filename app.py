import streamlit as st
from utils.nlp_engine import extract_startup_info
from utils.scoring import calculate_scores

st.set_page_config(page_title="FounderScore", layout="wide")

st.title("🚀 VentureLens AI")
st.subheader("AI-Powered Startup Feasibility Engine")

idea_input = st.text_area("Describe your startup idea:")

if st.button("Analyze Idea"):

    if idea_input.strip() == "":
        st.warning("Please enter a startup idea.")
    else:
        with st.spinner("Analyzing..."):

            extracted = extract_startup_info(idea_input)
            scores, total = calculate_scores()

        st.success("Analysis Complete")

        st.header("📌 Extracted Insights")
        st.json(extracted)

        st.header("📊 Feasibility Scores")
        st.write(scores)
        st.metric("Total Feasibility Score", total)

        # Aarya 

import streamlit.components.v1 as components



st.markdown("""
    <style>
        .block-container {
            padding: 0rem;
        }
        header {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

with open("landing.html", "r", encoding="utf-8") as f:
    html_code = f.read()

components.html(html_code, height=1100, scrolling=False)