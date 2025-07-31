from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from services.supabase import store_customer
from services.encryption import encrypt
from worker import run_email_agent_task

app = FastAPI()

class CustomerConfig(BaseModel):
    email: EmailStr
    password: str
    store_name: str

@app.post("/register")
async def register_customer(config: CustomerConfig):
    try:
        encrypted = {
            "email": encrypt(config.email),
            "password": encrypt(config.password),
            "store_name": config.store_name
        }

        store_customer(encrypted)
        run_email_agent_task.delay(encrypted)

        return {"message": "Customer registered and background email agent started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

