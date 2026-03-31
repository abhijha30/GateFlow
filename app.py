import streamlit as st
from pages import student, admin, scanner

st.set_page_config(page_title="GateFlow", layout="wide")

# 🔥 GLOBAL STYLE
st.markdown("""
<style>
body {
    background-color: #0f172a;
}
.block-container {
    padding-top: 2rem;
    max-width: 900px;
    margin: auto;
}
h1, h2, h3 {
    color: white;
    text-align: center;
}
.stTextInput input {
    border-radius: 10px;
}
.stButton>button {
    width: 100%;
    border-radius: 10px;
    background: linear-gradient(90deg, #6366f1, #9333ea);
    color: white;
}
.card {
    background: #1e293b;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# LOGO
st.image("assets/logo.png", width=120)

st.markdown("## 🚀 GateFlow")
st.caption("Smart Event Entry System")

# NAVIGATION
menu = st.selectbox("", ["Student", "Admin", "Scanner"])

# ROUTING
if menu == "Student":
    student.show()

elif menu == "Admin":
    admin.show()

elif menu == "Scanner":
    scanner.show()
