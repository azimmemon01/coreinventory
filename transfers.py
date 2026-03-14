import streamlit as st
import pandas as pd
from database import *

def show(connect, status_filter="All"):

    st.title("🔄 Internal Transfers")

    products = get_product_names(connect)

    product_dict = {p[1]: p[0] for p in products}

    col1, col2 = st.columns(2)

    with col1:
        from_wh = st.text_input("From Warehouse")

    with col2:
        to_wh = st.text_input("To Warehouse")

    selected_product = st.selectbox(
        "Product",
        list(product_dict.keys())
    )

    qty = st.number_input("Quantity", min_value=1)

    if st.button("Schedule Transfer"):

        add_transfer(connect, from_wh, to_wh, selected_product, qty)

        st.success("Transfer scheduled")

    st.divider()

    transfers = get_transfers(connect)

    df = pd.DataFrame(
        transfers,
        columns=["From","To","Product","Quantity","Status"]
    )

    # 🔎 APPLY FILTER
    if status_filter != "All" and "Status" in df.columns:
        df = df[df["Status"] == status_filter]

    if df.empty:
        st.info("No transfers found")
        return

    st.dataframe(df, use_container_width=True)