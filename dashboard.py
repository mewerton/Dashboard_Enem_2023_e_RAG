import pandas as pd
import streamlit as st
import plotly.express as px
from constants import (FAIXA_ETARIA_MAP, SEXO_MAP, REDE_ENSINO_MAP, 
                       PRESENCA_MAP, ACESSO_INTERNET_MAP, RENDA_FAMILIAR_MAP, 
                       ESCOLARIDADE_PAIS_MAP)

# Configurar o layout em wide
st.set_page_config(page_title="Dashboard ENEM 2023", layout="wide")

def render_dashboard(data, faixa_etaria, sexo, uf, rede):
    # Substituir os valores categóricos pelas descrições
    data["TP_FAIXA_ETARIA_DESC"] = data["TP_FAIXA_ETARIA"].map(FAIXA_ETARIA_MAP)
    data["TP_SEXO_DESC"] = data["TP_SEXO"].map(SEXO_MAP)
    data["TP_ESCOLA_DESC"] = data["TP_ESCOLA"].map(REDE_ENSINO_MAP)
    data["Q025_DESC"] = data["Q025"].map(ACESSO_INTERNET_MAP)
    data["Q006_DESC"] = data["Q006"].map(RENDA_FAMILIAR_MAP)
    data["Q001_DESC"] = data["Q001"].map(ESCOLARIDADE_PAIS_MAP)
    data["Q002_DESC"] = data["Q002"].map(ESCOLARIDADE_PAIS_MAP)

    # Filtrar os dados com base nos filtros
    data_filtered = data[
        (data["TP_FAIXA_ETARIA"].isin(faixa_etaria)) &
        (data["TP_SEXO"].isin(sexo)) &
        (data["SG_UF_ESC"].isin(uf)) &
        (data["TP_ESCOLA"].isin(rede))
    ]

    st.title("Dashboard ENEM 2023")

    # Cálculo das métricas
    total_alunos = len(data_filtered)
    sexo_m = len(data_filtered[data_filtered["TP_SEXO_DESC"] == "Masculino"])
    sexo_f = len(data_filtered[data_filtered["TP_SEXO_DESC"] == "Feminino"])
    rede_predominante = data_filtered["TP_ESCOLA_DESC"].value_counts().idxmax()
    faixa_etaria_comum = data_filtered["TP_FAIXA_ETARIA_DESC"].value_counts().idxmax()

    # Exibir métricas
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total de Alunos", f"{total_alunos:,}")
    col2.metric("Sexo M", f"{sexo_m:,}")
    col3.metric("Sexo F", f"{sexo_f:,}")
    col4.metric("Rede Predominante", rede_predominante)
    col5.metric("Faixa Etária Comum", faixa_etaria_comum)

