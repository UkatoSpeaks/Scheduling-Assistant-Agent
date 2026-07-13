from sqlalchemy import Column, Date, DateTime, Integer, String
from sqlalchemy.sql import func

from app.database.database import Base


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)

    date = Column(Date, nullable=False, index=True)

    time = Column(String(20), nullable=False)

    email = Column(String(255), nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )