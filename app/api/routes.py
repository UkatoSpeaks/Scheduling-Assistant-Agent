from fastapi import APIRouter
from langchain_core.messages import HumanMessage

from app.graph.workflow import graph
from app.schemas.chat import ChatRequest, ChatResponse
from app.utils.logger import logger

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    logger.info(
        f"Incoming request | Thread: {request.thread_id} | Message: {request.message}"
    )

    config = {
        "configurable": {
            "thread_id": request.thread_id
        }
    }

    result = graph.invoke(
        {
            "messages": [
                HumanMessage(content=request.message)
            ]
        },
        config=config,
    )

    response = result["messages"][-1].content

    logger.info("Response generated successfully.")

    return ChatResponse(
        response=response
    )