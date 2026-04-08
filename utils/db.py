import streamlit as st
from supabase import create_client

# 🔥 DIRECT CONNECTION
SUPABASE_URL = "https://ahaiguauzayaslaazokj.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFoYWlndWF1emF5YXNsYWF6b2tqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQ5MjQ2OTYsImV4cCI6MjA5MDUwMDY5Nn0.K6WMZeR-TjAoq0zWfTj-5Gi2Xn-zqjmiC23fz6yk-cg"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# ================== EVENTS ==================

def create_event(data):
    return supabase.table("events").insert(data).execute()


# ✅ CACHE EVENTS (BIG PERFORMANCE BOOST)
@st.cache_data(ttl=60)
def get_events():
    return supabase.table("events").select("*").order("id", desc=True).execute()


# ================== REGISTRATION ==================

def register_user(data):
    # 🔁 prevent duplicate
    check = supabase.table("registrations") \
        .select("*") \
        .eq("email", data["email"]) \
        .eq("event_id", data["event_id"]) \
        .execute()

    if check.data:
        return "duplicate"

    # ❗ clear cache after insert
    get_all.clear()
    get_events.clear()

    return supabase.table("registrations").insert(data).execute()


@st.cache_data(ttl=60)
def get_pending():
    return supabase.table("registrations") \
        .select("*") \
        .eq("status", "pending") \
        .execute()


def update_status(id, status, qr):
    res = supabase.table("registrations").update({
        "status": status,
        "qr_code": qr
    }).eq("id", id).execute()

    # ❗ clear cache after update
    get_all.clear()
    get_pending.clear()

    return res


# ✅ CACHE ALL REGISTRATIONS
@st.cache_data(ttl=60)
def get_all():
    return supabase.table("registrations").select("*").execute()
#Delete Event
def delete_event(event_id):
    return supabase.table("events").delete().eq("id", event_id).execute()

