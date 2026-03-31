import streamlit as st
from utils.auth import admin_login
from utils.db import *
from utils.qr import generate_qr
from utils.mail import send_qr
import uuid

def show():
    if "admin" not in st.session_state:
        admin_login()
        return

    st.markdown("### 🛠 Admin Dashboard")

    # CREATE EVENT
   st.subheader("📅 Create Event")

name = st.text_input("Event Name")
date = st.date_input("Event Date")
deadline = st.date_input("Registration Deadline")
venue = st.text_input("Venue")

if st.button("Create Event"):
    create_event({
        "name": name,
        "date": str(date),
        "deadline": str(deadline),
        "venue": venue
    })
    st.success("Event Created Successfully")
    # APPROVAL
    st.subheader("Pending Registrations")

    users = get_pending().data

    if not users:
        st.info("No pending requests")
        return

    for user in users:
        with st.container():
            st.markdown(f"""
            <div class='card'>
            👤 {user['name']} <br>
            📧 {user['email']}
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)

            if col1.button(f"Approve {user['id']}"):
                qr_id = str(uuid.uuid4())
                file = f"{qr_id}.png"

                generate_qr(qr_id, file)
                update_status(user["id"], "approved", qr_id)
                send_qr(user["email"], file)

                st.success("Approved & QR sent")

            if col2.button(f"Reject {user['id']}"):
                update_status(user["id"], "rejected", "")
                st.error("Rejected")
