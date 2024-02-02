import pandas as pd
import streamlit as st



st.set_page_config(page_title="Supermarket",
                              page_icon=":rainbow:",
                              layout="wide"
)



df=pd.read_excel(io="supermarkt_sales.xlsx",
                 engine="openpyxl",
                 sheet_name="Sales",
                 skiprows=3,
                 usecols="B:R",
                 nrows=1000,
)
df_selection=(df.iloc[350:550])
st.dataframe(df_selection)