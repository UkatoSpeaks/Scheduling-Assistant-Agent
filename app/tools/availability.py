from datetime import datetime

from langchain_core.tools import tool
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.database.models import Appointment


WORKING_HOURS = [
    "09:00",
    "10:00",
    "11:00",
    "12:00",
    "13:00",
    "14:00",
    "15:00",
    "16:00",
    "17:00",
]


@tool
def check_availability(date: str) -> dict:
    """
    Check available appointment slots for a given date.

    Args:
        date: Date in YYYY-MM-DD format.

    Returns:
        Dictionary containing available slots.
    """

    db: Session = SessionLocal()

    try:
        booking_date = datetime.strptime(date, "%Y-%m-%d").date()

        booked_slots = (
            db.query(Appointment.time)
            .filter(Appointment.date == booking_date)
            .all()
        )

        booked = {slot[0] for slot in booked_slots}

        available = [
            slot
            for slot in WORKING_HOURS
            if slot not in booked
        ]

        return {
            "date": date,
            "available_slots": available,
            "success": True,
        }

    finally:
        db.close()