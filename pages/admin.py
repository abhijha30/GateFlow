import streamlit as st
from utils.auth import admin_login
from utils.db import *
from utils.qr import generate_qr
from utils.mail import send_qr
import uuid
import pandas as pd
import base64
import os

def show():

    # 🔐 LOGIN
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
    capacity = st.number_input("Capacity", min_value=1, step=1)

    poster = st.file_uploader("Upload Poster", type=["png","jpg","jpeg"])

    if st.button("Create Event", use_container_width=True):

        if not name or not venue:
            st.warning("Please fill all fields")
            return

        poster_data = None
        if poster:
            poster_data = base64.b64encode(poster.read()).decode()

        create_event({
            "name": name,
            "date": str(date),
            "deadline": str(deadline),
            "venue": venue,
            "capacity": int(capacity),
            "poster": poster_data
        })

        st.success("✅ Event Created")
        st.rerun()

    st.divider()

    # ================== EVENTS LIST ==================
    st.subheader("📢 All Events")

    events = get_events().data or []

    if not events:
        st.info("No events created")

    for i, e in enumerate(events, start=1):

        col1, col2 = st.columns([4,1])

        with col1:
            st.markdown(f"""
            <div class="card">
            <b>{i}. 🎯 {e['name']}</b><br>
            📅 {e['date']}<br>
            ⏳ {e.get('deadline','N/A')}<br>
            📍 {e['venue']}<br>
            👥 Capacity: {e.get('capacity','∞')}
            </div>
            """, unsafe_allow_html=True)

        with col2:
            if st.button("🗑 Delete", key=f"delete_{e['id']}"):
                delete_event(e["id"])
                st.success("✅ Event Deleted")
                st.rerun()

    st.divider()

    # ================== REGISTRATIONS ==================
    data = get_all().data or []

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

            # ✅ APPROVE
            if col1.button("Approve", key=f"approve_{user['id']}"):

                qr_id = str(uuid.uuid4())
                file_path = f"{qr_id}.png"

                # ✅ Generate QR
                generate_qr(qr_id, file_path)

                # ✅ Update DB
                update_status(user["id"], "approved", qr_id)

                # ✅ Send Mail
                success = send_qr(user["email"], file_path)

                if success:
                    st.success("✅ Approved & QR sent")
                else:
                    st.warning("⚠ Approved but email failed")

                # 🧹 Delete temp QR file
                if os.path.exists(file_path):
                    os.remove(file_path)

                st.rerun()

            # ❌ REJECT
            if col2.button("Reject", key=f"reject_{user['id']}"):
                update_status(user["id"], "rejected", "")
                st.error("❌ Rejected")
                st.rerun()

            st.divider()

    # 🔹 APPROVED
    with tab2:
        approved = [u for u in data if u["status"] == "approved"]

        if not approved:
            st.info("No approved users")

        for i, user in enumerate(approved, start=1):
            st.success(f"{i}. {user['name']} | {user.get('course','')}")

    # 🔹 REJECTED
    with tab3:
        rejected = [u for u in data if u["status"] == "rejected"]

        if not rejected:
            st.info("No rejected users")

        for i, user in enumerate(rejected, start=1):
            st.error(f"{i}. {user['name']}")

    # ================== ANALYTICS ==================
    st.divider()
    st.subheader("📊 Analytics")

    if not data:
        st.info("No data available")
        return

    df = pd.DataFrame(data)

    col1, col2, col3 = st.columns(3)

    col1.metric("Total", len(df))
    col2.metric("Approved", len(df[df["status"]=="approved"]))
    col3.metric("Pending", len(df[df["status"]=="pending"]))

    st.bar_chart(df["status"].value_counts())

    # 🔍 SEARCH EVENT
search_event = st.text_input("🔍 Search Event by Name")

filtered_events = []

for e in events:
    if search_event.lower() in e["name"].lower():
        filtered_events.append(e)

if not filtered_events:
    st.info("No events found")

    # ✅ DOWNLOAD FIX (UNIQUE KEY)
    st.download_button(
        "⬇️ Download Attendee List",
        df.to_csv(index=False),
        "attendees.csv",
        key="download_attendees_unique"
    )
