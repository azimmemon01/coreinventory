import streamlit as st
from database import *
import random
import products, deliveries, dashboard, stock, transfers,history


def generate_otp():
    return random.randint(1000, 9999)


connect = create_connection()


def initialize_database(conn):

    create_table(conn)
    create_products_table(conn)
    create_deliveries_table(conn)
    create_transfers_table(conn)
    create_stock_transactions_table(conn)


initialize_database(connect)

st.set_page_config(page_title="Inventory Management System")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "allow_reset" not in st.session_state:
    st.session_state.allow_reset = False

if "otp" not in st.session_state:
    st.session_state.otp = None

if "reset_user" not in st.session_state:
    st.session_state.reset_user = ""


if not st.session_state.logged_in:

    st.title("Login Authentication System")

    menu = st.sidebar.selectbox("Menu", ["Login", "Create Account", "Forgot Password"])
    if menu == "Login":

        st.subheader("Login Section")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            result = login(connect, username, password)

            if result:
                st.session_state.logged_in = True
                st.session_state.current_user = username
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid username or password")

    elif menu == "Create Account":

        st.subheader("Create New Account")

        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type="password")

        if st.button("Signup"):
            try:
                add_user(connect, new_user, new_password)
                st.success("Account created successfully")
            except:
                st.error("Username already exists")

    elif menu == "Forgot Password":

        st.subheader("Reset Password")

        username = st.text_input("Enter your username")

        if st.button("Generate OTP"):
            otp = generate_otp()
            st.session_state.otp = otp
            st.session_state.reset_user = username
            st.session_state.allow_reset = False
            st.info(f"Demo OTP: {otp}")

        otp_input = st.text_input("Enter OTP")

        if st.button("Verify OTP"):
            if st.session_state.otp is not None and otp_input != "":
                if int(otp_input) == st.session_state.otp:
                    st.success("OTP verified")
                    st.session_state.allow_reset = True
                else:
                    st.error("Invalid OTP")
            else:
                st.warning("Generate OTP first")

        if st.session_state.allow_reset:
            new_password = st.text_input("New Password", type="password")

            if st.button("Update Password"):
                update_password(connect, st.session_state.reset_user, new_password)
                st.success("Password updated successfully")
                st.session_state.allow_reset = False
                st.session_state.otp = None
                st.session_state.reset_user = ""


else:
    st.title("Inventory Management System")

    st.sidebar.success(f"Welcome {st.session_state.current_user}")

    page = st.sidebar.selectbox(
        "IMS Menu",
        ["Dashboard", "Products", "Stock Management", "Deliveries", "Transfers","Stock History"],
    )

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.current_user = ""
        st.rerun()

    if page == "Dashboard":
        dashboard.show(connect)
    elif page == "Products":
        products.show(connect)

    elif page == "Stock Management":
        stock.show(connect)
    elif page == "Deliveries":
        deliveries.show(connect)

    elif page == "Transfers":
        transfers.show(connect)
    elif page == "Stock History":
        history.show(connect)
