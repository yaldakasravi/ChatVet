# app/main.py

import streamlit as st
from auth.auth import login_user, logout_user, get_current_user
from auth.billing import get_subscription_status, toggle_subscription
from session_manager import get_chat_history, append_chat_message, clear_chat_history
from chat_ui import render_chat_interface
from chatbot import Chatbot

# Initialize chatbot backend once
chatbot = Chatbot()

def main():
    st.set_page_config(page_title="ChatVet - Your Virtual Vet Assistant ", layout="wide")
    st.title("ChatVet - AI Pet Health Assistant")

    # --- Sidebar ---
    with st.sidebar:
        st.header("User Account")
        user = get_current_user()

        if user is None:
            # Show login form
            if st.button("Login (Demo)"):
                login_user("demo_user")
                st.experimental_rerun()
        else:
            st.write(f"Logged in as: **{user}**")
            if st.button("Logout"):
                logout_user()
                clear_chat_history()
                st.experimental_rerun()

            # Subscription toggle (simulate Stripe billing)
            sub_status = get_subscription_status(user)
            new_status = st.checkbox("Subscription Active", value=sub_status)
            if new_status != sub_status:
                toggle_subscription(user, new_status)
                st.experimental_rerun()

    # --- Main Chat Interface ---
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
