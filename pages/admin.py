import streamlit as st
from utils.auth import admin_login
from utils.db import *
from utils.qr import generate_qr
from utils.mail import send_qr
import uuid
import pandas as pd

def show():

    # 🔐 LOGIN CHECK
    if not st.session_state.get("admin"):
        admin_login()
        return

    st.markdown("## 🛠 GateFlow Admin Dashboard")

    # ================== CREATE EVENT ==================
    st.subheader("📅 Create Event")

    name = st.text_input("Event Name")
    date = st.date_input("Event Date")
    deadline = st.date_input("Registration Deadline")
    venue = st.text_input("Venue")
    capacity = st.number_input("Capacity", min_value=1)

    poster = st.file_uploader("Upload Poster", type=["png","jpg","jpeg"])

    if st.button("Create Event", use_container_width=True):
        create_event({
            "name": name,
            "date": str(date),
            "deadline": str(deadline),
            "venue": venue,
            "capacity": capacity,
            "poster": poster.name if poster else None
        })
        st.success("✅ Event Created")
        st.rerun()

    st.divider()

    # ================== SHOW EVENTS ==================
    st.subheader("📢 All Events")

    events = get_events().data

    for i, e in enumerate(events, start=1):
        st.markdown(f"""
        {i}. 🎯 {e['name']}  
        📅 {e['date']} | ⏳ {e.get('deadline','N/A')}  
        📍 {e['venue']}
        """)

    st.divider()

    # ================== REGISTRATIONS ==================
    data = get_all().data

    tab1, tab2, tab3 = st.tabs(["⏳ Pending", "✅ Approved", "❌ Rejected"])

    # 🔹 PENDING
    with tab1:
        pending = [u for u in data if u["status"] == "pending"]

        if not pending:
            st.info("No pending requests")

        for i, user in enumerate(pending, start=1):

            st.markdown(f"""
            **{i}. 👤 {user['name']}**  
            📧 {user['email']}  
            📱 {user.get('mobile','')}  
            🎓 {user.get('course','')} - {user.get('year','')}
            """)

            col1, col2 = st.columns(2)

            if col1.button(f"Approve {user['id']}"):
                qr_id = str(uuid.uuid4())

                file_path = generate_qr(qr_id)

                update_status(user["id"], "approved", qr_id)
                send_qr(user["email"], file_path)

                st.success("✅ Approved & QR sent")
                st.rerun()

            if col2.button(f"Reject {user['id']}"):
                update_status(user["id"], "rejected", "")
                st.error("❌ Rejected")
                st.rerun()

            st.divider()

    # 🔹 APPROVED
    with tab2:
        approved = [u for u in data if u["status"] == "approved"]

        for i, user in enumerate(approved, start=1):
            st.success(f"{i}. {user['name']} | {user.get('course','')}")

    # 🔹 REJECTED
    with tab3:
        rejected = [u for u in data if u["status"] == "rejected"]

        for i, user in enumerate(rejected, start=1):
            st.error(f"{i}. {user['name']}")

    # ================== ANALYTICS ==================
    st.divider()
    st.subheader("📊 Analytics")

    df = pd.DataFrame(data)

    if not df.empty:
        col1, col2, col3 = st.columns(3)

        col1.metric("Total", len(df))
        col2.metric("Approved", len(df[df["status"]=="approved"]))
        col3.metric("Pending", len(df[df["status"]=="pending"]))

        st.bar_chart(df["status"].value_counts())

        # DOWNLOAD
        st.download_button(
            "⬇️ Download CSV",
            df.to_csv(index=False),
            "attendees.csv"
        )
