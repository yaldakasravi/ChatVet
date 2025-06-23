import streamlit as st
from auth.auth import login_user, logout_user, get_current_user
from auth.billing import get_subscription_status, toggle_subscription
from session_manager import clear_chat_history

def render_sidebar():
    st.sidebar.header("User Account")

    user = get_current_user()

    if user is None:
        st.sidebar.write("You are not logged in.")
        if st.sidebar.button("Login (Demo)"):
            login_user("demo_user")  # simple demo login
            st.experimental_rerun()
    else:
        st.sidebar.write(f"Logged in as: **{user}**")
        if st.sidebar.button("Logout"):
            logout_user()
            clear_chat_history()
            st.experimental_rerun()

        # Subscription toggle
        sub_status = get_subscription_status(user)
        new_status = st.sidebar.checkbox("Subscription Active", value=sub_status)
        if new_status != sub_status:
            toggle_subscription(user, new_status)
            st.experimental_rerun()
