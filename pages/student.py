import streamlit as st
from utils.db import get_events, register_user
import datetime

def show():
    st.markdown("## 🎓 GateFlow - Student Portal")

    events = get_events().data

    if not events:
        st.warning("No events available")
        return

    today = datetime.date.today()
    valid_events = []

    # 🔥 SAFE FILTER (fixes your issue)
    for e in events:
        try:
            deadline = e.get("deadline")

            if deadline:
                # handle timestamp issue
                deadline_date = datetime.date.fromisoformat(deadline.split("T")[0])

                if deadline_date >= today:
                    valid_events.append(e)
            else:
                # if no deadline → still show
                valid_events.append(e)

        except:
            valid_events.append(e)

    # 🎯 SHOW EVENTS
    st.markdown("### 📢 Upcoming Events")

    if not valid_events:
        st.warning("No active events available")
        return

    for e in valid_events:
        st.markdown(f"""
        <div style="
            background:#f1f5f9;
            padding:15px;
            border-radius:12px;
            margin-bottom:10px;
        ">
        🎯 <b>{e['name']}</b><br>
        📅 {e['date']}<br>
        ⏳ Deadline: {e.get('deadline','N/A')}<br>
        📍 {e['venue']}
        </div>
        """, unsafe_allow_html=True)

    # 📝 REGISTRATION FORM
    st.markdown("### 📝 Register")

    event_map = {e["name"]: e["id"] for e in valid_events}

    name = st.text_input("👤 Name")
    email = st.text_input("📧 Email")
    event = st.selectbox("🎯 Event", list(event_map.keys()))

    if st.button("🚀 Register", use_container_width=True):
        if not name or not email:
            st.warning("Fill all fields")
            return

        res = register_user({
            "name": name,
            "email": email,
            "event_id": event_map[event],
            "status": "pending"
        })

        if res == "duplicate":
            st.warning("Already registered")
        else:
            st.success("✅ Registered! Wait for approval")
