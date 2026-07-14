from langgraph.graph import StateGraph, START, END

from app.agents.booking import booking_agent
from app.agents.triage import triage_agent
from app.graph.general import general_agent
from app.graph.router import route_after_triage
from app.graph.session_router import route_session
from app.graph.state import BookingState
from app.graph.checkpointer import checkpointer

builder = StateGraph(BookingState)

# Nodes
builder.add_node("triage", triage_agent)
builder.add_node("general", general_agent)
builder.add_node("booking", booking_agent)

# Entry Point
builder.add_conditional_edges(
    START,
    route_session,
    {
        "triage": "triage",
        "booking": "booking",
    },
)

# Route after triage
builder.add_conditional_edges(
    "triage",
    route_after_triage,
    {
        "general": "general",
        "booking": "booking",
    },
)

builder.add_edge("general", END)
builder.add_edge("booking", END)

graph = builder.compile(
    checkpointer=checkpointer
)