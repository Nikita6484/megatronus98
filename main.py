import pandas as pd
import streamlit as st



st.set_page_config(page_title="Supermarket sales",
                              page_icon=":full_moon:",
                              layout="wide"
)



df=pd.read_excel(io="supermarkt_sales.xlsx",
                 engine="openpyxl",
                 sheet_name="Sales",
                 skiprows=3,
                 usecols="B:R",
                 nrows=1000,
)

st.sidebar.header("фильтр")
city=st.sidebar.multiselect(
                "Выберете город",
                options=df["City"].unique(),
                default=df["City"].unique()
 )

customer_type=st.sidebar.multiselect(
                "Выберете тип покупателя",
                options=df["Customer_type"].unique(),
                default=df["Customer_type"].unique()
)


gender=st.sidebar.multiselect(
                "Выберете пол",
                options=df["Gender"].unique(),
                default=df["Gender"].unique()
)

branch=st.sidebar.multiselect(
                "Выберете категорию",
                options=df["Branch"].unique(),
                default=df["Branch"].unique()
)

df_selection=(df.iloc[350:550].query(
    "City==@city & Customer_type==@customer_type & Gender==@gender & Branch==@branch "
))
st.dataframe(df_selection)