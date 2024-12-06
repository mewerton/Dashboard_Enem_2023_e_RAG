**Dashboard ENEM 2023**

Este projeto apresenta um **dashboard interativo** para análise dos dados do ENEM 2023. Ele foi desenvolvido utilizando **Streamlit** e permite a exploração dos dados demográficos, desempenho acadêmico, e características socioeconômicas dos participantes.

## **Funcionalidades**
- Visualizações interativas com gráficos dinâmicos.
- Filtros por faixa etária, sexo, estado (UF), e rede de ensino.
- Resumo de métricas importantes, como quantidade total de participantes, distribuição por sexo e renda familiar.
- Gráficos intuitivos que mostram tendências de desempenho e distribuições.

---

## **Pré-requisitos**
Antes de iniciar, verifique se você possui as ferramentas abaixo instaladas:
- **Python 3.8+**
- **Git** (opcional, para clonar o repositório)
- **Virtualenv** (opcional, para criar um ambiente virtual)

---

## **Instalação**
Siga os passos abaixo para configurar o projeto localmente:

### **1. Clone este repositório**
\`\`\`bash
git clone https://github.com/mewerton/enem2023.git
cd enem2023
\`\`\`

### **2. Crie e ative um ambiente virtual (opcional, mas recomendado)**
\`\`\`bash
# Criação do ambiente virtual
python -m venv venv

# Ativação
# No Windows:
venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate
\`\`\`

### **3. Instale as dependências**
\`\`\`bash
pip install -r requirements.txt
\`\`\`

---

## **Como usar**
1. Certifique-se de que o arquivo de dataset está presente na pasta \`database\`.
   - Por padrão, o arquivo processado (Parquet) deve ser:  
     \`database/MICRODADOS_ENEM_2023_filtered_PQ.parquet\`
   - Você também pode usar o arquivo CSV original configurando o \`data_loader.py\`.

2. Inicie o Streamlit:
   \`\`\`bash
   streamlit run app.py
   \`\`\`

3. O dashboard estará disponível no navegador, geralmente no endereço:  
   [http://localhost:8501](http://localhost:8501)

---

## **Estrutura do Projeto**
\`\`\`
enem2023/
├── database/                # Pasta para os datasets
├── app.py               # Arquivo principal para executar o projeto
├── dashboard.py         # Geração e exibição do dashboard
│── data_loader.py       # Carregamento do dataset
│── sidebar.py           # Filtros interativos da barra lateral
│── constants.py         # Mapas de constantes e descrições dos dados
├── .gitignore               # Arquivos ignorados pelo Git
├── README.md                # Documentação do projeto
├── requirements.txt         # Dependências do projeto
\`\`\`

---

## **Contribuindo**
Contribuições são bem-vindas!  
Sinta-se à vontade para abrir **issues** ou enviar **pull requests**.

---

## **Licença**
Este projeto está licenciado sob a licença [MIT](https://opensource.org/licenses/MIT).  

---

## **Contato**
Criado por **Mewerton Melo**.  

