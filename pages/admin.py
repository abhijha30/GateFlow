import streamlit as st
from utils.auth import admin_login
from utils.db import *
from utils.qr import generate_qr
from utils.mail import send_qr
import uuid

def show():
    # 🔐 LOGIN CHECK
    if "admin" not in st.session_state:
        admin_login()
        return

    st.markdown("## 🛠 GateFlow - Admin Dashboard")

    # 📅 CREATE EVENT
   if st.button("Create Event", use_container_width=True):
    if not name or not venue:
        st.warning("Fill all fields")
    else:
        create_event({
            "name": name,
            "date": str(date),
            "deadline": str(deadline),
            "venue": venue
        })
        st.success("Event Created")

        st.rerun()  # 🔥 IMPORTANT FIX

    # 📥 APPROVAL SECTION
    st.subheader("📥 Pending Registrations")

    users = get_pending().data

    if not users:
        st.info("No pending requests")
        return

    for user in users:
        st.markdown(f"""
        **👤 {user['name']}**  
        📧 {user['email']}
        """)

        col1, col2 = st.columns(2)

        if col1.button(f"Approve {user['id']}"):
            qr_id = str(uuid.uuid4())
            file = f"{qr_id}.png"

            generate_qr(qr_id, file)
            update_status(user["id"], "approved", qr_id)
            send_qr(user["email"], file)

            st.success("✅ Approved & QR sent")

        if col2.button(f"Reject {user['id']}"):
            update_status(user["id"], "rejected", "")
            st.error("❌ Rejected")

        st.divider()
