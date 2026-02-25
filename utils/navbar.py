import streamlit as st

def show_navbar():
    st.markdown("""
    <style>
    .nav-bar {
        display:flex;
        gap:20px;
        padding:14px 28px;
        background:#0b120b;
        border-bottom:1px solid rgba(143,173,106,0.25);
        font-family: 'Outfit', sans-serif;
    }
    .nav-btn {
        color:#b8d090;
        text-decoration:none;
        font-size:14px;
        letter-spacing:1px;
    }
    .nav-btn:hover {
        color:#ffffff;
    }
    </style>

    <div class="nav-bar">
        <a class="nav-btn" href="/?page=home">HOME</a>
        <a class="nav-btn" href="/?page=analysis">ANALYSIS</a>
        <a class="nav-btn" href="/?page=competitors">COMPETITORS</a>
        <a class="nav-btn" href="/?page=risk">RISK MODEL</a>
    </div>
    """, unsafe_allow_html=True)