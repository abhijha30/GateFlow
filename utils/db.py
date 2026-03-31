from supabase import create_client
import os

supabase = create_client(
    os.getenv("https://ahaiguauzayaslaazokj.supabase.co")
    os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFoYWlndWF1emF5YXNsYWF6b2tqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQ5MjQ2OTYsImV4cCI6MjA5MDUwMDY5Nn0.K6WMZeR-TjAoq0zWfTj-5Gi2Xn-zqjmiC23fz6yk-cg")
)

def get_events():
    return supabase.table("events").select("*").execute()

def create_event(data):
    return supabase.table("events").insert(data).execute()

def register_user(data):
    check = supabase.table("registrations") \
        .select("*") \
        .eq("email", data["email"]) \
        .eq("event_id", data["event_id"]) \
        .execute()

    if check.data:
        return "duplicate"

    return supabase.table("registrations").insert(data).execute()

def get_pending():
    return supabase.table("registrations").select("*").eq("status", "pending").execute()

def update_status(id, status, qr):
    return supabase.table("registrations").update({
        "status": status,
        "qr_code": qr
    }).eq("id", id).execute()

def get_all():
    return supabase.table("registrations").select("*").execute()
