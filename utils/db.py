from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("https://ahaiguauzayaslaazokj.supabase.co")
SUPABASE_KEY = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFoYWlndWF1emF5YXNsYWF6b2tqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQ5MjQ2OTYsImV4cCI6MjA5MDUwMDY5Nn0.K6WMZeR-TjAoq0zWfTj-5Gi2Xn-zqjmiC23fz6yk-cg")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise Exception("Supabase credentials missing!")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 🔥 DEBUG PRINT
print("Connected to Supabase")

def create_event(data):
    res = supabase.table("events").insert(data).execute()
    print("CREATE EVENT:", res)
    return res

def get_events():
    res = supabase.table("events").select("*").execute()
    print("FETCH EVENTS:", res)
    return res

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
