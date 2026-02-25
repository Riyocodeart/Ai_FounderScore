import streamlit as st
from utils.recommendation_engine import generate_strategic_recommendations

st.set_page_config(page_title="Strategic Advisor", layout="wide")

st.title("🧠 VentureLens AI — Strategic Advisor")

# Check if analysis exists
if "extracted" not in st.session_state or "scores" not in st.session_state:
    st.warning("⚠ Please analyze a startup idea first on the main page.")
    st.stop()

extracted = st.session_state["extracted"]
scores = st.session_state["scores"]

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