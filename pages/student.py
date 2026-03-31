import streamlit as st
from utils.db import get_events, register_user

def show():
    st.markdown("### 🎓 Student Registration")

    events = get_events().data
    if not events:
        st.warning("No events available")
        return

    event_map = {e["name"]: e["id"] for e in events}

    name = st.text_input("👤 Full Name")
    email = st.text_input("📧 Email")
    event = st.selectbox("🎯 Select Event", list(event_map.keys()))

    if st.button("🚀 Register"):
        res = register_user({
            "name": name,
            "email": email,
            "event_id": event_map[event],
            "status": "pending"
        })

        if res == "duplicate":
            st.warning("Already registered!")
        else:
            st.success("Registered! Wait for admin approval.")
