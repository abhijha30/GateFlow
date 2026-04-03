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
/* Background */
body {
    background-color: #0f172a;
}

/* Container */
.block-container {
    padding-top: 2rem;
    max-width: 900px;
    margin: auto;
}

/* Headings */
h1, h2, h3 {
    color: white;
    text-align: center;
}

/* Inputs */
.stTextInput input, .stSelectbox div {
    border-radius: 10px !important;
}

/* Buttons */
.stButton>button {
    width: 100%;
    border-radius: 12px;
    height: 45px;
    background: linear-gradient(90deg, #6366f1, #9333ea);
    color: white;
    font-weight: 600;
    border: none;
}

/* Cards */
.card {
    background: #1e293b;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 15px;
    color: white;
}

/* Mobile fix */
@media (max-width: 768px) {
    .block-container {
        padding: 1rem;
    }
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
    "<center style='color:gray;'>© 2026 GateFlow | Final Year Project</center>",
    unsafe_allow_html=True
)
