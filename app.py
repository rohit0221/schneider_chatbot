import streamlit as st
from chatbotbasic import conversational_rag_chain
from schneider_chatbot.chatbot.langsmith import initialize_langsmith
from schneider_chatbot.chatbot.session_management import get_session_history, generate_session_id

initialize_langsmith()

# Streamlit App Configuration
st.set_page_config(page_title="Welcome to Schneider Electric Helpline", page_icon="./icons/page_icon.png")

# Title and Description with Branch Icon
st.title("Electric Installation Helpline")

# Display the customer's logo
logo_path = "./icons/brand.png"
try:
    st.image(logo_path, use_container_width=False, width=150)
except FileNotFoundError:
    st.warning("Logo not found. Ensure 'brand.png' is in the application directory.")

st.markdown("Ask me anything about Schneider Electric Installation process. I am here to help!")

# ✅ Ensure session_id is stored in Streamlit's session state
if "session_id" not in st.session_state:
    st.session_state.session_id = generate_session_id()

# ✅ Retrieve Redis-based chat history
history = get_session_history(st.session_state.session_id)

# ✅ Function to add message to Redis chat history
def add_message(role, content):
    if role == "user":
        history.add_user_message(content)
    else:
        history.add_ai_message(content)

# ✅ Function to generate chatbot response
def generate_response(user_input):
    try:
        response = conversational_rag_chain.invoke(
            {"input": user_input},
            config={"configurable": {"session_id": st.session_state.session_id}},
        )
        return response["answer"]
    except Exception as e:
        return f"An error occurred: {str(e)}"

# ✅ Display Chat History with Custom Icons (Loaded from Redis)
def display_chat_history():
    for message in history.messages:
        role = "user" if message.type == "human" else "assistant"
        avatar = "./icons/user.png" if role == "user" else "./icons/bot.png"
        with st.chat_message(role, avatar=avatar):
            st.markdown(message.content)

# ✅ Main chat interface
display_chat_history()

# ✅ User input section
user_input = st.chat_input("Ask me a question...")

# ✅ Process user input
if user_input:
    # Display user message
    with st.chat_message("user", avatar="./icons/user.png"):
        st.markdown(user_input)

    # Add user message to Redis history
    add_message("user", user_input)

    # Generate bot response
    with st.chat_message("assistant", avatar="./icons/bot.png"):
        with st.spinner("Generating response..."):
            bot_response = generate_response(user_input)
            st.markdown(bot_response)

    # Add bot response to Redis history
    add_message("assistant", bot_response)
