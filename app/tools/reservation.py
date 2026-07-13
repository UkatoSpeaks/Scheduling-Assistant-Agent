from datetime import datetime

from langchain_core.tools import tool
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.database.models import Appointment


@tool
def reserve_slot(date: str, time: str, email: str) -> dict:
    """
    Reserve an appointment slot.

    Args:
        date: Appointment date (YYYY-MM-DD)
        time: Appointment time (HH:MM)
        email: User email

    Returns:
        Dictionary containing booking result.
    """

    db: Session = SessionLocal()

    try:
        booking_date = datetime.strptime(date, "%Y-%m-%d").date()

        # Check if slot already exists
        existing = (
            db.query(Appointment)
            .filter(
                Appointment.date == booking_date,
                Appointment.time == time,
            )
            .first()
        )

        if existing:
            return {
                "success": False,
                "message": "This slot has already been booked.",
            }

        appointment = Appointment(
            date=booking_date,
            time=time,
            email=email,
        )

        db.add(appointment)
        db.commit()
        db.refresh(appointment)

        return {
            "success": True,
            "message": "Appointment booked successfully.",
            "appointment_id": appointment.id,
            "date": date,
            "time": time,
            "email": email,
        }

    except IntegrityError:
        db.rollback()

        return {
            "success": False,
            "message": "This slot has already been booked.",
        }

    except Exception as e:
        db.rollback()

        return {
            "success": False,
            "message": str(e),
        }

    finally:
        db.close()