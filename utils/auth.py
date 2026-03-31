import streamlit as st

def admin_login():
    st.subheader("🔐 Admin Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password") 

    if st.button("Login"):
        if username == "i_avinashjha" and password == "gateflow123":
            st.session_state["admin"] = True
        else:
            st.error("Invalid credentials")
