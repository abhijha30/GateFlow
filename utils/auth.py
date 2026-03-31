import streamlit as st

def admin_login():
    st.subheader("🔐 Admin Login")

    username = st.text_input("i_avinashjha")
    password = st.text_input("Password", type="Avinash@123")

    if st.button("Login"):
        if username == "admin" and password == "gateflow123":
            st.session_state["admin"] = True
        else:
            st.error("Invalid credentials")
