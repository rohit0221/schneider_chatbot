import os
import uuid
from langchain_redis import RedisChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# Load Redis URL from environment or use default
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """Retrieve chat history for a given session ID from Redis."""
    return RedisChatMessageHistory(session_id=session_id, redis_url=REDIS_URL)

def generate_session_id() -> str:
    """Generate a unique session ID that is safe for Redis."""
    return uuid.uuid4().hex  # Hex format avoids Redis syntax issues

def create_conversational_rag_chain(rag_chain, session_history_func):
    """Create a conversational RAG chain with Redis-based message history."""
    return RunnableWithMessageHistory(
        rag_chain,
        session_history_func,
        input_messages_key="input",
        history_messages_key="chat_history",  # Updated to match expected key
        output_messages_key="answer",    # Ensure it matches your response format
    )
