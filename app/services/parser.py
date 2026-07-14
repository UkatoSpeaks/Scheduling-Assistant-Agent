from typing import Optional

from pydantic import BaseModel, Field

from app.services.llm import llm


class BookingDetails(BaseModel):
    date: Optional[str] = Field(
        default=None,
        description="Booking date mentioned by the user."
    )

    time: Optional[str] = Field(
        default=None,
        description="Booking time mentioned by the user."
    )

    email: Optional[str] = Field(
        default=None,
        description="Email address mentioned by the user."
    )


structured_llm = llm.with_structured_output(BookingDetails)


SYSTEM_PROMPT = """
You extract booking information from user messages.

Extract ONLY:

- date
- time
- email

Rules:

- If something is missing return null.
- Do not invent values.
- Do not explain anything.
"""


def extract_booking_details(message: str) -> BookingDetails:
    """
    Extract booking details from a user's message.
    """

    return structured_llm.invoke(
        [
            ("system", SYSTEM_PROMPT),
            ("human", message),
        ]
    )