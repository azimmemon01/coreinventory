import streamlit as st
import pandas as pd
from database import *

def show(connect):

    st.title("📥 Receipts")

    products = get_product_names(connect)

    product_dict = {p[1]: p[0] for p in products}

    selected_product = st.selectbox(
        "Product",
        list(product_dict.keys())
    )

    qty = st.number_input("Quantity", min_value=1)

    if st.button("Add Receipt"):
        add_receipt(connect, selected_product, qty, "Pending")
        st.success("Receipt added")

    st.divider()

    receipts = get_receipts(connect)

    df = pd.DataFrame(
        receipts,
        columns=["ID","Product","Quantity","Status"]
    )

    st.dataframe(df, use_container_width=True)

    st.subheader("Update Receipt Status")

    receipt_id = st.selectbox("Select Receipt", df["ID"])

    new_status = st.selectbox(
        "Status",
        ["Pending","Received"]
    )

    if st.button("Update Status"):
        update_receipt_status(connect, receipt_id, new_status)
        st.success("Receipt updated")