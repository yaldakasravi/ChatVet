import streamlit as st
from sidebar import render_sidebar
from auth.auth import get_current_user
from session_manager import get_chat_history, append_chat_message
from chat_ui import render_chat_interface
from chatbot import Chatbot

# Initialize chatbot backend once
chatbot = Chatbot()

def main():
    st.set_page_config(page_title="ChatVet - Your Virtual Vet Assistant ", layout="wide")
    st.title("ChatVet - AI Pet Health Assistant")

    # Render sidebar from sidebar.py
    render_sidebar()

    user = get_current_user()

    if user is None:
        st.info("Please login from the sidebar to start chatting with ChatVet.")
        return

    st.subheader("Ask about your pet's symptoms or health concerns!")

    # Retrieve chat history from session state or backend
    chat_history = get_chat_history(user)

    # Render chat UI and get user input
    user_input = render_chat_interface(chat_history)

    if user_input:
        # Generate chatbot response
        with st.spinner("ChatVet is thinking..."):
            response = chatbot.ask(user_input)

        # Append messages to history and update session
        append_chat_message(user, "user", user_input)
        append_chat_message(user, "bot", response)

        # Rerun to update UI with new messages
        st.experimental_rerun()

if __name__ == "__main__":
    main()
