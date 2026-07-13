from typing import Annotated, Literal
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict

class BookingState(TypedDict):
    #conversational history
    messages:Annotated[list,add_messages]

    #routing
    intent:Literal["general","booking","unknown"]

    #booking details
    date:str|None
    time:str|None
    email:str|None

    #tool outputs
    available_slots:list[str]

    #status
    booking_confirmed:bool

    #error / clarification
    error:str|None

    #Conversation
    thread_id:str