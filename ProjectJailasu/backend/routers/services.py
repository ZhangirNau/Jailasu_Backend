from fastapi import APIRouter
from ..schemas import Service

router = APIRouter(
    prefix="/services",
    tags=["Services"]
)

# Временный список заведений (фейковые данные)
fake_services = [
    Service(id=1, name="Сауна Жайласы", description="Комфортная сауна с VIP комнатами.", address="г. Астана, ул. Абая 10", phone="+7 777 123 45 67"),
    Service(id=2, name="Ресторан Nomad", description="Национальная кухня, банкетный зал.", address="г. Алматы, пр. Достык 25", phone="+7 701 888 77 66"),
    Service(id=3, name="Салон красоты Shine", description="SPA, массаж, косметология.", address="г. Шымкент, ул. Байтурсынова 7", phone="+7 705 555 33 22"),
]

@router.get("/", response_model=list[Service])
def get_services():
    return fake_services

@router.get("/{service_id}", response_model=Service)
def get_service(service_id: int):
    for item in fake_services:
        if item.id == service_id:
            return item
    return {"error": "Service not found"}
