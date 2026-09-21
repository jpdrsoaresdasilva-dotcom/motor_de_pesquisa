###- Importação das bibliotecas necessárias
import streamlit as st
import pandas as pd
from rapidfuzz import process
df=pd.read_csv("top_1000_imdb_movies.csv")
#
#
#
###Configuração geral
st.set_page_config(
    page_title="Motor de pesquisas de filmes do IMDB", 
    page_icon="🎬", 
    layout="centered"
)
#
#
#
@st.cache_data
def load_and_clean_data():
    df = pd.read_csv("top_1000_imdb_movies.csv")
#
#
#Limpeza 1
if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])
#
#
#Limpeza 2
df['Year of Release'] = df['Year of Release'].astype(str).str.extract(r'(\d{4})')
df['Year of Release'] = pd.to_numeric(df['Year of Release'])
#
#
#Limpeza 3
df = df.drop_duplicates()
    
@st.cache_data
def load_and_clean_data():
    df = pd.read_csv("top_1000_imdb_movies.csv")

    # Limpeza 1
    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])

    # Limpeza 2
    df['Year of Release'] = df['Year of Release'].astype(str).str.extract(r'(\d{4})')
    df['Year of Release'] = pd.to_numeric(df['Year of Release'])

    # Limpeza 3
    df = df.drop_duplicates()

    return df

dataset = load_and_clean_data()
#
#
#
#Estrutura da interface
st.title("Motor de pesquisas de filmes do IMDB")
st.write("Encontra o filme que procuras mesmo sem te lembrares do nome exato!")
#
#
#
#Campo de emtrada
query = st.text_input("De que filme estás à procura?", "")
#
#
#Lógica de pesquisa
if query:
    # RapidFuzz: Procura correspondências com um limite mínimo de 80% de semelhança
    resultados = process.extract(query, dataset["Movie Name"], score_cutoff=80)
    
    if resultados:
        st.subheader("Resultados encontrados:")
        
        for nome, score, index in resultados:
            # Buscar os dados complementares usando o índice do dataset
            dados_filme = dataset.loc[index]
            ano = dados_filme['Year of Release']
            nota = dados_filme['Movie Rating']
            duracao = dados_filme['Watch Time']
            
            # Exibir de forma organizada na interface
            with st.container():
                st.markdown(f"### 🎬 {nome} ({ano})")
                st.write(f"**Semelhança:** {score:.1f}% | **Nota IMDb:** ⭐ {nota}/10 | **Duração:** ⏱️ {duracao} min")
                st.divider()
    else:
        st.warning("Nenhum filme encontrado com esse nível de semelhança. Tenta outro termo!")