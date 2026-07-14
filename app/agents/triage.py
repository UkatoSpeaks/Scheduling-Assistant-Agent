from langchain_core.messages import AIMessage

from app.graph.state import BookingState
from app.utils.logger import logger

BOOKING_KEYWORDS = [
    "book",
    "booking",
    "schedule",
    "appointment",
    "meeting",
    "reserve",
    "slot",
]


def triage_agent(state: BookingState):
    """
    Triage Agent

    Decides whether the user wants to:
    - Book an appointment
    - Ask a general question
    """

    logger.info("Triage Agent Invoked")

    user_message = state["messages"][-1].content.lower()

    logger.info(f"Incoming message: {user_message}")

    booking_intent = any(
        keyword in user_message
        for keyword in BOOKING_KEYWORDS
    )

    if booking_intent:
        logger.success("Booking intent detected. Routing to Booking Agent.")

        return {
            "intent": "booking",
            "messages": [
                AIMessage(content="Routing to Booking Agent...")
            ]
        }

    logger.success("General intent detected. Routing to General Agent.")

    return {
        "intent": "general",
        "messages": [
            AIMessage(content="Routing to General Agent...")
        ]
    }