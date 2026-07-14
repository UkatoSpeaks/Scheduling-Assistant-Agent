from langchain_core.messages import AIMessage
from app.graph.state import BookingState
from app.services.llm import llm

SYSTEM_PROMPT="""
You are a helpful AI assistant.

Answer normally.

Do NOT schedule appointments.
"""

def general_agent(state:BookingState):
    user_message=state["messages"][-1].content

    response=llm.invoke(
        [
            ("system",SYSTEM_PROMPT),
            ("human",user_message),
        ]
    )

    return {
        "messages":[
            AIMessage(content=response.content)
        ]
    }