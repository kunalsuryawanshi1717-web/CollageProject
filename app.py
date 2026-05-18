import streamlit as st
from login import login_ui, register_ui
from expense import expense_ui
from db import create_user_table, create_expense_table

view_mode = st.sidebar.radio("Choose View Mode", ["Wide", "Regular"])
if view_mode == "Wide":
    st.set_page_config(page_title="Expense Tracker", page_icon="💰", layout="wide")
else:
    st.set_page_config(page_title="Expense Tracker", page_icon="💰", layout="centered")
    
st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Create DB tables on startup
create_user_table()
create_expense_table()

# Session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# App UI
if not st.session_state.logged_in:
    st.title("💰 Personal Expense Tracker")

    menu = st.sidebar.radio("Menu", ["Login", "Register"])
    
    if menu == "Register":
        register_ui()
    else:
        login_ui()

    st.stop()

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Add Expense", "View Expenses", "Analytics"])

st.sidebar.write(f"✅ Logged in as: **{st.session_state.username}**")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

expense_ui(page)
