import streamlit as st
import os
import toml
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate


# Função para inicializar o chatbot no corpo do dashboard
def render_chatbot():
    # Carregar a chave da API do arquivo config.toml
    try:
        config = toml.load("config.toml")
        API_KEY = config.get("API_KEY")
    except FileNotFoundError:
        st.error("Arquivo config.toml não encontrado.")
        return
    except Exception as e:
        st.error(f"Erro ao carregar config.toml: {e}")
        return

    if API_KEY:
        os.environ['GROQ_API_KEY'] = API_KEY
    else:
        st.error("API Key não encontrada no arquivo config.toml.")

    # Variável de estado para armazenar o histórico de conversa
    if "chat_historico" not in st.session_state:
        st.session_state.chat_historico = []

    def process_message():
        # Processar a mensagem do chatbot
        pergunta_usuario = st.session_state.chat_input

        if pergunta_usuario:
            try:
                # Instanciar o modelo Groq com a Llama
                chat = ChatGroq(model='llama-3.1-70b-versatile')

                # Criar regras básicas para o chatbot
                regras = """
                    Você é Carly, uma assistente amigável e inteligente. Responda de forma clara e objetiva.
                    Não cumprimente o usuário várias vezes e evite respostas muito longas.
                """
                historico = "\n".join(st.session_state.chat_historico)
                template = ChatPromptTemplate.from_messages([
                    ('system', regras),
                    ('user', historico + f"\nUsuário: {pergunta_usuario}")
                ])
                chain = template | chat
                resposta = chain.invoke({'input': pergunta_usuario}).content
                resposta = resposta.strip() if resposta.strip() else "Desculpe, não entendi sua pergunta."

                # Adicionar a interação ao histórico
                st.session_state.chat_historico.append(f"Usuário: {pergunta_usuario}")
                st.session_state.chat_historico.append(f"**Carly:** {resposta}")
            except Exception as e:
                st.session_state.chat_historico.append(f"Erro ao processar: {e}")

        # Limpar o input
        st.session_state.chat_input = ""

    # Layout do chatbot no corpo do dashboard
    st.subheader("Carly - Assistente Virtual")
    input_col, button_col = st.columns([5, 1])

    # Campo de entrada de texto
    with input_col:
        st.text_input("Digite sua pergunta:", key="chat_input", on_change=process_message)

    # Botão de envio
    with button_col:
        st.button("Enviar", on_click=process_message)

    # Exibir o histórico de conversa
    st.markdown("### Histórico de Conversa")
    for msg in st.session_state.chat_historico:
        st.write(msg)
