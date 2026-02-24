import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

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