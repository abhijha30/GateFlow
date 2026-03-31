import streamlit as st
from utils.db import get_all

def show():
    st.title("📷 GateFlow - Scanner")

    code = st.text_input("Enter QR Code")

    data = get_all().data

    if code:
        for user in data:
            if user["qr_code"] == code:
                if user["status"] == "approved":
                    st.success("✅ Entry Allowed")
                else:
                    st.error("❌ Not Approved")
