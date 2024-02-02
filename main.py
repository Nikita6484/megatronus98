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