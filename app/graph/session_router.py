from app.graph.state import BookingState


def route_session(state: BookingState) -> str:
    """
    If the user is already in an active booking conversation,
    continue directly with the Booking Agent.

    Otherwise, send the request to the Triage Agent.
    """

    if state.get("intent") == "booking":
        return "booking"

    return "triage"