import streamlit as st
from constants import FAIXA_ETARIA_MAP, REDE_ENSINO_MAP  # Importar os mapeamentos do arquivo constants.py

def render_sidebar(data):
    st.sidebar.header("Filtros")
    
    # Filtro por faixa etária com descrição
    faixa_etaria_opcoes = ["TODOS"] + [FAIXA_ETARIA_MAP[faixa] for faixa in sorted(FAIXA_ETARIA_MAP.keys())]
    faixa_etaria = st.sidebar.multiselect(
        "Faixa Etária",
        faixa_etaria_opcoes,
        default=["TODOS"],  # Apenas "TODOS" selecionado inicialmente
        key="faixa_etaria"
    )

    # Garantir que "TODOS" exclua outras opções e vice-versa
    if "TODOS" in faixa_etaria and len(faixa_etaria) > 1:
        faixa_etaria = ["TODOS"]
        st.sidebar.warning("Ao selecionar 'TODOS', as outras opções são desmarcadas automaticamente.")
    elif "TODOS" not in faixa_etaria and len(faixa_etaria) == 0:
        faixa_etaria = ["TODOS"]
        st.sidebar.warning("Nenhuma faixa etária selecionada. Revertendo para 'TODOS'.")

    # Converter as descrições de volta para os números, incluindo a lógica para "TODOS"
    if "TODOS" in faixa_etaria:
        faixa_etaria_numeros = list(FAIXA_ETARIA_MAP.keys()) + [None]
    else:
        faixa_etaria_numeros = [key for key, value in FAIXA_ETARIA_MAP.items() if value in faixa_etaria]
        if "Não informado" in faixa_etaria:
            faixa_etaria_numeros.append(None)

    # Filtro por sexo
    sexos = sorted(data["TP_SEXO"].unique())
    sexo_opcoes = ["Masculino", "Feminino"]
    sexo_selecionado = st.sidebar.multiselect("Sexo", sexo_opcoes, default=sexo_opcoes)
    sexo = [s[0] for s in sexo_selecionado]  # Converter para "M" ou "F"

    # Filtro por UF (Estado) com "TODOS"
    uf_opcoes = ["TODOS"] + list(data["SG_UF_ESC"].fillna("Não informado").unique())
    uf_selecionado = st.sidebar.multiselect(
        "Estado (UF)",
        uf_opcoes,
        default=["TODOS"],  # Apenas "TODOS" selecionado inicialmente
        key="estado"
    )

    # Garantir que "TODOS" exclua outras opções e vice-versa
    if "TODOS" in uf_selecionado and len(uf_selecionado) > 1:
        uf_selecionado = ["TODOS"]
        st.sidebar.warning("Ao selecionar 'TODOS', as outras opções são desmarcadas automaticamente.")
    elif "TODOS" not in uf_selecionado and len(uf_selecionado) == 0:
        uf_selecionado = ["TODOS"]
        st.sidebar.warning("Nenhum estado selecionado. Revertendo para 'TODOS'.")

    # Ajustar os valores selecionados para o filtro
    if "TODOS" in uf_selecionado:
        uf = list(data["SG_UF_ESC"].unique())  # Inclui todos os estados, incluindo NaN
    else:
        uf = [u for u in uf_selecionado]

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

    # Filtro por notas válidas ou todos
    st.sidebar.subheader("Notas")
    filtro_notas_opcoes = ["Notas Válidas (0-1000)", "Todos"]
    filtro_notas = st.sidebar.radio("Selecione:", filtro_notas_opcoes, index=1)

    # Retornar os filtros
    return faixa_etaria_numeros, sexo, uf, redes_numeros_selecionados, filtro_notas
