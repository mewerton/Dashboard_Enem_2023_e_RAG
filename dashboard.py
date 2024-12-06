import pandas as pd
import streamlit as st
import plotly.express as px
from chatbot import botao_analise
from constants import (FAIXA_ETARIA_MAP, SEXO_MAP, REDE_ENSINO_MAP, 
                       ACESSO_INTERNET_MAP, RENDA_FAMILIAR_MAP, 
                       ESCOLARIDADE_PAIS_MAP)

# Configurar o layout em wide
st.set_page_config(page_title="Dashboard ENEM 2023", layout="wide")

def render_dashboard(data, faixa_etaria, sexo, uf, rede, filtro_notas):
    # Substituir os valores categóricos pelas descrições
    data["TP_FAIXA_ETARIA_DESC"] = data["TP_FAIXA_ETARIA"].map(FAIXA_ETARIA_MAP)
    data["TP_SEXO_DESC"] = data["TP_SEXO"].map(SEXO_MAP)
    data["TP_ESCOLA_DESC"] = data["TP_ESCOLA"].map(REDE_ENSINO_MAP)
    data["Q025_DESC"] = data["Q025"].map(ACESSO_INTERNET_MAP)
    data["Q006_DESC"] = data["Q006"].map(RENDA_FAMILIAR_MAP)
    data["Q001_DESC"] = data["Q001"].map(ESCOLARIDADE_PAIS_MAP)
    data["Q002_DESC"] = data["Q002"].map(ESCOLARIDADE_PAIS_MAP)

    # Filtrar os dados com base nos filtros do sidebar
    data_filtered = data[
        ((faixa_etaria == ["TODOS"]) | (data["TP_FAIXA_ETARIA"].isin(faixa_etaria))) &
        (data["TP_SEXO"].isin(sexo) if sexo else True) &
        ((uf == ["TODOS"]) | (data["SG_UF_ESC"].isin(uf))) &  # Verifica se "TODOS" está selecionado no filtro de Estado (UF)
        (data["TP_ESCOLA"].isin(rede) if rede else True)
    ]

    # Aplicar o filtro de notas válidas
    if filtro_notas == "Notas Válidas (0-1000)":
        data_filtered = data_filtered[
            data_filtered[["NU_NOTA_CN", "NU_NOTA_CH", "NU_NOTA_LC", "NU_NOTA_MT", "NU_NOTA_REDACAO"]]
            .apply(lambda row: row.between(0, 1000).all(), axis=1)
        ]

    st.title("Estatísticas - ENEM 2023")

    # Cálculo das métricas
    total_alunos = len(data)  # Total geral de alunos sem filtros
    total_filtrado = len(data_filtered)  # Total de alunos após filtros
    sexo_m = len(data_filtered[data_filtered["TP_SEXO_DESC"] == "Masculino"])
    sexo_f = len(data_filtered[data_filtered["TP_SEXO_DESC"] == "Feminino"])
    rede_predominante = (
        data_filtered["TP_ESCOLA_DESC"].value_counts().idxmax()
        if not data_filtered.empty else "N/A"
    )
    faixa_etaria_comum = (
        data_filtered["TP_FAIXA_ETARIA_DESC"].value_counts().idxmax()
        if not data_filtered.empty else "N/A"
    )

    # Exibir métricas
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric("Total de Alunos (Geral)", f"{total_alunos:,}".replace(",", "."))
    col2.metric("Total Filtrado", f"{total_filtrado:,}".replace(",", "."))
    col3.metric("Sexo M", f"{sexo_m:,}".replace(",", "."))
    col4.metric("Sexo F", f"{sexo_f:,}".replace(",", "."))
    col5.metric("Rede Predominante", rede_predominante)
    col6.metric("Faixa Etária Comum", faixa_etaria_comum)



    # Linha separadora
    st.divider()

    faixa_etaria_order = list(FAIXA_ETARIA_MAP.values())

    # Criação das Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Sexo & Idade", "Rede & Região", "Média por UF", "Faixa & Rede", "Comparação"])

    # 1. Faixa Etária
