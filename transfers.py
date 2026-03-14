import streamlit as st
import pandas as pd
from database import *

def show(connect):

    def show(connect):

     st.title("🔄 Internal Transfers")

    col1,col2 = st.columns(2)

    with col1:
        from_wh = st.text_input("From Warehouse")

    with col2:
        to_wh = st.text_input("To Warehouse")

    product = st.text_input("Product")
    qty = st.number_input("Quantity")

    if st.button("Schedule Transfer"):
        add_transfer(connect, from_wh, to_wh, product, qty)
        st.success("Transfer scheduled")

    st.divider()

    transfers = get_transfers(connect)

    df = pd.DataFrame(
        transfers,
        columns=["From","To","Product","Quantity"]
    )

    st.dataframe(df, use_container_width=True)