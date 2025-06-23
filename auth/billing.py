# auth/billing.py

import streamlit as st
from auth import get_user_id

# Simulated billing database (in-memory for demo)
_subscription_db = {}

def get_subscription_status(user_id: str) -> bool:
    """
    Check if the user has an active subscription.

    Args:
        user_id (str): The username or user ID.

    Returns:
        bool: True if subscription is active, False otherwise.
    """
    if not user_id:
        return False
    return _subscription_db.get(user_id, False)

def toggle_subscription(user_id: str, new_status: bool):
    """
    Toggle the user's subscription status.

    Args:
        user_id (str): The username or user ID.
        new_status (bool): New subscription state (True = subscribed).
    """
    if user_id:
        _subscription_db[user_id] = new_status
        # Optionally reflect this in session state
        if "user" in st.session_state:
            st.session_state["user"]["subscription"] = new_status
