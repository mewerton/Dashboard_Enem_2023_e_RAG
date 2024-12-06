import pandas as pd
import streamlit as st
import plotly.express as px
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
        (data["TP_FAIXA_ETARIA"].isin(faixa_etaria) if faixa_etaria else True) &
        (data["TP_SEXO"].isin(sexo) if sexo else True) &
        (data["SG_UF_ESC"].isin(uf) if uf else True) &
        (data["TP_ESCOLA"].isin(rede) if rede else True)
    ]

    # Aplicar o filtro de notas válidas
    if filtro_notas == "Notas Válidas (0-1000)":
        data_filtered = data_filtered[
            data_filtered[["NU_NOTA_CN", "NU_NOTA_CH", "NU_NOTA_LC", "NU_NOTA_MT", "NU_NOTA_REDACAO"]]
            .apply(lambda row: row.between(0, 1000).all(), axis=1)
        ]

    st.title("Dashboard ENEM 2023")

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
    # 1. Faixa Etária
    col1, col2 = st.columns(2)
    with col1:
        #st.subheader("Distribuição por Sexo")
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
        st.plotly_chart(sexo_fig, use_container_width=True)

        
    # 2. Média das Notas por Faixa Etária
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
        st.plotly_chart(faixa_fig, use_container_width=True)


        # 3. Média Simples por Estado (UF)
    col1, col2 = st.columns(2)
    with col1:
        #st.subheader("Média Simples das Notas por Estado (UF)")

        # Calcular a média simples das notas por estado (UF)
        data_filtered["MEDIA_SIMPLES"] = data_filtered[["NU_NOTA_CN", "NU_NOTA_CH", "NU_NOTA_LC", "NU_NOTA_MT", "NU_NOTA_REDACAO"]].mean(axis=1)
        media_estado_data = data_filtered.groupby("SG_UF_ESC")["MEDIA_SIMPLES"].mean().reset_index()

        # Criar o gráfico de barras
        media_estado_fig = px.bar(
            media_estado_data,
            x="SG_UF_ESC",
            y="MEDIA_SIMPLES",
            title="Média Simples das Notas por Estado (UF)",
            text="MEDIA_SIMPLES",  # Exibir a média no rótulo das barras
            color_discrete_sequence=["#FFD700"]
        )
        media_estado_fig.update_layout(
            xaxis_title="Estado (UF)",
            yaxis_title="Média Simples das Notas",
            font=dict(color="white"),
            #title=dict(x=0.5),  # Centraliza o título
        )
        media_estado_fig.update_traces(
            texttemplate="%{text:.2f}",  # Formata o texto com duas casas decimais
            textposition="outside",  # Posiciona o rótulo fora das barras
            hovertemplate="<b>Estado (UF)</b>: %{x}<br><b>Média Simples</b>: %{y:.2f}"
        )
        st.plotly_chart(media_estado_fig, use_container_width=True)

    # 4. Distribuição por Sexo
    with col2:
        # Calcular a média simples das notas por faixa etária
        data_filtered["MEDIA_SIMPLES"] = data_filtered[["NU_NOTA_CN", "NU_NOTA_CH", "NU_NOTA_LC", "NU_NOTA_MT", "NU_NOTA_REDACAO"]].mean(axis=1)
        media_data = data_filtered.groupby("TP_FAIXA_ETARIA_DESC")["MEDIA_SIMPLES"].mean().reset_index()

        # Criar o gráfico de barras com gradação de cores
        media_fig = px.bar(
            media_data,
            x="TP_FAIXA_ETARIA_DESC",
            y="MEDIA_SIMPLES",
            title="Média Simples das Notas por Faixa Etária",
            color="MEDIA_SIMPLES",  # Basear a cor na média simples
            color_continuous_scale="Blues",  # Paleta de cores
        )
        media_fig.update_layout(
            xaxis_title="Faixa Etária",
            yaxis_title="Média Simples das Notas",
            xaxis=dict(categoryorder="array", categoryarray=faixa_etaria_order),
            font=dict(color="white"),
            #title=dict(x=0.5),  # Centraliza o título
            coloraxis_colorbar=dict(
                title="Média",  # Legenda da escala de cores
                title_side="right"
            ),
        )
        media_fig.update_traces(
            hovertemplate="<b>Faixa Etária</b>: %{x}<br><b>Média Simples</b>: %{y:.2f}"
        )
        st.plotly_chart(media_fig, use_container_width=True)
        #st.metric("Total Filtrado (Distribuição por Sexo)", len(data_filtered))
        #faixa_etaria_order = list(FAIXA_ETARIA_MAP.values())


    # 5. Distribuição por Rede de Ensino
    col1, col2 = st.columns(2)
    with col1:
        #st.subheader("Distribuição por Rede de Ensino")
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
        st.plotly_chart(rede_fig, use_container_width=True)

    with col2:
        #st.subheader("Média Simples das Notas por Rede de Ensino")
        
        # Calcular a média simples das notas para cada rede de ensino
        data_filtered["MEDIA_SIMPLES"] = data_filtered[["NU_NOTA_CN", "NU_NOTA_CH", "NU_NOTA_LC", "NU_NOTA_MT", "NU_NOTA_REDACAO"]].mean(axis=1)
        media_rede_data = data_filtered.groupby("TP_ESCOLA_DESC")["MEDIA_SIMPLES"].mean().reset_index()

        # Ordenar os valores para uma apresentação mais clara
        media_rede_data = media_rede_data.sort_values(by="MEDIA_SIMPLES", ascending=True)  # Ordem crescente para barras horizontais

        # Criar o gráfico de barras horizontais
        media_rede_fig = px.bar(
            media_rede_data,
            y="TP_ESCOLA_DESC",  # Rede de ensino no eixo Y
            x="MEDIA_SIMPLES",  # Média simples no eixo X
            title="Média Simples das Notas por Rede de Ensino",
            text="MEDIA_SIMPLES",  # Mostrar as médias como texto nas barras
            labels={"TP_ESCOLA_DESC": "Rede de Ensino", "MEDIA_SIMPLES": "Média Simples"},
            color="TP_ESCOLA_DESC",  # Diferenciar redes pelo nome
            color_discrete_sequence=px.colors.sequential.Teal  # Paleta de cores
        )

        # Ajustar o layout do gráfico
        media_rede_fig.update_layout(
            yaxis_title="Rede de Ensino",
            xaxis_title="Média Simples das Notas",
            font=dict(color="white"),
            title=dict(x=0.5),  # Centralizar o título
        )

        # Mostrar os valores nas barras
        media_rede_fig.update_traces(
            texttemplate="%{text:.2f}", 
            textposition="outside", 
            hovertemplate="<b>Rede de Ensino</b>: %{y}<br><b>Média Simples</b>: %{x:.2f}"
        )

        # Exibir o gráfico
        st.plotly_chart(media_rede_fig, use_container_width=True)

    col1, col2 = st.columns(2)
    # 8. Comparação Geral por Sexo
    with col1:
        # Adicionar descrições das provas
        prova_map = {
            "NU_NOTA_CN": "Ciências da Natureza",
            "NU_NOTA_CH": "Ciências Humanas",
            "NU_NOTA_LC": "Linguagens e Códigos",
            "NU_NOTA_MT": "Matemática",
            "NU_NOTA_REDACAO": "Redação"
        }

        # Agrupar os dados e calcular a média
        media_geral_data = (
            data_filtered.groupby("TP_SEXO_DESC")[[
                "NU_NOTA_MT", "NU_NOTA_LC", "NU_NOTA_CN", "NU_NOTA_CH", "NU_NOTA_REDACAO"
            ]]
            .mean()
            .reset_index()
            .melt(id_vars=["TP_SEXO_DESC"], var_name="Prova", value_name="Média")
        )

        # Substituir os nomes das provas pelas descrições
        media_geral_data["Prova"] = media_geral_data["Prova"].map(prova_map)

        # Criar o gráfico
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
            hovertemplate="<b>Média</b>: %{y:.2f}"  # Apenas exibe a média no hover
        )
        # Adicionar a coluna Prova como customdata para o hovertemplate
        media_geral_fig.for_each_trace(lambda t: t.update(customdata=media_geral_data.loc[
            media_geral_data["Prova"] == t.name, ["Prova"]
        ].to_numpy()))

        st.plotly_chart(media_geral_fig, use_container_width=True)




    # 9. Desempenho por Sexo e Região em Provas
    #col1, col2 = st.columns(2)
    # with col2:
    #     st.subheader("Desempenho por Sexo e Região")
    #     desempenho_fig = px.bar(
    #         data_filtered.groupby(["TP_SEXO_DESC", "SG_UF_ESC"])[
    #             ["NU_NOTA_MT", "NU_NOTA_LC", "NU_NOTA_CN", "NU_NOTA_CH", "NU_NOTA_REDACAO"]
    #         ].mean().reset_index().melt(id_vars=["TP_SEXO_DESC", "SG_UF_ESC"]),
    #         x="SG_UF_ESC",
    #         y="value",
    #         color="TP_SEXO_DESC",
    #         facet_col="variable",
    #         barmode="group",
    #         title="Desempenho por Sexo e Região nas Provas",
    #         color_discrete_sequence=px.colors.sequential.Cividis
    #     )
    #     desempenho_fig.update_layout(
    #         font=dict(color="white"),
    #         xaxis_title="Estado (UF)",
    #         yaxis_title="Média de Notas",
    #     )
    #     desempenho_fig.update_traces(
    #         hovertemplate="<b>Estado (UF)</b>: %{x}<br><b>Média</b>: %{y:.2f}"
    #     )
    #     st.plotly_chart(desempenho_fig, use_container_width=True)

    # # 10. Distribuição por Região
    # with col2:
    #     st.subheader("Distribuição por Região")
    #     regiao_fig = px.histogram(
    #         data_filtered,
    #         x="SG_UF_ESC",
    #         title="Distribuição por Estado (UF)",
    #         color_discrete_sequence=["#6baed6"]
    #     )
    #     regiao_fig.update_layout(
    #         font=dict(color="white"),
    #         xaxis_title="Estado (UF)",
    #         yaxis_title="Quantidade",
    #     )
    #     regiao_fig.update_traces(
    #         hovertemplate="<b>Estado (UF)</b>: %{x}<br><b>Quantidade</b>: %{y}"
    #     )
    #     st.plotly_chart(regiao_fig, use_container_width=True)

    # # 11. Desempenho Geral por Faixa Etária
    # col1, col2 = st.columns(2)
    # with col1:
    #     st.subheader("Desempenho Geral por Faixa Etária")

    #     data_grouped = data_filtered.groupby("TP_FAIXA_ETARIA_DESC")[
    #         ["NU_NOTA_MT", "NU_NOTA_LC", "NU_NOTA_CN", "NU_NOTA_CH", "NU_NOTA_REDACAO"]
    #     ].mean().reset_index()

    #     faixa_etaria_order = list(FAIXA_ETARIA_MAP.values())
    #     data_grouped["TP_FAIXA_ETARIA_DESC"] = pd.Categorical(
    #         data_grouped["TP_FAIXA_ETARIA_DESC"],
    #         categories=faixa_etaria_order,
    #         ordered=True
    #     )
    #     data_grouped = data_grouped.sort_values("TP_FAIXA_ETARIA_DESC")

    #     if len(data_grouped) == 1:
    #         provas_fig = px.bar(
    #             data_grouped.melt(id_vars=["TP_FAIXA_ETARIA_DESC"],
    #                               var_name="Prova",
    #                               value_name="Média"),
    #             x="Prova",
    #             y="Média",
    #             title=f"Desempenho Geral na Faixa Etária: {data_grouped['TP_FAIXA_ETARIA_DESC'].iloc[0]}"
    #         )
    #     else:
    #         provas_fig = px.line(
    #             data_grouped,
    #             x="TP_FAIXA_ETARIA_DESC",
    #             y=["NU_NOTA_MT", "NU_NOTA_LC", "NU_NOTA_CN", "NU_NOTA_CH", "NU_NOTA_REDACAO"],
    #             title="Desempenho Geral nas Provas por Faixa Etária",
    #             color_discrete_sequence=px.colors.sequential.Rainbow
    #         )

    #     provas_fig.update_layout(
    #         font=dict(color="white"),
    #         xaxis_title="Faixa Etária",
    #         yaxis_title="Média das Notas",
    #         xaxis=dict(categoryorder="array", categoryarray=faixa_etaria_order)
    #     )
    #     provas_fig.update_traces(
    #         hovertemplate="<b>Faixa Etária</b>: %{x}<br><b>Média</b>: %{y:.2f}"
    #     )
    #     st.plotly_chart(provas_fig, use_container_width=True)
