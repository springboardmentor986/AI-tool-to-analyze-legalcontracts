import streamlit as st
import time
from utils import db

def login_form():
    st.markdown("<h2 style='text-align: center;'>Welcome Back</h2>", unsafe_allow_html=True)
    with st.form("login"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login", type="primary", use_container_width=True)
        
        if submitted:
            user = db.check_user(username, password)
            if user:
                st.session_state['authenticated'] = True
                st.session_state['username'] = username
                st.session_state['plan'] = user[2] # Plan is the 3rd column
                st.success(f"Welcome, {username}!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid username or password")
    
    if st.button("Don't have an account? Sign Up"):
        st.session_state['page'] = 'signup'
        st.rerun()

def signup_form():
    st.markdown("<h2 style='text-align: center;'>Create Account</h2>", unsafe_allow_html=True)
    with st.form("signup"):
        new_user = st.text_input("Choose Username")
        new_pass = st.text_input("Choose Password", type="password")
        confirm_pass = st.text_input("Confirm Password", type="password")
        submitted = st.form_submit_button("Sign Up", type="primary", use_container_width=True)
        
        if submitted:
            if new_pass != confirm_pass:
                st.error("Passwords do not match!")
            elif len(new_pass) < 4:
                st.error("Password must be at least 4 chars")
            else:
                success = db.add_user(new_user, new_pass)
                if success:
                    st.success("Account created! Please Login.")
                    st.session_state['page'] = 'login'
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Username already taken.")

    if st.button("Already have an account? Login"):
        st.session_state['page'] = 'login'
        st.rerun()