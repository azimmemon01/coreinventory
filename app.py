import streamlit as st
from database import *
import random
def generate_otp():
    return random.randint(1000,9999)

connect=create_connection()
create_table(connect)
st.set_page_config(page_title="Login System")

st.title("Login Authentication System")

menu = st.sidebar.selectbox("Menu", ["Login", "Create Account","forget password"])

if menu == "Login":
    
    st.subheader("Login Section")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        result=login(connect,username,password)
        if result:
            st.success("Login successful")
        else:
            st.error("Invalid username or password")



if menu == "Create Account":

    st.subheader("Create New Account")

    new_user = st.text_input("Username")
    new_password = st.text_input("Password", type="password")

    if st.button("Signup"):
        add_user(connect,new_user,new_password)
        st.success("Account created (demo)")

if menu == "forget password":

    st.subheader("Reset Password")

    username = st.text_input("Enter your username")

    if st.button("Generate OTP"):

        otp = generate_otp()
        st.session_state.otp = otp
        st.session_state.reset_user = username

        st.info(f"Demo OTP: {otp}")
    otp_input = st.text_input("Enter OTP")

    if st.button("Verify OTP"):

     if int(otp_input) == st.session_state.otp:
        st.success("OTP verified")
        st.session_state.allow_reset = True
     else:
        st.error("Invalid OTP")
    if st.session_state.get("allow_reset"):

     new_password = st.text_input("New Password", type="password")

    if st.button("Update Password"):

        update_password(connect, st.session_state.reset_user, new_password)

        st.success("Password updated successfully")