import pandas as pd
import streamlit as st
import plotly.express as px


st.set_page_config(page_title="Supermarket sales",
                              page_icon=":full_moon:",
                              layout="wide"
)



@st.cache
def get_data_from_excel():
 df=pd.read_excel(
        io="supermarkt_sales.xlsx",
        engine="openpyxl",
        sheet_name="Sales",
        skiprows=3,
        usecols="B:R",
        nrows=1000,
    )


 df["hour"]=pd.to_datetime(df["Time"],format="%H:%M:%S").dt.hour
 return df
df =get_data_from_excel()
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

st.title(" Панель управления продажами")
st.markdown("##")

total_sales=int(df_selection["Total"].sum())
average_rating=round(df_selection["Rating"].mean(),1)
star_rating=":star:"*int(round(average_rating,0))
average_sale_by_transaction=round(df_selection["Total"].mean(),2)

left_column,middle_column,right_column=st.columns(3)
with left_column:
    st.subheader("Общий объём продаж")
    st.subheader(f"US $ {total_sales:,}")
with middle_column:
    st.subheader("Средняя оценка")
    st.subheader(f"{average_rating} {star_rating}")
with right_column:
    st.subheader("Средний объём продаж")
    st.subheader(f"US ${average_sale_by_transaction}")#

sales_by_product_line=(
    df_selection.groupby(by=["Product_line"]).sum(numeric_only=True)[["Total"]].sort_values(by="Total")
)
fig_product_sales=px.bar(
    sales_by_product_line,
    x="Total",
    y=sales_by_product_line.index,
    orientation="h",
    title="<b>Продажи по продуктовой линии</b>",
    color_discrete_sequence=["#0083B8"]*len(sales_by_product_line),
    template="plotly_white",
)
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)


sales_by_hour=df_selection.groupby(by=["hour"]).sum(numeric_only=True)[["Total"]]
fig_hour_sales=px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Total",
    title="<b>Продажи в час</b>",
    color_discrete_sequence=["#0083B8"]*len(sales_by_hour),
    template="plotly_white",
)
fig_hour_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)
left_column,right_column=st.columns(2)
left_column.plotly_chart(fig_hour_sales,use_container_width=True)
right_column.plotly_chart(fig_product_sales,use_container_width=True)
st.dataframe(df_selection)