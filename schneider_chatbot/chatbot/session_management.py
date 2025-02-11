import os
import uuid
from langchain_redis import RedisChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from streamlit_js_eval import get_cookie, set_cookie

# Load Redis URL from environment or use default
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """Retrieve chat history for a given session ID from Redis."""
    return RedisChatMessageHistory(session_id=session_id, redis_url=REDIS_URL)

def generate_session_id() -> str:
    """Generate or retrieve a unique session ID from cookies."""
    session_id = get_cookie("chatbot_session")  # Try retrieving session ID from cookies
    
    if not session_id:  # If no session ID exists, generate a new one
        session_id = uuid.uuid4().hex
        set_cookie("chatbot_session", session_id, 30)  # Store in cookies

    # Store session ID in Streamlit session state
    # st.session_state.session_id = session_id

    return session_id

def create_conversational_rag_chain(rag_chain, session_history_func):
    """Create a conversational RAG chain with Redis-based message history."""
    return RunnableWithMessageHistory(
        rag_chain,
        session_history_func,
        input_messages_key="input",
        history_messages_key="chat_history",  # Updated to match expected key
        output_messages_key="answer",    # Ensure it matches your response format
    )
