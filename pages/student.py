import streamlit as st
from utils.db import get_events, register_user
import datetime

def show():
    st.markdown("## 🎓 GateFlow - Student Portal")

    today = datetime.date.today()
    events = get_events().data

    if not events:
        st.warning("No events available")
        return

    # 🔥 FILTER ACTIVE EVENTS
    valid_events = []
    for e in events:
        if e.get("deadline"):
            if datetime.date.fromisoformat(e["deadline"]) >= today:
                valid_events.append(e)

    # 🔥 SHOW UPCOMING EVENTS
    st.markdown("### 📢 Upcoming Events")

    if not valid_events:
        st.warning("No active events available")
        return

    for e in valid_events:
        st.markdown(f"""
        <div class='card'>
        🎯 <b>{e['name']}</b><br>
        📅 Date: {e['date']}<br>
        ⏳ Deadline: {e['deadline']}<br>
        📍 Venue: {e['venue']}
        </div>
        """, unsafe_allow_html=True)

    # 🔥 REGISTRATION FORM
    st.markdown("### 📝 Register for Event")

    event_map = {e["name"]: e["id"] for e in valid_events}

    name = st.text_input("👤 Full Name")
    email = st.text_input("📧 Email")
    event = st.selectbox("🎯 Select Event", list(event_map.keys()))

    if st.button("🚀 Register"):
        if not name or not email:
            st.warning("Please fill all fields")
            return

        res = register_user({
            "name": name,
            "email": email,
            "event_id": event_map[event],
            "status": "pending"
        })

        if res == "duplicate":
            st.warning("Already registered!")
        else:
            st.success("✅ Registered! Wait for admin approval.")
