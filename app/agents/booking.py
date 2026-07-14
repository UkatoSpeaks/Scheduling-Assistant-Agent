import re

from langchain_core.messages import AIMessage

from app.graph.state import BookingState
from app.services.parser import extract_booking_details
from app.tools.availability import check_availability
from app.tools.notification import send_booking_notification
from app.tools.reservation import reserve_slot
from app.utils.data_parser import normalize_date
from app.utils.logger import logger


def booking_agent(state: BookingState):

    logger.info("Booking Agent Invoked")

    message = state["messages"][-1].content

    details = extract_booking_details(message)

    date = details.date or state.get("date")
    time = details.time or state.get("time")
    email = details.email or state.get("email")

    if date:
        date = normalize_date(date)

    logger.info(
        f"Extracted Details -> Date: {date}, Time: {time}, Email: {email}"
    )

    updates = {
        "date": date,
        "time": time,
        "email": email,
    }

    # -------------------------
    # Ask Date
    # -------------------------

    if not date:

        logger.warning("Date missing.")

        return {
            **updates,
            "messages": [
                AIMessage(
                    content="Sure! What date would you like to book?"
                )
            ],
        }

    # -------------------------
    # Validate Time
    # -------------------------

    if time:

        pattern = r"^([01]\d|2[0-3]):([0-5]\d)$"

        if not re.match(pattern, time):

            logger.warning("Invalid time format.")

            return {
                **updates,
                "messages": [
                    AIMessage(
                        content="Please provide the time in HH:MM format (example: 10:00)."
                    )
                ],
            }

    # -------------------------
    # Ask Time
    # -------------------------

    if not time:

        logger.info(f"Checking availability for {date}")

        availability = check_availability.invoke(
            {
                "date": date
            }
        )

        slots = availability["available_slots"]

        return {
            **updates,
            "available_slots": slots,
            "messages": [
                AIMessage(
                    content=(
                        f"Available slots on {date}:\n\n"
                        f"{', '.join(slots)}\n\n"
                        "Which time would you like?"
                    )
                )
            ],
        }

    # -------------------------
    # Ask Email
    # -------------------------

    if not email:

        logger.warning("Email missing.")

        return {
            **updates,
            "messages": [
                AIMessage(
                    content="Great! Please provide your email address."
                )
            ],
        }

    # -------------------------
    # Validate Email
    # -------------------------

    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    if not re.match(email_pattern, email):

        logger.warning("Invalid email received.")

        return {
            **updates,
            "messages": [
                AIMessage(
                    content="Please provide a valid email address."
                )
            ],
        }

    # -------------------------
    # Check Availability
    # -------------------------

    logger.info(f"Checking slot {time} on {date}")

    availability = check_availability.invoke(
        {
            "date": date
        }
    )

    slots = availability["available_slots"]

    if time not in slots:

        logger.warning(f"Requested slot {time} unavailable.")

        return {
            **updates,
            "available_slots": slots,
            "messages": [
                AIMessage(
                    content=(
                        f"Sorry, {time} is already booked.\n\n"
                        f"Available slots:\n"
                        f"{', '.join(slots)}"
                    )
                )
            ],
        }

    # -------------------------
    # Reserve Slot
    # -------------------------

    logger.info("Reserving appointment...")

    booking = reserve_slot.invoke(
        {
            "date": date,
            "time": time,
            "email": email,
        }
    )

    if not booking["success"]:

        logger.error("Reservation failed.")

        return {
            **updates,
            "messages": [
                AIMessage(
                    content=booking["message"]
                )
            ],
        }

    logger.success("Appointment reserved successfully.")

    # -------------------------
    # Notification
    # -------------------------

    logger.info("Sending webhook notification...")

    notification = send_booking_notification.invoke(
        {
            "email": email,
            "date": date,
            "time": time,
        }
    )

    if notification["success"]:
        logger.success("Webhook notification sent successfully.")
    else:
        logger.error("Webhook notification failed.")

    # -------------------------
    # Response
    # -------------------------

    confirmation = (
        f"🎉 Your appointment has been booked successfully!\n\n"
        f"📅 Date: {date}\n"
        f"🕒 Time: {time}\n"
        f"📧 Email: {email}"
    )

    if notification["success"]:
        confirmation += "\n\n✅ Confirmation notification sent."

    return {
        **updates,
        "booking_confirmed": True,
        "available_slots": [],
        "messages": [
            AIMessage(content=confirmation)
        ],
    }