import streamlit as st
import pandas as pd
from database import *



def show(connect):

    st.title("📦 Product Management")

    st.subheader("Add New Product")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Product Name")
        category = st.text_input("Category")

    with col2:
        price = st.number_input("Price")
        min_stock = st.number_input("Minimum Stock")

    if st.button("Add Product"):

        if name != "":
            add_product(connect, name, category, price, min_stock)
            st.success("Product added successfully")
        else:
            st.warning("Product name required")

    st.divider()

    st.subheader("Product List")

    products = get_products(connect)

    df = pd.DataFrame(
        products,
        columns=["ID","Name","Category","Price","Min Stock","Quantity"]
    )

    st.dataframe(df, use_container_width=True)
    st.write(products)