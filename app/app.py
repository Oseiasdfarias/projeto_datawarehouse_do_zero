import os
import pandas as pd
import streamlit as st
import plotly.express as px
from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Obter as variáveis do arquivo .env
DB_HOST = os.getenv('DB_HOST_PROD')
DB_PORT = os.getenv('DB_PORT_PROD')
DB_NAME = os.getenv('DB_NAME_PROD')
DB_USER = os.getenv('DB_USER_PROD')
DB_PASS = os.getenv('DB_PASS_PROD')
DB_SCHEMA = os.getenv('DB_SCHEMA_PROD')

# Criar a URL de conexão do banco de dados
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"  # noqa: E501

# Criar o engine de conexão com o banco de dados
engine = create_engine(DATABASE_URL)


# Consultar os dados da tabela dm_commodities
def get_data():
    query = """
    SELECT
        data,
        simbolo,
        valor_fechamento,
        acao,
        quantidade,
        valor,
        ganho
    FROM
        public.dm_commodities;
    """
    try:
        df = pd.read_sql(query, engine)
        return df
    except ProgrammingError as e:
        st.error(f"Erro ao acessar a tabela 'dm_commodities' no schema '{DB_SCHEMA}': {e}")  # noqa: E501
        return pd.DataFrame()  # Retorna um DataFrame vazio em caso de erro


# Configurar a página do Streamlit
st.set_page_config(page_title='Dashboard de Commodities')


# Título do Dashboard
st.title("Dashboard de Commodities")

# Descrição
st.write("""
Este dashboard mostra os dados de commodities e suas transações.
""")

# Obter os dados
df = get_data()

st.dataframe(df)


st.subheader('Gráficos das Commodities | 2024-06-10')
col1, col2 = st.columns(2)
fig1 = px.bar(df, x='simbolo', y='quantidade', text_auto='.2s',
              title="Quantidade de commodities no dia")
col1.plotly_chart(fig1)

fig2 = px.bar(df, x='simbolo', y='ganho', text_auto='.2s',
              title="Ganho no dia por commodities")
col2.plotly_chart(fig2)
