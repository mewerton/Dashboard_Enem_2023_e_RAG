import streamlit as st
from constants import FAIXA_ETARIA_MAP, REDE_ENSINO_MAP  # Importar os mapeamentos do arquivo constants.py

def render_sidebar(data):
    st.sidebar.header("Filtros")
    
    # Filtro por faixa etária com descrição
    faixas_etarias = sorted(data["TP_FAIXA_ETARIA"].unique())
    faixa_etaria_opcoes = [FAIXA_ETARIA_MAP[faixa] for faixa in faixas_etarias]
    faixa_etaria = st.sidebar.multiselect("Faixa Etária", faixa_etaria_opcoes, default=faixa_etaria_opcoes)
    
    # Converter as descrições de volta para os números
    faixa_etaria_numeros = [key for key, value in FAIXA_ETARIA_MAP.items() if value in faixa_etaria]

    # Filtro por sexo
    sexos = sorted(data["TP_SEXO"].unique())
    sexo = st.sidebar.multiselect("Sexo", sexos, default=sexos)

    # Filtro por UF
    ufs = sorted(data["SG_UF_ESC"].dropna().unique())
    uf = st.sidebar.multiselect("Estado (UF)", ufs, default=ufs)

    # Filtro por rede de ensino com descrição
    redes_numeros = sorted(data["TP_ESCOLA"].dropna().unique())
    redes_opcoes = [REDE_ENSINO_MAP[rede] for rede in redes_numeros]
    redes_selecionadas = st.sidebar.multiselect("Rede de Ensino", redes_opcoes, default=redes_opcoes)

    # Converter as descrições de volta para os números
    redes_numeros_selecionados = [key for key, value in REDE_ENSINO_MAP.items() if value in redes_selecionadas]

    # Retornar os filtros
    return faixa_etaria_numeros, sexo, uf, redes_numeros_selecionados