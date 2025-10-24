from pydantic import BaseModel, Field
from typing import Optional, List

# ----------- Схемы для услуг (рестораны, сауны и т.д.) -------------
class ServiceBase(BaseModel):
    name: str
    description: str
    address: str
    phone: str


class Service(ServiceBase):
    id: int

    class Config:
        orm_mode = True


# ----------- Схемы для бронирования -------------
class BookingBase(BaseModel):
    service_id: int
    user_name: str
    user_phone: str
    date: str  # позже можно заменить на datetime


class Booking(BookingBase):
    id: int

    class Config:
        orm_mode = True


# ----------- Схема для обратной связи (Tilda webhook) -------------
class ContactMessage(BaseModel):
    name: str = Field(..., alias="Name")
    email: str = Field(..., alias="Email")
    message: str = Field(..., alias="Textarea")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True  # позволяет обращаться и по alias, и по внутренним именам
