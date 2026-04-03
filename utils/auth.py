import streamlit as st
import random

# 🔥 Temporary OTP store
otp_store = {}

# 📩 SEND OTP (demo)
def send_otp(email):
    otp = str(random.randint(1000, 9999))
    otp_store[email] = otp
    st.info(f"Demo OTP: {otp}")  # Replace with email later


# 🎓 STUDENT LOGIN
def student_login():
    st.subheader("🔐 Student Login (OTP)")

    email = st.text_input("Email")

    col1, col2 = st.columns(2)

    if col1.button("Send OTP"):
        if email:
            send_otp(email)
        else:
            st.warning("Enter email")

    otp = st.text_input("Enter OTP")

    if col2.button("Verify OTP"):
        if email in otp_store and otp_store[email] == otp:
            st.session_state["student"] = email
            st.success("Login successful")
        else:
            st.error("Invalid OTP")


# 🔐 ADMIN LOGIN (UPDATED USERNAME)
def admin_login():
    st.subheader("🔐 Admin Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "i_avinashjha" and password == "gateflow123":
            st.session_state["admin"] = True
        else:
            st.error("Invalid credentials")
