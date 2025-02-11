import streamlit as st
from chatbotbasic import conversational_rag_chain, session_id

from schneider_chatbot.chatbot.langsmith import initialize_langsmith

initialize_langsmith()

# Initialize session state for chat history if not exists
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Streamlit App Configuration
st.set_page_config(page_title="Welcome to Schneider Electric Helpline", page_icon="./icons/page_icon.png")

# Title and Description with Branch Icon
st.title("Electric installation Helpline")
# Display the customer's logo
logo_path = "./icons/brand.png"  # Replace with the path to the logo file
try:
    st.image(logo_path, use_container_width=False, width=150)  # Adjust width as needed
except FileNotFoundError:
    st.warning("Logo not found. Please ensure 'brand.png' is in the application directory.")
    
st.markdown("Ask me anything about Schneider Electric Installation process . I am here to help!")

# Function to add message to chat history
def add_message(role, content):
    st.session_state.chat_history.append({"role": role, "content": content})

# Function to generate response
def generate_response(user_input):
    try:
        response = conversational_rag_chain.invoke(
            {"input": user_input},
            config={"configurable": {"session_id": session_id}},
        )
        return response["answer"]
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Display Chat History with Custom Icons
def display_chat_history():
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            with st.chat_message(message["role"], avatar="./icons/user.png"):
                st.markdown(message["content"])
        else:
            with st.chat_message(message["role"], avatar="./icons/bot.png"):
                st.markdown(message["content"])

# Main chat interface
display_chat_history()

# User input section
user_input = st.chat_input("Ask me a question...")

# Process user input
if user_input:
    # Display user message with custom icon
    with st.chat_message("user", avatar="./icons/user.png"):
        st.markdown(user_input)
    
    # Add user message to history
    add_message("user", user_input)
    
    # Generate and display bot response with custom icon
    with st.chat_message("assistant", avatar="./icons/bot.png"):
        with st.spinner("Generating response..."):
            bot_response = generate_response(user_input)
            st.markdown(bot_response)
    
    # Add bot response to history
    add_message("assistant", bot_response)