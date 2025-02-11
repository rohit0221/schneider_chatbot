from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
import uuid

store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

def generate_session_id() -> str:
    return str(uuid.uuid4())

def create_conversational_rag_chain(rag_chain, session_history_func):
    return RunnableWithMessageHistory(
        rag_chain,
        session_history_func,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    )
