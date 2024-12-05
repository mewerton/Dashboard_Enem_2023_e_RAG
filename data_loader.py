import pandas as pd
import streamlit as st

@st.cache_data
def load_dataset():
    dataset_path = "./database/MICRODADOS_ENEM_2023_filtered_PQ.parquet"
    try:
        data = pd.read_parquet(dataset_path)
        return data
    except Exception as e:
        st.error(f"Erro ao carregar o dataset: {e}")
        return None

