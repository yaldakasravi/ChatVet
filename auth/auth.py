# auth/auth.py

import streamlit as st

# Simulated user database (for prototype)
DEMO_USERS = {
    "demo_user": {
        "username": "demo_user",
        "email": "demo@chatvet.ai",
        "subscription": True  # default subscription status
    }
}

def login_user(username: str):
    """
    Log in a user by saving their info in session state.

    Args:
        username (str): The username to log in (must exist in DEMO_USERS)
    """
    user = DEMO_USERS.get(username)
    if user:
        st.session_state["user"] = user
        st.session_state["username"] = username
        st.session_state["is_logged_in"] = True
    else:
        st.error("User does not exist.")

def logout_user():
    """Log out the current user by clearing session keys."""
    for key in ["user", "username", "is_logged_in", "subscription"]:
        if key in st.session_state:
            del st.session_state[key]

def get_current_user():
    """
    Returns:
        dict or None: The logged-in user's info, or None if not logged in.
    """
    return st.session_state.get("user", None)

def get_user_id():
    """
    Returns:
        str or None: The username (used as user ID), or None if not logged in.
    """
    return st.session_state.get("username", None)
