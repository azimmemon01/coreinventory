import streamlit as st
import pandas as pd
from database import *


def show(connect):

    st.title("📦 Inventory Management Dashboard")
    st.caption("Monitor stock and warehouse operations")

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Products", total_products(connect))
    col2.metric("Low Stock", low_stock(connect))
    col3.metric("Out of Stock", out_of_stock(connect))
    col4.metric("Pending Deliveries",pending_deliveries(connect) )

    col5, col6 = st.columns(2)

    col5.metric("Pending Receipts", pending_receipts(connect))
    col6.metric("Transfers Scheduled", scheduled_transfers(connect))

    st.divider()
    stock_data = get_product_stock(connect)
    st.write(stock_data)

    df = pd.DataFrame(
    stock_data,
    columns=["Product", "Stock"]
    )

    st.subheader("📊 Stock Distribution")

    if not df.empty:
     st.bar_chart(df.set_index("Product"))
    else:
     st.info("No products added yet")
    inventory = get_inventory(connect)

    table_df = pd.DataFrame(
    inventory,
    columns=["Product", "Category", "Price", "Stock"]
    )

    st.subheader("📋 Inventory Overview")

    st.dataframe(table_df, use_container_width=True)
    low_stock_df = table_df[table_df["Stock"] <= 5]

    if not low_stock_df.empty:
      st.subheader(" Low Stock Alerts")
      st.dataframe(low_stock_df)
    low_stock_products = get_low_stock_products(connect)

    df_low = pd.DataFrame(
    low_stock_products,
    columns=["Product","Current Stock","Minimum Stock"]
   )

    if not df_low.empty:

     st.subheader("⚠ Low Stock Alert")

     st.dataframe(df_low, use_container_width=True)