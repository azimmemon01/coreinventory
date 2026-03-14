import streamlit as st
import pandas as pd
from database import *

def show(connect):

    st.title("📜 Stock Activity History")

    history = get_stock_history(connect)

    df = pd.DataFrame(
        history,
        columns=["Product","Action","Quantity","Date"]
    )

    st.dataframe(df, use_container_width=True)