from app.graph.state import BookingState


def route_after_triage(state: BookingState) -> str:
    if state["intent"] == "booking":
        return "booking"

    return "general"