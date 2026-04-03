import streamlit as st
from utils.db import *
from utils.auth import student_login
import datetime

def show():

    # 🔐 LOGIN (OPTIONAL OTP)
    if "student" not in st.session_state:
        student_login()
        return

    st.markdown("## 🎓 Student Portal")

    events = get_events().data

    if not events:
        st.warning("No events available")
        return

    today = datetime.date.today()
    valid_events = []

    # ✅ FIXED DEADLINE FILTER
    for e in events:
        try:
            deadline = e.get("deadline")
            if deadline:
                d = datetime.date.fromisoformat(deadline.split("T")[0])
                if d >= today:
                    valid_events.append(e)
            else:
                valid_events.append(e)
        except:
            valid_events.append(e)

    st.markdown("### 📢 Upcoming Events")

    event_map = {}

    for e in valid_events:
        st.markdown(f"""
        <div class="card">
        🎯 <b>{e['name']}</b><br>
        📅 {e['date']}<br>
        📍 {e['venue']}<br>
        ⏳ Deadline: {e.get('deadline','N/A')}
        </div>
        """, unsafe_allow_html=True)

        if e.get("poster"):
            st.image(e["poster"], width=250)

        event_map[e["name"]] = e["id"]

    st.divider()

    # 📝 REGISTRATION FORM
    st.markdown("### 📝 Register")

    name = st.text_input("👤 Name")
    mobile = st.text_input("📱 Mobile")

    # ✅ EMAIL FIX (VISIBLE + AUTO FILL)
    email_default = st.session_state.get("student", "")
    email = st.text_input("📧 Email", value=email_default)

    course = st.selectbox("🎓 Course", ["BBA","BCA"])
    section = st.selectbox("🏫 Section", list("ABCDEFG"))
    year = st.selectbox("📘 Year", ["1st","2nd","3rd"])

    event = st.selectbox("🎯 Event", list(event_map.keys()))

    if st.button("Register", use_container_width=True):

        # ✅ BASIC VALIDATION
        if not name or not mobile or not email:
            st.warning("Please fill all fields")
            return

        all_regs = get_all().data
        event_id = event_map[event]

        # 🔥 FIXED CAPACITY CHECK
        count = len([r for r in all_regs if r["event_id"] == event_id])
        selected_event = [e for e in valid_events if e["id"] == event_id][0]

        capacity = selected_event.get("capacity")

        if capacity is None:
            capacity = 9999  # unlimited fallback

        if count >= int(capacity):
            st.error("🚫 Event Full")
            return

        # ✅ REGISTER USER
        res = register_user({
            "name": name,
            "mobile": mobile,
            "email": email,
            "course": course,
            "section": section,
            "year": year,
            "event_id": event_id,
            "status": "pending"
        })

        if res == "duplicate":
            st.warning("Already registered")
        else:
            st.success("✅ Registered! Wait for approval")
