import pandas as pd
import streamlit as st
import plotly.express as px
import base64
from io import StringIO,BytesIO

def generate_excel_download_link(df):
    towrite = BytesIO()
    df.to_excel(towrite, index=False, header=True)  
    towrite.seek(0)  # reset pointer
    b64 = base64.b64encode(towrite.read()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="data_download.xlsx">Скачать таблицу</a>'
    return st.markdown(href, unsafe_allow_html=True)

def generate_html_download_link(fig):
    towrite = StringIO()
    fig.write_html(towrite, include_plotlyjs="cdn")
    towrite = BytesIO(towrite.getvalue().encode())
    b64 = base64.b64encode(towrite.read()).decode()
    href = f'<a href="data:text/html;charset=utf-8;base64, {b64}" download="plot.html">Скачать график</a>'
    return st.markdown(href, unsafe_allow_html=True)

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

    generate_excel_download_link(df_grouped)
    generate_html_download_link(fig)