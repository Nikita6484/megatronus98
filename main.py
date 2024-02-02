import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="megatronus")
st.title("Графопостроитель")
st.subheader("Отправьте мне файл excel")

uploaded_file = st.file_uploader("Выберите файл", type="xlsx")
if uploaded_file:
    df = pd.read_excel(uploaded_file, engine="openpyxl")
    st.dataframe(df)
    groupby_column = st.selectbox(
        "Что вы хотите проанализировать?",
        ("Ship Mode", "Segment", "Category", "Sub-Category"),
    )
    output_columns = ["Sales", "Profit"]
    df_grouped = df.groupby(by=[groupby_column], as_index=False)[output_columns].sum()

    fig = px.bar(
        df_grouped,
        x=groupby_column,
        y = "Sales",
        color="Profit",
        color_continuous_scale=["red", "yellow", "green"],
        template="plotly_white",
        title=f"<b>Продажи и прибыль по {groupby_column}</b>"
    )
    st.plotly_chart(fig)