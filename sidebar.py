import streamlit as st
from constants import FAIXA_ETARIA_MAP, REDE_ENSINO_MAP  # Importar os mapeamentos do arquivo constants.py

def render_sidebar(data):
    st.sidebar.header("Filtros")
    
    # Filtro por faixa etária com descrição
    faixas_etarias = data["TP_FAIXA_ETARIA"].unique()
    faixa_etaria_opcoes = [FAIXA_ETARIA_MAP.get(faixa, f"Não informado ({faixa})") for faixa in faixas_etarias]
    faixa_etaria = st.sidebar.multiselect("Faixa Etária", faixa_etaria_opcoes, default=faixa_etaria_opcoes)

    # Converter as descrições de volta para os números
    faixa_etaria_numeros = [key for key, value in FAIXA_ETARIA_MAP.items() if value in faixa_etaria]
    if "Não informado" in faixa_etaria:
        faixa_etaria_numeros.append(None)

    # Filtro por sexo
    sexos = sorted(data["TP_SEXO"].unique())
    sexo_opcoes = ["Masculino", "Feminino"]
    sexo_selecionado = st.sidebar.multiselect("Sexo", sexo_opcoes, default=sexo_opcoes)
    sexo = [s[0] for s in sexo_selecionado]  # Converter para "M" ou "F"

    # Filtro por UF (inclui valores NaN como 'Não informado')
    ufs = data["SG_UF_ESC"].fillna("Não informado").unique()
    uf = st.sidebar.multiselect("Estado (UF)", ufs, default=ufs)
    if "Não informado" in uf:
        uf = list(data["SG_UF_ESC"].unique())  # Inclui NaN no filtro

    # Filtro por rede de ensino com descrição
    redes_numeros = data["TP_ESCOLA"].fillna("Não informado").unique()
    redes_opcoes = [REDE_ENSINO_MAP.get(rede, f"Não informado ({rede})") for rede in redes_numeros]
    redes_selecionadas = st.sidebar.multiselect("Rede de Ensino", redes_opcoes, default=redes_opcoes)

    # Converter as descrições de volta para os números
    redes_numeros_selecionados = [
        key for key, value in REDE_ENSINO_MAP.items() if value in redes_selecionadas
    ]
    if "Não informado" in redes_selecionadas:
        redes_numeros_selecionados.append(None)

    # Retornar os filtros
    return faixa_etaria_numeros, sexo, uf, redes_numeros_selecionados