# Linha separadora
    st.divider()

    # 1. Faixa Etária
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Distribuição por Faixa Etária")
        faixa_etaria_order = list(FAIXA_ETARIA_MAP.values())
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
        faixa_fig.for_each_trace(lambda t: t.update(name="Quantidade"))
        faixa_fig.update_traces(hovertemplate="<b>Faixa Etária</b>: %{x}<br><b>Quantidade</b>: %{y}")
        st.plotly_chart(faixa_fig, use_container_width=True)

    # 2. Média das Notas por Faixa Etária
    with col2:
        st.subheader("Média das Notas por Faixa Etária")
        media_data = data_filtered.groupby("TP_FAIXA_ETARIA_DESC")[["NU_NOTA_MT", "NU_NOTA_LC"]].mean().reset_index()
        media_data = media_data.melt(id_vars=["TP_FAIXA_ETARIA_DESC"], var_name="Prova", value_name="Média")
        media_data["Prova"] = media_data["Prova"].replace({
            "NU_NOTA_MT": "Matemática",
            "NU_NOTA_LC": "Linguagens"
        })
        media_fig = px.bar(
            media_data,
            x="TP_FAIXA_ETARIA_DESC",
            y="Média",
            color="Prova",
            barmode="group",
            title="Média das Notas por Faixa Etária",
            color_discrete_sequence=["#87CEEB", "#20B2AA"]
        )
        media_fig.update_layout(
            xaxis_title="Faixa Etária",
            yaxis_title="Média",
            xaxis=dict(categoryorder="array", categoryarray=faixa_etaria_order),
            font=dict(color="white"),

        )
        media_fig.update_traces(hovertemplate="<b>Faixa Etária</b>: %{x}<br><b>Média</b>: %{y}<br><b>Prova</b>: %{legendgroup}")
        st.plotly_chart(media_fig, use_container_width=True)

    # 3. Média das Notas por Região
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Média das Notas por Estado (UF)")
        regiao_data = data_filtered.groupby("SG_UF_ESC")[["NU_NOTA_MT", "NU_NOTA_LC"]].mean().reset_index()
        regiao_data = regiao_data.melt(id_vars=["SG_UF_ESC"], var_name="Prova", value_name="Média")
        regiao_data["Prova"] = regiao_data["Prova"].replace({
            "NU_NOTA_MT": "Matemática",
            "NU_NOTA_LC": "Linguagens"
        })
        regiao_fig = px.bar(
            regiao_data,
            x="SG_UF_ESC",
            y="Média",
            color="Prova",
            barmode="group",
            title="Média das Notas por Estado (UF)",
            color_discrete_sequence=["#FFD700", "#FF6347"]
        )
        regiao_fig.update_layout(
            xaxis_title="Estado (UF)",
            yaxis_title="Média",
            font=dict(color="white"),

        )
        regiao_fig.update_traces(hovertemplate="<b>Estado (UF)</b>: %{x}<br><b>Média</b>: %{y}<br><b>Prova</b>: %{legendgroup}")
        st.plotly_chart(regiao_fig, use_container_width=True)

    # 4. Distribuição por Sexo
    with col2:
        st.subheader("Distribuição por Sexo")
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

    # 5. Distribuição por Rede de Ensino
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Distribuição por Rede de Ensino")
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

    # 6. Desempenho em Linguagens por Sexo
    with col2:
        st.subheader("Desempenho em Linguagens por Sexo")
        linguagens_data = data_filtered.groupby("TP_SEXO_DESC")["NU_NOTA_LC"].mean().reset_index()
        linguagens_fig = px.bar(
            linguagens_data,
            x="TP_SEXO_DESC",
            y="NU_NOTA_LC",
            title="Média de Linguagens por Sexo",
            color_discrete_sequence=["#FF8C00"]
        )
        linguagens_fig.update_layout(
            xaxis_title="Sexo",
            yaxis_title="Média de Linguagens",
            font=dict(color="white"),
        )
        linguagens_fig.update_traces(hovertemplate="<b>Sexo</b>: %{x}<br><b>Média</b>: %{y}")
        st.plotly_chart(linguagens_fig, use_container_width=True)


    # 7. Desempenho em Matemática por Região
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Desempenho em Matemática por Região")
        matematica_regiao_fig = px.bar(
            data_filtered.groupby("SG_UF_ESC")["NU_NOTA_MT"].mean().reset_index(),
            x="SG_UF_ESC",
            y="NU_NOTA_MT",
            title="Média de Matemática por Estado (UF)",
            color="SG_UF_ESC",
            color_discrete_sequence=px.colors.sequential.Turbo
        )
        matematica_regiao_fig.update_layout(
            font=dict(color="white"),
            xaxis_title="Estado (UF)",
            yaxis_title="Média de Notas",
        )
        matematica_regiao_fig.update_traces(
            hovertemplate="<b>Estado (UF)</b>: %{x}<br><b>Média</b>: %{y:.2f}"
        )
        st.plotly_chart(matematica_regiao_fig, use_container_width=True)

    # 8. Comparação Geral por Sexo
    with col2:
        st.subheader("Comparação Geral das Provas por Sexo")
        media_geral_fig = px.bar(
            data_filtered.groupby("TP_SEXO_DESC")[
                ["NU_NOTA_MT", "NU_NOTA_LC", "NU_NOTA_CN", "NU_NOTA_CH", "NU_NOTA_REDACAO"]
            ].mean().reset_index().melt(id_vars=["TP_SEXO_DESC"]),
            x="TP_SEXO_DESC",
            y="value",
            color="variable",
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
        media_geral_fig.for_each_trace(lambda t: t.update(name=t.name.replace("NU_NOTA_", "")))
        media_geral_fig.update_traces(
            hovertemplate="<b>Sexo</b>: %{x}<br><b>Média</b>: %{y:.2f}"
        )
        st.plotly_chart(media_geral_fig, use_container_width=True)

    # 9. Desempenho por Sexo e Região em Provas
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Desempenho por Sexo e Região")
        desempenho_fig = px.bar(
            data_filtered.groupby(["TP_SEXO_DESC", "SG_UF_ESC"])[
                ["NU_NOTA_MT", "NU_NOTA_LC", "NU_NOTA_CN", "NU_NOTA_CH", "NU_NOTA_REDACAO"]
            ].mean().reset_index().melt(id_vars=["TP_SEXO_DESC", "SG_UF_ESC"]),
            x="SG_UF_ESC",
            y="value",
            color="TP_SEXO_DESC",
            facet_col="variable",
            barmode="group",
            title="Desempenho por Sexo e Região nas Provas",
            color_discrete_sequence=px.colors.sequential.Cividis
        )
        desempenho_fig.update_layout(
            font=dict(color="white"),
            xaxis_title="Estado (UF)",
            yaxis_title="Média de Notas",
        )
        desempenho_fig.update_traces(
            hovertemplate="<b>Estado (UF)</b>: %{x}<br><b>Média</b>: %{y:.2f}"
        )
        st.plotly_chart(desempenho_fig, use_container_width=True)

    # 10. Distribuição por Região
    with col2:
        st.subheader("Distribuição por Região")
        regiao_fig = px.histogram(
            data_filtered,
            x="SG_UF_ESC",
            title="Distribuição por Estado (UF)",
            color_discrete_sequence=["#6baed6"]
        )
        regiao_fig.update_layout(
            font=dict(color="white"),
            xaxis_title="Estado (UF)",
            yaxis_title="Quantidade",
        )
        regiao_fig.update_traces(
            hovertemplate="<b>Estado (UF)</b>: %{x}<br><b>Quantidade</b>: %{y}"
        )
        st.plotly_chart(regiao_fig, use_container_width=True)

    # 11. Desempenho Geral por Faixa Etária
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Desempenho Geral por Faixa Etária")

        data_grouped = data_filtered.groupby("TP_FAIXA_ETARIA_DESC")[
            ["NU_NOTA_MT", "NU_NOTA_LC", "NU_NOTA_CN", "NU_NOTA_CH", "NU_NOTA_REDACAO"]
        ].mean().reset_index()

        faixa_etaria_order = list(FAIXA_ETARIA_MAP.values())
        data_grouped["TP_FAIXA_ETARIA_DESC"] = pd.Categorical(
            data_grouped["TP_FAIXA_ETARIA_DESC"],
            categories=faixa_etaria_order,
            ordered=True
        )
        data_grouped = data_grouped.sort_values("TP_FAIXA_ETARIA_DESC")

        if len(data_grouped) == 1:
            provas_fig = px.bar(
                data_grouped.melt(id_vars=["TP_FAIXA_ETARIA_DESC"],
                                  var_name="Prova",
                                  value_name="Média"),
                x="Prova",
                y="Média",
                title=f"Desempenho Geral na Faixa Etária: {data_grouped['TP_FAIXA_ETARIA_DESC'].iloc[0]}"
            )
        else:
            provas_fig = px.line(
                data_grouped,
                x="TP_FAIXA_ETARIA_DESC",
                y=["NU_NOTA_MT", "NU_NOTA_LC", "NU_NOTA_CN", "NU_NOTA_CH", "NU_NOTA_REDACAO"],
                title="Desempenho Geral nas Provas por Faixa Etária",
                color_discrete_sequence=px.colors.sequential.Rainbow
            )

        provas_fig.update_layout(
            font=dict(color="white"),
            xaxis_title="Faixa Etária",
            yaxis_title="Média das Notas",
            xaxis=dict(categoryorder="array", categoryarray=faixa_etaria_order)
        )
        provas_fig.update_traces(
            hovertemplate="<b>Faixa Etária</b>: %{x}<br><b>Média</b>: %{y:.2f}"
        )
        st.plotly_chart(provas_fig, use_container_width=True)