# 1. Faixa Etária
    with tab1:
        col1, col2 = st.columns(2)

        # Gráfico 1: Distribuição por Sexo
        with col1:
            sexo_fig = px.pie(
                data_filtered,
                names="TP_SEXO_DESC",
                title="Distribuição por Sexo",
                hole=0.4,
                color_discrete_sequence=px.colors.sequential.RdBu
            )
            sexo_fig.update_layout(
                font=dict(color="white"),
            )
            sexo_fig.update_traces(hovertemplate="<b>Sexo</b>: %{label}<br><b>Porcentagem</b>: %{percent}")
            st.plotly_chart(sexo_fig, use_container_width=True, key="sexo_fig")

        # Gráfico 2: Distribuição por Faixa Etária
        with col2:
            faixa_fig = px.histogram(
                data_filtered,
                x="TP_FAIXA_ETARIA_DESC",
                title="Distribuição por Faixa Etária",
                color_discrete_sequence=["#FFA07A"]
            )
            faixa_fig.update_layout(
                xaxis_title="Faixa Etária",
                yaxis_title="Quantidade",
                xaxis=dict(categoryorder="array", categoryarray=faixa_etaria_order),
                font=dict(color="white"),
            )
            faixa_fig.update_traces(hovertemplate="<b>Faixa Etária</b>: %{x}<br><b>Quantidade</b>: %{y}")
            st.plotly_chart(faixa_fig, use_container_width=True, key="faixa_fig")

        # Adicionar tabelas abaixo dos gráficos
        st.subheader("Tabela: Distribuição por Sexo")
        tabela_sexo = data_filtered["TP_SEXO_DESC"].value_counts().reset_index()
        tabela_sexo.columns = ["Sexo", "Quantidade"]
        tabela_sexo["Porcentagem"] = (tabela_sexo["Quantidade"] / tabela_sexo["Quantidade"].sum() * 100).round(2)
        st.dataframe(tabela_sexo, use_container_width=True)

        st.subheader("Tabela: Distribuição por Faixa Etária")
        tabela_faixa_etaria = data_filtered["TP_FAIXA_ETARIA_DESC"].value_counts().reset_index()
        tabela_faixa_etaria.columns = ["Faixa Etária", "Quantidade"]
        tabela_faixa_etaria["Porcentagem"] = (tabela_faixa_etaria["Quantidade"] / tabela_faixa_etaria["Quantidade"].sum() * 100).round(2)
        st.dataframe(tabela_faixa_etaria, use_container_width=True)

        # Botão de análise

        tabelas = [("Distribuição por Sexo", tabela_sexo), ("Distribuição por Faixa Etária", tabela_faixa_etaria)]
        botao_analise("Análise de Sexo & Idade", tabelas)

    with tab2:
        col1, col2 = st.columns(2)

        # Gráfico 1: Distribuição por Rede de Ensino
        with col1:
            rede_fig = px.pie(
                data_filtered,
                names="TP_ESCOLA_DESC",
                title="Distribuição por Rede de Ensino",
                hole=0.4,
                color_discrete_sequence=px.colors.sequential.Plasma_r  # Paleta vibrante
            )
            rede_fig.update_layout(
                font=dict(color="white"),
            )
            rede_fig.update_traces(
                textinfo="percent+label",
                hovertemplate="<b>Rede de Ensino</b>: %{label}<br><b>Porcentagem</b>: %{percent}"
            )
            st.plotly_chart(rede_fig, use_container_width=True, key="rede_fig")

        # Gráfico 2: Distribuição por Região
        with col2:
            # Adicionar uma coluna "Estado" com "Não informado" para valores nulos
            data_filtered["Estado"] = data_filtered["SG_UF_ESC"].fillna("Não informado")

            # Criar o gráfico
            regiao_fig = px.histogram(
                data_filtered,
                x="Estado",
                title="Distribuição por Estado (UF)",
                color_discrete_sequence=["#90ee90"]
            )
            regiao_fig.update_layout(
                font=dict(color="white"),
                xaxis_title="Estado (UF)",
                yaxis_title="Quantidade",
            )
            regiao_fig.update_traces(
                hovertemplate="<b>Estado (UF)</b>: %{x}<br><b>Quantidade</b>: %{y}"
            )
            st.plotly_chart(regiao_fig, use_container_width=True, key="regiao_fig")

        # Tabela: Distribuição por Rede de Ensino
        st.subheader("Tabela: Distribuição por Rede de Ensino")
        tabela_rede = data_filtered["TP_ESCOLA_DESC"].value_counts().reset_index()
        tabela_rede.columns = ["Rede de Ensino", "Quantidade"]
        tabela_rede["Porcentagem"] = (tabela_rede["Quantidade"] / tabela_rede["Quantidade"].sum() * 100).round(2)
        # Exibe a tabela apenas se você deseja visualizar os dados:
        st.dataframe(tabela_rede, use_container_width=True)

        # Tabela: Distribuição por Estado (UF)
        st.subheader("Tabela: Distribuição por Estado (UF)")
        tabela_regiao = data_filtered["Estado"].value_counts().reset_index()
        tabela_regiao.columns = ["Estado (UF)", "Quantidade"]
        tabela_regiao["Porcentagem"] = (tabela_regiao["Quantidade"] / tabela_regiao["Quantidade"].sum() * 100).round(2)
        # Exibe a tabela apenas se você deseja visualizar os dados:
        st.dataframe(tabela_regiao, use_container_width=True)

        # Botão de análise
        tabelas_tab2 = [
            ("Distribuição por Rede de Ensino", tabela_rede),
            ("Distribuição por Estado (UF)", tabela_regiao),
        ]
        botao_analise("Análise de Rede de ensino e Região", tabelas_tab2, botao_texto="Análise de Rede de ensino e Região", key="botao_tab2")

    with tab3:
        col1, col2 = st.columns(2)

        # Gráfico 1: Média Simples das Notas por Estado (UF)
        with col1:
            data_filtered["MEDIA_SIMPLES"] = data_filtered[["NU_NOTA_CN", "NU_NOTA_CH", "NU_NOTA_LC", "NU_NOTA_MT", "NU_NOTA_REDACAO"]].mean(axis=1)
            media_estado_data = data_filtered.groupby("SG_UF_ESC")["MEDIA_SIMPLES"].mean().reset_index()

            media_estado_fig = px.bar(
                media_estado_data,
                x="SG_UF_ESC",
                y="MEDIA_SIMPLES",
                title="Média Simples das Notas por Estado (UF)",
                text="MEDIA_SIMPLES",
                color_discrete_sequence=["#FFD700"]
            )
            media_estado_fig.update_layout(
                xaxis_title="Estado (UF)",
                yaxis_title="Média Simples das Notas",
                font=dict(color="white"),
            )
            media_estado_fig.update_traces(
                texttemplate="%{text:.2f}",
                textposition="outside",
                hovertemplate="<b>Estado (UF)</b>: %{x}<br><b>Média Simples</b>: %{y:.2f}"
            )
            st.plotly_chart(media_estado_fig, use_container_width=True, key="media_estado_fig")

        # Gráfico 2: Média Simples das Notas por Faixa Etária
        with col2:
            media_data = data_filtered.groupby("TP_FAIXA_ETARIA_DESC")["MEDIA_SIMPLES"].mean().reset_index()

            media_fig = px.bar(
                media_data,
                x="TP_FAIXA_ETARIA_DESC",
                y="MEDIA_SIMPLES",
                title="Média Simples das Notas por Faixa Etária",
                color="MEDIA_SIMPLES",
                color_continuous_scale="Blues"
            )
            media_fig.update_layout(
                xaxis_title="Faixa Etária",
                yaxis_title="Média Simples das Notas",
                xaxis=dict(categoryorder="array", categoryarray=faixa_etaria_order),
                font=dict(color="white"),
                coloraxis_colorbar=dict(
                    title="Média",
                    title_side="right"
                ),
            )
            media_fig.update_traces(
                hovertemplate="<b>Faixa Etária</b>: %{x}<br><b>Média Simples</b>: %{y:.2f}"
            )
            st.plotly_chart(media_fig, use_container_width=True, key="media_fig")

        # Tabela: Média Simples das Notas por Estado (UF)
        st.subheader("Tabela: Média Simples das Notas por Estado (UF)")
        tabela_estado = media_estado_data.copy()
        tabela_estado.columns = ["Estado (UF)", "Média Simples"]
        st.dataframe(tabela_estado, use_container_width=True)

        # Tabela: Média Simples das Notas por Faixa Etária
        st.subheader("Tabela: Média Simples das Notas por Faixa Etária")
        tabela_faixa = media_data.copy()
        tabela_faixa.columns = ["Faixa Etária", "Média Simples"]
        st.dataframe(tabela_faixa, use_container_width=True)

        # Botão de análise
        tabelas_tab3 = [
            ("Média Simples das Notas por Estado (UF)", tabela_estado),
            ("Média Simples das Notas por Faixa Etária", tabela_faixa),
        ]
        botao_analise("Análise das Médias", tabelas_tab3, botao_texto="Análise das Médias", key="botao_tab3")

    with tab4:
        # Distribuição por Rede de Ensino
        col1, col2 = st.columns(2)

        # Gráfico 1: Desempenho Geral por Faixa Etária
        with col1:
            data_grouped = data_filtered.groupby("TP_FAIXA_ETARIA_DESC")[
                ["NU_NOTA_MT", "NU_NOTA_LC", "NU_NOTA_CN", "NU_NOTA_CH", "NU_NOTA_REDACAO"]
            ].mean().reset_index()

            # Mapeamento de nomes das colunas para os nomes das matérias
            materia_map = {
                "NU_NOTA_MT": "Matemática",
                "NU_NOTA_LC": "Linguagens",
                "NU_NOTA_CN": "Ciências da Natureza",
                "NU_NOTA_CH": "Ciências Humanas",
                "NU_NOTA_REDACAO": "Redação"
            }

            # Ordenar faixas etárias
            faixa_etaria_order = list(FAIXA_ETARIA_MAP.values())
            data_grouped["TP_FAIXA_ETARIA_DESC"] = pd.Categorical(
                data_grouped["TP_FAIXA_ETARIA_DESC"],
                categories=faixa_etaria_order,
                ordered=True
            )
            data_grouped = data_grouped.sort_values("TP_FAIXA_ETARIA_DESC")

            # Renomear colunas de acordo com os nomes das matérias
            data_grouped_renamed = data_grouped.rename(columns=materia_map)

            # Verificar o número de faixas etárias para escolher o tipo de gráfico
            if len(data_grouped) == 1:
                provas_fig = px.bar(
                    data_grouped_renamed.melt(id_vars=["TP_FAIXA_ETARIA_DESC"],
                                            var_name="Prova",
                                            value_name="Média"),
                    x="Prova",
                    y="Média",
                    title=f"Desempenho Geral na Faixa Etária: {data_grouped['TP_FAIXA_ETARIA_DESC'].iloc[0]}",
                    color_discrete_sequence=["#FFA07A"]
                )

                # Gerar tabela para este tipo de gráfico
                tabela_provas = data_grouped_renamed.melt(id_vars=["TP_FAIXA_ETARIA_DESC"],
                                                        var_name="Prova",
                                                        value_name="Média")
            else:
                provas_fig = px.line(
                    data_grouped_renamed,
                    x="TP_FAIXA_ETARIA_DESC",
                    y=list(materia_map.values()),
                    title="Desempenho Geral nas Provas por Faixa Etária",
                    color_discrete_sequence=px.colors.sequential.Rainbow
                )

                # Gerar tabela para este tipo de gráfico
                tabela_provas = data_grouped_renamed.copy()

            provas_fig.update_layout(
                font=dict(color="white"),
                xaxis_title="Faixa Etária",
                yaxis_title="Média das Notas",
                xaxis=dict(categoryorder="array", categoryarray=faixa_etaria_order),
                legend_title="Matérias"
            )
            provas_fig.update_traces(
                hovertemplate="<b>Faixa Etária</b>: %{x}<br><b>Média</b>: %{y:.2f}"
            )

            st.plotly_chart(provas_fig, use_container_width=True, key="provas_fig")

        # Gráfico 2: Média Simples das Notas por Rede de Ensino
        with col2:
            data_filtered["MEDIA_SIMPLES"] = data_filtered[["NU_NOTA_CN", "NU_NOTA_CH", "NU_NOTA_LC", "NU_NOTA_MT", "NU_NOTA_REDACAO"]].mean(axis=1)
            media_rede_data = data_filtered.groupby("TP_ESCOLA_DESC")["MEDIA_SIMPLES"].mean().reset_index()

            media_rede_data = media_rede_data.sort_values(by="MEDIA_SIMPLES", ascending=True)

            media_rede_fig = px.bar(
                media_rede_data,
                y="TP_ESCOLA_DESC",
                x="MEDIA_SIMPLES",
                title="Média Simples das Notas por Rede de Ensino",
                text="MEDIA_SIMPLES",
                labels={"TP_ESCOLA_DESC": "Rede de Ensino", "MEDIA_SIMPLES": "Média Simples"},
                color="TP_ESCOLA_DESC",
                color_discrete_sequence=px.colors.sequential.Teal
            )
            media_rede_fig.update_layout(
                yaxis_title="Rede de Ensino",
                xaxis_title="Média Simples das Notas",
                font=dict(color="white"),
                title=dict(x=0.5)
            )
            media_rede_fig.update_traces(
                texttemplate="%{text:.2f}",
                textposition="outside",
                hovertemplate="<b>Rede de Ensino</b>: %{y}<br><b>Média Simples</b>: %{x:.2f}"
            )

            st.plotly_chart(media_rede_fig, use_container_width=True, key="media_rede_fig")

            # Tabela: Média Simples das Notas por Rede de Ensino
            tabela_rede = media_rede_data.copy()
            tabela_rede.columns = ["Rede de Ensino", "Média Simples"]

        # Tabela: Desempenho Geral por Faixa Etária
        st.subheader("Tabela: Desempenho Geral por Faixa Etária")
        st.dataframe(tabela_provas, use_container_width=True)

        # Tabela: Média Simples das Notas por Rede de Ensino
        st.subheader("Tabela: Média Simples das Notas por Rede de Ensino")
        st.dataframe(tabela_rede, use_container_width=True)

        # Botão de análise
        tabelas_tab4 = [
            ("Desempenho Geral por Faixa Etária", tabela_provas),
            ("Média Simples das Notas por Rede de Ensino", tabela_rede),
        ]
        botao_analise("Análise de Faixa Etária & Rede", tabelas_tab4, botao_texto="Analisar com Inteligência Artificial", key="botao_tab4")

    with tab5:
        col1, col2 = st.columns(2)

        # Gráfico 1: Média Geral das Provas por Sexo
        with col1:
            prova_map = {
                "NU_NOTA_CN": "Ciências da Natureza",
                "NU_NOTA_CH": "Ciências Humanas",
                "NU_NOTA_LC": "Linguagens e Códigos",
                "NU_NOTA_MT": "Matemática",
                "NU_NOTA_REDACAO": "Redação"
            }

            # Agrupamento por sexo e cálculo das médias
            media_geral_data = (
                data_filtered.groupby("TP_SEXO_DESC")[
                    ["NU_NOTA_MT", "NU_NOTA_LC", "NU_NOTA_CN", "NU_NOTA_CH", "NU_NOTA_REDACAO"]
                ]
                .mean()
                .reset_index()
                .melt(id_vars=["TP_SEXO_DESC"], var_name="Prova", value_name="Média")
            )

            # Substituir os códigos das provas pelos nomes
            media_geral_data["Prova"] = media_geral_data["Prova"].map(prova_map)

            # Criar gráfico de barras agrupadas
            media_geral_fig = px.bar(
                media_geral_data,
                x="TP_SEXO_DESC",
                y="Média",
                color="Prova",
                barmode="group",
                title="Média Geral das Provas por Sexo",
                color_discrete_sequence=px.colors.sequential.Viridis
            )
            media_geral_fig.update_layout(
                font=dict(color="white"),
                xaxis_title="Sexo",
                yaxis_title="Média de Notas",
                legend_title="Provas",
            )
            media_geral_fig.update_traces(
                hovertemplate="<b>Média</b>: %{y:.2f}"
            )
            st.plotly_chart(media_geral_fig, use_container_width=True, key="media_geral_fig")

        # Gráfico 2: Diferença de Médias das Provas por Sexo
        with col2:
            if set(data_filtered["TP_SEXO_DESC"].unique()) >= {"Masculino", "Feminino"}:
                diff_data = (
                    data_filtered.groupby("TP_SEXO_DESC")[
                        ["NU_NOTA_MT", "NU_NOTA_LC", "NU_NOTA_CN", "NU_NOTA_CH", "NU_NOTA_REDACAO"]
                    ]
                    .mean()
                    .reset_index()
                    .melt(id_vars=["TP_SEXO_DESC"], var_name="Prova", value_name="Média")
                    .pivot(index="Prova", columns="TP_SEXO_DESC", values="Média")
                )
                diff_data.index = diff_data.index.map(prova_map)
                diff_data["Diferença"] = (diff_data["Masculino"] - diff_data["Feminino"]).round(2)  # Arredondar para 2 casas decimais
                diff_data = diff_data.reset_index()

                diff_fig = px.bar(
                    diff_data,
                    x="Diferença",
                    y="Prova",
                    orientation="h",
                    title="Diferença de Médias das Provas por Sexo",
                    text="Diferença",
                    color="Diferença",
                    color_continuous_scale="RdBu"
                )
                diff_fig.update_layout(
                    font=dict(color="white"),
                    xaxis_title="Diferença (Masculino - Feminino)",
                    yaxis_title="Matéria",
                    coloraxis_showscale=False,
                )
                diff_fig.update_traces(
                    texttemplate="%{x:.2f}",  # Formatar valores com 2 casas decimais
                    hovertemplate="<b>Prova</b>: %{y}<br><b>Diferença</b>: %{x:.2f}"  # Exibir 2 casas decimais no hover
                )
                st.plotly_chart(diff_fig, use_container_width=True, key="diff_fig")
            else:
                st.warning("É necessário marcar os dois sexos no sidebar para exibir este gráfico.")


        # Tabela: Média Geral das Provas por Sexo
        st.subheader("Tabela: Média Geral das Provas por Sexo")
        tabela_media_geral = media_geral_data.copy()
        tabela_media_geral.columns = ["Sexo", "Prova", "Média"]
        st.dataframe(tabela_media_geral, use_container_width=True)

        # Tabela: Diferença de Médias das Provas por Sexo
        if set(data_filtered["TP_SEXO_DESC"].unique()) >= {"Masculino", "Feminino"}:
            st.subheader("Tabela: Diferença de Médias das Provas por Sexo")
            tabela_diferenca = diff_data.copy()

            # Ajustar os nomes das colunas invertidas
            tabela_diferenca.columns = ["Prova", "Média Feminino", "Média Masculino", "Diferença"]
            st.dataframe(tabela_diferenca, use_container_width=True)

        # Botão de análise
        tabelas_tab5 = [
            ("Média Geral das Provas por Sexo", tabela_media_geral),
        ]
        if set(data_filtered["TP_SEXO_DESC"].unique()) >= {"Masculino", "Feminino"}:
            tabelas_tab5.append(("Diferença de Médias das Provas por Sexo", tabela_diferenca))

        botao_analise("Análise por Sexo", tabelas_tab5, botao_texto="Analisar com Inteligência Artificial", key="botao_tab5")
