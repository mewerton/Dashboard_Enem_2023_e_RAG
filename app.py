import streamlit as st
from data_loader import load_dataset
from sidebar import render_sidebar
from dashboard import render_dashboard

def main():
    # Carregar o dataset
    data = load_dataset()
    if data is None:
        st.stop()

    # Renderizar o sidebar
    faixa_etaria, sexo, uf, rede = render_sidebar(data)

    # Renderizar o dashboard
    render_dashboard(data, faixa_etaria, sexo, uf, rede)

if __name__ == "__main__":
    main()
