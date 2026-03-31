import streamlit as st
from utils.db import *
from utils.qr import generate_qr
from utils.mail import send_qr
from utils.auth import admin_login
import uuid

def show():
    if "admin" not in st.session_state:
        admin_login()
        return

    st.title("🛠 GateFlow - Admin Dashboard")

    st.subheader("Create Event")
    name = st.text_input("Event Name")
    date = st.text_input("Date")
    venue = st.text_input("Venue")

    if st.button("Create"):
        create_event({"name": name, "date": date, "venue": venue})
        st.success("Event Created")

    st.subheader("Pending Approvals")
    data = get_pending().data

    for user in data:
        st.write(user["name"], user["email"])

        if st.button(f"Approve {user['id']}"):
            qr_id = str(uuid.uuid4())
            file = f"{qr_id}.png"

            generate_qr(qr_id, file)
            update_status(user["id"], "approved", qr_id)
            send_qr(user["email"], file)

            st.success("Approved & Email Sent")

        if st.button(f"Reject {user['id']}"):
            update_status(user["id"], "rejected", "")
            st.error("Rejected")
