import os
import streamlit as st
from langchain_groq import ChatGroq
from configparser import ConfigParser

import tomli

# Função para carregar a chave API do arquivo config.toml
def carregar_chave_api():
    with open("config.toml", "rb") as f:
        config = tomli.load(f)
    return config["API_KEY"]

# Função genérica para análise das tabelas
def analisar_tabelas(titulo, tabelas):
    """
    Analisa uma ou mais tabelas fornecidas e gera um resumo com a LLM.

    Args:
    - titulo (str): Título ou contexto da análise, para exibir no prompt.
    - tabelas (list of tuples): Lista de tabelas no formato [(nome_tabela, df), ...].

    Returns:
    - str: Resultado da análise gerada pela LLM.
    """
    try:
        # Carregar a chave da API
        API_KEY = carregar_chave_api()
        if API_KEY:
            os.environ['GROQ_API_KEY'] = API_KEY
        else:
            return "Erro: API Key não encontrada no arquivo config.toml."

        # Criar o modelo LLM
        chat = ChatGroq(model='llama-3.1-70b-versatile')

        # Preparar o prompt
        prompt = f"Analise as tabelas a seguir para o contexto: {titulo}\n\n"
        for nome_tabela, tabela in tabelas:
            prompt += f"Tabela: {nome_tabela}\n{tabela.to_string(index=False)}\n\n"

        prompt += "Você é um Assistente de Ingeligência virtual analisando os dados para um Analista de Dados que trabalha em uma instituição de ensino que tem como sua principal função oferecer cursos e programas de formação profissional para a indústria, contribuindo para a qualificação da mão de obra e o desenvolvimento tecnológico do setor. Faça insights com base nos dados apresentados e que seja do interesse desse analista."

        # Enviar para a LLM como uma string
        resposta = chat.invoke(prompt)  # Passar o prompt diretamente como string
        return resposta.content if resposta.content.strip() else "Não foi possível gerar uma análise no momento."
    except Exception as e:
        return f"Erro ao processar a análise: {str(e)}"

# Função para criar um botão de análise
def botao_analise(titulo, tabelas, botao_texto="Analisar com Inteligência Artificial", key=None):
    """
    Exibe um botão e, ao clicar, analisa as tabelas fornecidas.

    Args:
    - titulo (str): Título ou contexto da análise.
    - tabelas (list of tuples): Lista de tabelas no formato [(nome_tabela, df), ...].
    - botao_texto (str): Texto do botão a ser exibido.
    - key (str): Chave única para o botão.

    Returns:
    - None
    """
    if st.button(botao_texto, key=key):
        resultado_analise = analisar_tabelas(titulo, tabelas)
        st.markdown(f"### Resultado da Análise:\n{resultado_analise}")
