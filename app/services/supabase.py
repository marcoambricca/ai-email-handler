from supabase import create_client
import os
from encryption import encrypt, decrypt

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def store_customer(data):
    data_to_save = data.copy()
    data_to_save['password'] = encrypt(data['password'])
    supabase.table("customers").insert(data_to_save).execute()

def get_all_customers():
    response = supabase.table("customers").select("*").execute()
    customers = response.data
    for c in customers:
        c['password'] = decrypt(c['password'])
    return customers

def log_email(store, sender, subject, date, original_body, reply_body):
    supabase.table("email_logs").insert({
        "store": store,
        "sender": sender,
        "subject": subject,
        "date": date,
        "original_body": original_body,
        "reply_body": reply_body
    }).execute()

