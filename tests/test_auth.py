# tests/test_auth.py

import streamlit as st
import pytest

from auth.auth import login_user, logout_user, get_current_user, get_user_id
from auth.billing import get_subscription_status, toggle_subscription

@pytest.fixture(autouse=True)
def clear_session_state():
    # Clear session state before each test to avoid leakage
    st.session_state.clear()
    yield
    st.session_state.clear()

def test_login_logout_flow():
    # Login demo_user
    login_user("demo_user")
    user = get_current_user()
    user_id = get_user_id()

    assert user is not None
    assert user_id == "demo_user"
    assert user["username"] == "demo_user"
    assert st.session_state["is_logged_in"] is True

    # Logout clears session keys
    logout_user()
    assert get_current_user() is None
    assert get_user_id() is None
    assert "is_logged_in" not in st.session_state

def test_invalid_login():
    # Try to login a non-existent user
    login_user("nonexistent")
    assert get_current_user() is None
    assert "is_logged_in" not in st.session_state

def test_subscription_toggle():
    login_user("demo_user")
    user_id = get_user_id()

    # Initial subscription default is True (from demo user)
    initial_status = get_subscription_status(user_id)
    assert initial_status is True

    # Toggle off
    toggle_subscription(user_id, False)
    assert get_subscription_status(user_id) is False
    assert st.session_state["user"]["subscription"] is False

    # Toggle on again
    toggle_subscription(user_id, True)
    assert get_subscription_status(user_id) is True
    assert st.session_state["user"]["subscription"] is True

def test_subscription_no_user():
    # When no user is logged in
    assert get_subscription_status(None) is False
    toggle_subscription(None, True)  # Should not error
