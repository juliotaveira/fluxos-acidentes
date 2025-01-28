import streamlit as st
import folium
from streamlit_folium import st_folium

def show_mapa(df_filtrado):
    """
    Exibe o conteúdo da aba Mapa
    """
    # Criar mapa com os dados filtrados
    st.subheader("Distribuição Geográfica das Vendas")
    
    # # Agrupar dados por cidade para o mapa
    # dados_mapa = df_filtrado.groupby(['Cidade', 'latitude', 'longitude']).agg({
    #     'Valor': ['sum', 'count']
    # }).reset_index()
    # dados_mapa.columns = ['Cidade', 'latitude', 'longitude', 'Valor_Total', 'Num_Vendas']
    
    # # Criar mapa base
    # mapa = folium.Map(
    #     location=[dados_mapa['latitude'].mean(), dados_mapa['longitude'].mean()],
    #     zoom_start=4
    # )
    
    # # Adicionar marcadores
    # for idx, row in dados_mapa.iterrows():
    #     folium.Marker(
    #         [row['latitude'], row['longitude']],
    #         popup=f"""
    #         <b>{row['Cidade']}</b><br>
    #         Valor Total: R$ {row['Valor_Total']:,.2f}<br>
    #         Número de Vendas: {row['Num_Vendas']}
    #         """,
    #         tooltip=row['Cidade']
    #     ).add_to(mapa)
    
    # # Exibir mapa
    # st_folium(mapa, width=800, height=500)
    
    # # Tabela de resumo por cidade
    # st.subheader("Resumo por Cidade")
    # st.dataframe(
    #     dados_mapa,
    #     column_config={
    #         "Valor_Total": st.column_config.NumberColumn(
    #             "Valor Total",
    #             format="R$ %.2f"
    #         ),
    #         "Num_Vendas": st.column_config.NumberColumn(
    #             "Número de Vendas"
    #         )
    #     },
    #     hide_index=True
    # )