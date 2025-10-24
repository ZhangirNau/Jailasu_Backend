from fastapi import APIRouter
from ..schemas import Booking, BookingBase

router = APIRouter(
    prefix="/booking",
    tags=["Booking"]
)

# Временное хранилище броней (фейковые данные)
fake_bookings = []

@router.post("/", response_model=Booking)
def create_booking(booking: BookingBase):
    new_id = len(fake_bookings) + 1
    new_booking = Booking(
        id=new_id,
        service_id=booking.service_id,
        user_name=booking.user_name,
        user_phone=booking.user_phone,
        date=booking.date
    )
    fake_bookings.append(new_booking)
    return new_booking

@router.get("/", response_model=list[Booking])
def get_all_bookings():
    return fake_bookings
