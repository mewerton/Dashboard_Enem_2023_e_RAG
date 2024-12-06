import streamlit as st
from data_loader import load_dataset
from sidebar import render_sidebar
from dashboard import render_dashboard

def main():
    data = load_dataset()
    if data is None:
        st.stop()

    #Renderizar o sidebar e capturar os filtros
    faixa_etaria, sexo, uf, rede, filtro_notas = render_sidebar(data)

    #Renderizar o dashboard
    render_dashboard(data, faixa_etaria, sexo, uf, rede, filtro_notas)

if __name__ == "__main__":
    main()
