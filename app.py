import streamlit as st
import pandas as pd
import numpy as np
import datetime
import tab_dashboard
import tab_mapa

# Configuração da página
st.set_page_config(page_title="Relação Acidentes e Fluxos", layout="wide")



df_acidentes = pd.read_parquet("acidentes_app.parquet")
df_fluxo = pd.read_parquet("fluxo_app.parquet")
print(df_fluxo["UF"].unique())


# Inicializar o session_state se necessário
if 'df_filtrado' not in st.session_state:
    st.session_state.df_filtrado = df_acidentes.copy()  # df é seu DataFrame original


# Título principal
st.title('Dashboard de Acidentes e Fluxo')



# Sidebar para filtros
st.sidebar.header('Filtros')





# Filtro de data
data_min, data_max = st.sidebar.date_input(
    'Intervalo de Datas',
    [df_acidentes['data'].min(), df_acidentes['data'].max()],
    min_value=df_acidentes['data'].min(),
    max_value=df_acidentes['data'].max()
)

# # Filtros categóricos
uf = st.sidebar.multiselect(
    'UF',
    options=df_acidentes['uf'].unique(),
    default=df_acidentes['uf'].unique(),
    key='uf_filtro'  # chave para acessar o valor depois
)

br = st.sidebar.multiselect(
    'BR',
    options=sorted(df_acidentes['br'].unique()),
    key='br_filtro'  # chave para acessar o valor depois
)

distancia_busca = st.sidebar.slider(
    'Distância Acidente e ponto contagem',
    min_value=0,
    max_value=100,
    value=10 ,key="distancia_filtro" # valor inicial
)

# Método 2: Usando container
with st.sidebar.container():
    st.write("Considerar apenas com:")
    op_ferido_leve = st.checkbox('Feridos Leves', key="feridos_leves_filtro") #valores True ou False
    op_ferido_graves = st.checkbox('Feridos Graves', key="feridos_graves_filtro")
    op_mortos = st.checkbox('Mortos', key="mortos_filtro")

# Criar abas
tab1, tab2 = st.tabs(["📈 Dashboard", "🗺️ Mapa"])
                
# Botão de Aplicar
if st.sidebar.button('Aplicar Filtros'):
    # Aplicar os filtros apenas quando o botão for clicado
    mask = (
        df_acidentes['uf'].isin(st.session_state.uf_filtro) &
        df_acidentes['br'].isin(st.session_state.br_filtro) &
        (
            (df_acidentes['feridos_leves'] > 0) 
            if st.session_state.feridos_leves_filtro 
            else True
        ) &
        (
            (df_acidentes['feridos_graves'] > 0) 
            if st.session_state.feridos_graves_filtro 
            else True
        ) &
        (
            (df_acidentes['feridos_mortos'] > 0) 
            if st.session_state.mortos_filtro 
            else True
        )

    )
    st.session_state.df_filtrado = df_acidentes.loc[mask]
    st.session_state.filtros_aplicados = True  # opcional: flag para indicar que filtros foram aplicados

    tab_dashboard.exibir_listagem(st.session_state.df_filtrado,df_fluxo,st.session_state.distancia_filtro )
    



with tab1:
    #tab_dashboard.show_dashboard(st.session_state.df_filtrado,df_fluxo )
    pass

with tab2:
    tab_mapa.show_mapa(st.session_state.df_filtrado )

if st.session_state.get('filtros_aplicados', False):
    st.success('Filtros aplicados com sucesso!')

