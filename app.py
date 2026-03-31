import streamlit as st
from pages import student, admin, scanner

st.set_page_config(page_title="GateFlow", layout="wide")

# HEADER
st.image("assets/logo.png", width=180)
st.markdown("<h3 style='text-align:center;'>Smart Event Entry System</h3>", unsafe_allow_html=True)

# NAV
menu = st.radio("", ["🎓 Student", "🛠 Admin", "📷 Scanner"], horizontal=True)

if menu == "🎓 Student":
    student.show()

elif menu == "🛠 Admin":
    admin.show()

elif menu == "📷 Scanner":
    scanner.show()

st.markdown("<hr><center>🚀 GateFlow</center>", unsafe_allow_html=True)
