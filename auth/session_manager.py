# auth/session_manager.py

import streamlit as st
from auth.auth import get_user_id
from typing import List, Dict

def _get_session_key(user_id: str) -> str:
    """Internal helper to create a per-user session key for chat history."""
    return f"chat_history_{user_id}"

def get_chat_history(user_id: str) -> List[Dict[str, str]]:
    """
    Retrieve the current chat history for the user.

    Args:
        user_id (str): The user ID or username.

    Returns:
        List[Dict]: A list of messages with 'role' and 'content'.
    """
    if not user_id:
        return []

    session_key = _get_session_key(user_id)

    if session_key not in st.session_state:
        st.session_state[session_key] = []

    return st.session_state[session_key]

def append_chat_message(user_id: str, role: str, message: str):
    """
    Append a new message to the chat history.

    Args:
        user_id (str): The user ID.
        role (str): Either "user" or "bot".
        message (str): The message content.
    """
    if role not in ["user", "bot"]:
        raise ValueError("Role must be either 'user' or 'bot'.")

    history = get_chat_history(user_id)
    history.append({"role": role, "content": message})

def clear_chat_history():
    """
    Clears all chat history for the current user (from session).
    """
    user_id = get_user_id()
    if user_id:
        session_key = _get_session_key(user_id)
        if session_key in st.session_state:
            del st.session_state[session_key]
