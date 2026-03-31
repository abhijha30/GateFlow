from supabase import create_client
import os

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
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
