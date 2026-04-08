import streamlit as st
from pages import student, admin, scanner

# 🔥 PAGE CONFIG
st.set_page_config(
    page_title="GateFlow",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 🔥 GLOBAL UI STYLE (UPGRADED)
st.markdown("""
<style>

/* 🌌 Background */
body {
    background: linear-gradient(135deg, #0f172a, #020617);
}

/* 📦 Container */
.block-container {
    padding-top: 1.5rem;
    max-width: 1000px;
    margin: auto;
}

/* 🧠 Headings */
h1, h2, h3 {
    color: #f8fafc;
    font-weight: 600;
}

/* 🚀 Card UI */
.card {
    background: linear-gradient(145deg, #1e293b, #0f172a);
    padding: 18px;
    border-radius: 16px;
    margin-bottom: 15px;
    border: 1px solid #334155;
    transition: 0.3s;
}

.card:hover {
    transform: scale(1.02);
    border: 1px solid #6366f1;
}

/* 🎯 Buttons */
.stButton>button {
    width: 100%;
    border-radius: 12px;
    background: linear-gradient(90deg, #6366f1, #9333ea);
    color: white;
    font-weight: 500;
    border: none;
}

.stButton>button:hover {
    opacity: 0.9;
}

/* 🔤 Inputs */
.stTextInput input {
    border-radius: 10px;
}

/* 📊 Metrics */
[data-testid="metric-container"] {
    background: #1e293b;
    padding: 10px;
    border-radius: 12px;
}

/* 🔘 Navigation */
.stRadio > div {
    flex-direction: row;
    gap: 20px;
}

/* 🧊 Divider */
hr {
    border: 1px solid #334155;
}

/* 🖼 Poster */
img {
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)

# 🔥 SESSION INIT (important fix)
if "admin" not in st.session_state:
    st.session_state["admin"] = False

if "student" not in st.session_state:
    st.session_state["student"] = None

# 🔥 HEADER
col1, col2 = st.columns([1, 4])

with col1:
    st.image("assets/logo.png", width=100)

with col2:
    st.markdown("## 🚀 GateFlow")
    st.caption("Smart Event Entry System")

st.divider()

# 🔥 NAVIGATION (UPGRADED UI)
menu = st.radio(
    "Navigation",
    ["Student", "Admin", "Scanner"],
    horizontal=True
)

# 🔥 ROUTING
if menu == "Student":
    student.show()

elif menu == "Admin":
    admin.show()

elif menu == "Scanner":
    scanner.show()

# 🔥 FOOTER
st.divider()
st.markdown(
    "<center style='color:gray;'>© 2026 GateFlow </center>",
    unsafe_allow_html=True
)
