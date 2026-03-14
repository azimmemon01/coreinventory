import streamlit as st
import pandas as pd
from database import *


def show(connect):

    st.title("📦Stock Management")

    products = get_product_names(connect)

    product_names = {p[1]: p[0] for p in products}

    selected_product = st.selectbox(
        "Select Product",
        list(product_names.keys())
    )

    quantity = st.number_input("Quantity", min_value=1)

    action = st.selectbox(
        "Action",
        ["Stock In","Stock Out"]
    )

    if st.button("Update Stock"):

        product_id = product_names[selected_product]

        if action == "Stock In":
            update_stock(connect, product_id, quantity)

        else:
            update_stock(connect, product_id, -quantity)

        st.success("Stock updated")