# contact.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr

router = APIRouter()

# Модель данных
class ContactMessage(BaseModel):
    name: str
    email: EmailStr
    message: str

# Временное хранилище (как база)
contact_messages = []

@router.post("/contact")
async def send_contact_message(data: ContactMessage):
    contact_messages.append({
        "name": data.name,
        "email": data.email,
        "message": data.message
    })
    return {"success": True, "message": "Сообщение успешно отправлено"}
