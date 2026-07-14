import sqlite3

from langgraph.checkpoint.sqlite import SqliteSaver

from app.config import settings

# Create a persistent SQLite connection
connection = sqlite3.connect(
    settings.CHECKPOINT_DB,
    check_same_thread=False,
)

# Create the LangGraph checkpointer
checkpointer = SqliteSaver(connection)