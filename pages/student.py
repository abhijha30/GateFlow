import streamlit as st
from utils.db import *
from utils.auth import student_login
import datetime
import base64

def show():

    # 🔐 LOGIN
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

    # ✅ DEADLINE FILTER FIXED
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

        # ✅ FIXED IMAGE ERROR (BASE64 SUPPORT)
        if e.get("poster"):
            try:
                image_bytes = base64.b64decode(e["poster"])
                st.image(image_bytes, width=250)
            except:
                st.warning("⚠️ Poster not supported")

        event_map[e["name"]] = e["id"]

    st.divider()

    # ================= FORM =================
    st.markdown("### 📝 Register")

    name = st.text_input("👤 Name")
    mobile = st.text_input("📱 Mobile")

    # ✅ EMAIL FIX (VISIBLE)
    email_default = st.session_state.get("student", "")
    email = st.text_input("📧 Email", value=email_default)

    course = st.selectbox("🎓 Course", ["BBA","BCA"])
    section = st.selectbox("🏫 Section", list("ABCDEFG"))
    year = st.selectbox("📘 Year", ["1st","2nd","3rd"])

    if not event_map:
        st.warning("No active events")
        return

    event = st.selectbox("🎯 Event", list(event_map.keys()))

    # ================= REGISTER =================
    if st.button("Register", use_container_width=True):

        # ✅ VALIDATION
        if not name or not mobile or not email:
            st.warning("Please fill all fields")
            return

        try:
            all_regs = get_all().data or []
        except:
            st.error("⚠️ Database connection slow / failed")
            return

        event_id = event_map[event]

        # ✅ SAFE CAPACITY CHECK
        count = len([r for r in all_regs if r.get("event_id") == event_id])

        selected_event = next((e for e in valid_events if e["id"] == event_id), None)

        capacity = 9999
        if selected_event:
            try:
                capacity = int(selected_event.get("capacity") or 9999)
            except:
                capacity = 9999

        if count >= capacity:
            st.error("🚫 Event Full")
            return

        # ✅ REGISTER
        try:
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

        except Exception as e:
            st.error("⚠️ Registration failed (Slow DB / Network)")
