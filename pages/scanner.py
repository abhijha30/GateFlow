import streamlit as st
from utils.db import get_all

def show():
    st.markdown("### 📷 QR Verification")

    code = st.text_input("Enter QR Code")

    if not code:
        return

    users = get_all().data

    for u in users:
        if u["qr_code"] == code:
            if u["status"] == "approved":
                st.success("✅ Entry Allowed")
            else:
                st.error("❌ Not Approved")
