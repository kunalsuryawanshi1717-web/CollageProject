import streamlit as st
from db import register_user, get_user

def login_ui():
    st.subheader("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = get_user(username, password)

        if user:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("✅ Login Successful!")
            st.rerun()
        else:
            st.error("❌ Invalid username or password")

def register_ui():
    st.subheader("📝 Create New Account")

    username = st.text_input("Create Username")
    password = st.text_input("Create Password", type="password")

    if st.button("Register"):
        if username.strip() == "" or password.strip() == "":
            st.error("⚠ Username or password cannot be empty")
            return
        
        success = register_user(username, password)
        
        if success:
            st.success("✅ Registration Successful! Please login.")
            st.session_state.logged_in = False
        else:
            st.error("⚠ Username already exists! Try another")

