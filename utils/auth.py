import streamlit as st

def admin_login():
    user = st.text_input("Admin Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if user == "admin" and pwd == "1234":
            st.session_state["admin"] = True
        else:
            st.error("Invalid Credentials")
