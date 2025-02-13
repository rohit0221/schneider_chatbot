import streamlit as st
import yaml
from yaml.loader import SafeLoader
from chatbotbasic import conversational_rag_chain
from schneider_chatbot.chatbot.langsmith import initialize_langsmith
from schneider_chatbot.chatbot.session_management import get_session_history

# ✅ Set page config as the first command
st.set_page_config(page_title="Welcome to Schneider Electric Helpline", page_icon="./icons/page_icon.png")

initialize_langsmith()

# ✅ Debug: Load authentication config from YAML
try:
    with open("auth_config.yaml") as file:
        config = yaml.safe_load(file)
    st.write("✅ YAML config loaded successfully.")
    print("✅ YAML config loaded successfully.")
except Exception as e:
    st.error(f"❌ Error loading YAML: {e}")
    print(f"❌ Error loading YAML: {e}")

# ✅ Custom authentication function (No hashing)
def authenticate(username, password):
    print(f"🔍 Attempting login for username: {username}")  # Debug
    user_data = config.get("credentials", {}).get("usernames", {}).get(username)

    if user_data:
        stored_password = user_data["password"]  # ✅ Plaintext password
        print(f"✅ Found user: {user_data}")  # Debug
        print(f"🔍 Comparing: Entered: {password} | Stored: {stored_password}")  # Debug

        if password == stored_password:
            print(f"✅ Authentication successful for {username}")  # Debug
            return user_data["name"], True  # ✅ Authentication success
        else:
            print("❌ Password mismatch!")  # Debug
    else:
        print("❌ Username not found!")  # Debug

    return None, False  # ❌ Authentication failed

# ✅ Login UI
st.sidebar.header("Login")
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

if st.sidebar.button("Login"):
    name, authenticated = authenticate(username, password)
    
    if authenticated:
        st.sidebar.success(f"✅ Welcome, {name}!")
        st.session_state["authenticated"] = True
        st.session_state["username"] = username  # Store session info
        st.session_state["name"] = name
    else:
        st.sidebar.error("❌ Incorrect username or password.")

# ✅ Logout Button
if st.session_state.get("authenticated"):
    if st.sidebar.button("Logout"):
        st.session_state["authenticated"] = False
        st.experimental_rerun()

# ✅ Only Show Chatbot If Authenticated
if st.session_state.get("authenticated"):
    st.write(f"✅ Authenticated as {st.session_state['name']} ({st.session_state['username']})")

    st.title("Electric Installation Helpline")

    # ✅ Debug: Display the Customer’s Logo
    logo_path = "./icons/brand.png"
    try:
        st.image(logo_path, use_container_width=False, width=150)
        print("✅ Logo displayed successfully.")
    except FileNotFoundError:
        st.warning("⚠️ Logo not found. Ensure 'brand.png' is in the application directory.")
        print("⚠️ Logo not found.")

    st.markdown("Ask me anything about Schneider Electric Installation process. I am here to help!")

    # ✅ Debug: Session ID Management
    if "session_id" not in st.session_state:
        st.session_state.session_id = st.session_state["username"]  # Each user gets their own session
        print(f"🔍 Session initialized with ID: {st.session_state.session_id}")

    # ✅ Debug: Retrieve Redis-based Chat History
    history = get_session_history(st.session_state.session_id)

    def add_message(role, content):
        if role == "user":
            history.add_user_message(content)
        else:
            history.add_ai_message(content)
        print(f"✅ Message added: {role} -> {content}")

    def generate_response(user_input):
        try:
            print(f"🔍 Generating response for: {user_input}")
            response = conversational_rag_chain.invoke(
                {"input": user_input},
                config={"configurable": {"session_id": st.session_state.session_id}},
            )
            print(f"✅ Response generated: {response['answer']}")
            return response["answer"]
        except Exception as e:
            st.error(f"❌ Error in response generation: {str(e)}")
            print(f"❌ Error in response generation: {str(e)}")
            return f"An error occurred: {str(e)}"

    def display_chat_history():
        for message in history.messages:
            role = "user" if message.type == "human" else "assistant"
            avatar = "./icons/user.png" if role == "user" else "./icons/bot.png"
            with st.chat_message(role, avatar=avatar):
                st.markdown(message.content)
        print("✅ Chat history displayed.")

    display_chat_history()

    user_input = st.chat_input("Ask me a question...")

    if user_input:
        with st.chat_message("user", avatar="./icons/user.png"):
            st.markdown(user_input)
        add_message("user", user_input)

        with st.chat_message("assistant", avatar="./icons/bot.png"):
            with st.spinner("Generating response..."):
                bot_response = generate_response(user_input)
                st.markdown(bot_response)

        add_message("assistant", bot_response)
