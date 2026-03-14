import streamlit as st
import pandas as pd
from database import *

def show(connect, status_filter="All"):

    st.title("🚚 Deliveries")

    products = get_product_names(connect)

    product_dict = {p[1]: p[0] for p in products}

    selected_product = st.selectbox(
        "Product",
        list(product_dict.keys())
    )

    qty = st.number_input("Quantity", min_value=1)

    if st.button("Add Delivery"):

        add_delivery(connect, selected_product, qty, "Pending")

        st.success("Delivery added")

    st.divider()

    deliveries = get_deliveries(connect)

    df = pd.DataFrame(
        deliveries,
        columns=["ID","Product","Quantity","Status"]
    )

    # 🔎 Apply status filter
    if status_filter != "All":
        df = df[df["Status"] == status_filter]

    st.subheader("Delivery List")

    st.dataframe(df, use_container_width=True)

    st.divider()

    st.subheader("Update Delivery Status")

    delivery_id = st.selectbox(
        "Select Delivery",
        df["ID"]
    )

    new_status = st.selectbox(
        "Status",
        ["Pending","Delivered"]
    )

    if st.button("Update Status"):

        update_delivery_status(connect, delivery_id, new_status)

        st.success("Delivery updated")