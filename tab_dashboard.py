import streamlit as st
import pandas as pd
import datetime


def obter_hora_inteira(data_string, formato="%Y-%m-%d %H:%M:%S"):
    """
    Obtém a hora inteira de uma string de datetime.

    :param data_string: str - A string que representa o datetime.
    :param formato: str - O formato da string de datetime (padrão: "%Y-%m-%d %H:%M:%S").
    :return: int - A hora inteira.
    """
    data = datetime.datetime.strptime(data_string, formato)  # Converte a string para um objeto datetime
    return data.hour  # Retorna a hora inteira

def gerar_analise_fluxo_dia_semana(df, dia, datas_comp):

    dfx = df
    hora_init = obter_hora_inteira(datas_comp[0])
    hora_fim = obter_hora_inteira(datas_comp[1])

    if (hora_init > hora_fim): #Caso tenha alguma mudança de um dia pelo outro, pega o dia todo.
        hora_init,hora_fim = 0,23
      
    dfx = dfx[dfx['Hora'].between(hora_init,hora_fim)]
  
    if (dfx[dfx['Data'] == dia].empty):
        print("Sem contagem para o dia!")
        return None, None

    dia_semana = dfx[dfx['Data'] == dia]['DiaSemana'].iloc[0]
    
    dfx = dfx[dfx['DiaSemana'] == dia_semana]

    dfx['Data'] = dfx['Data'].dt.strftime('%Y-%m-%d')

    dfx = dfx.drop(columns="DiaSemana")
    
     
    dfx_c = dfx[dfx["Sentido"]=="C"]
    dfx_d = dfx[dfx["Sentido"]=="D"]

    mean_c = dfx_c.groupby('Hora')['total_passagens'].mean().reset_index()
    mean_c = mean_c.rename(columns={"total_passagens":"media-"+dia_semana})
    mean_d = dfx_d.groupby('Hora')['total_passagens'].mean().reset_index()
    mean_d = mean_d.rename(columns={"total_passagens":"media-"+dia_semana})


    df_pivot_c = dfx_c.pivot(index='Hora', 
                  columns="Data", 
                  values='total_passagens').reset_index()
    
    df_pivot_d = dfx_d.pivot(index='Hora', 
                  columns="Data", 
                  values='total_passagens').reset_index()
    
    

    xxx = df_pivot_d[[dia]]
    dfx_d = pd.concat([ mean_d,xxx], axis=1)

    xxx = df_pivot_c[[dia]]
    dfx_c = pd.concat([ mean_c,xxx], axis=1)
 
    dfx_c['percentual'] = (dfx_c.iloc[:, 2] / dfx_c.iloc[:, 1] * 100).round(2)
    dfx_d['percentual'] = (dfx_d.iloc[:, 2] / dfx_d.iloc[:, 1] * 100).round(2)


    return dfx_c, dfx_d


def obter_fluxo_local(dfx_acidentes,dfx_fluxo,distancia=10):
    RANGE_DISTANCIA:int = distancia
    
   
    json_df_pairs = []
    resultado = []

    list_brs = dfx_acidentes['br'].unique()

    print(dfx_acidentes['uf'].unique(),dfx_fluxo['UF'].unique())
    
    
    for br in list_brs:
        df2 = dfx_acidentes[dfx_acidentes["br"]==br]
        lista_interacao = df2.to_dict('records')

        for interdicao in lista_interacao:
            

            dfx_fluxo_tmp = dfx_fluxo[dfx_fluxo["BR"]==br]
            dfx_fluxo_tmp = dfx_fluxo_tmp[dfx_fluxo_tmp["UF"]==interdicao["uf"]]
            dfx_fluxo_tmp = dfx_fluxo_tmp[dfx_fluxo_tmp["ano"]==2023]

            km = interdicao["km_interdicao"]

            dfx_fluxo_tmp = dfx_fluxo_tmp[dfx_fluxo_tmp["KM"].between( km-RANGE_DISTANCIA , km+RANGE_DISTANCIA )]
        
            km_contador = 0
            if (not dfx_fluxo_tmp[["KM"]].empty):
                km_contador = dfx_fluxo_tmp[["KM"]].iloc[0,0]
            dfx_fluxo_dia_c,dfx_fluxo_dia_d = gerar_analise_fluxo_dia_semana(dfx_fluxo_tmp,interdicao["data"],[interdicao["hora_extensao_inicio"],interdicao["hora_extensao_fim"]])
            if ((not dfx_fluxo_dia_c is None) and (not dfx_fluxo_dia_d is None)):
                json_df_pairs.append((interdicao,km_contador,(km_contador-km),dfx_fluxo_dia_c,dfx_fluxo_dia_d))
                resultado.append(interdicao)

  
    return json_df_pairs


def exibir_listagem(dfx_acidentes, dfx_fluxo,distancia=10):
    
    dados_filtrados = obter_fluxo_local(dfx_acidentes, dfx_fluxo,distancia)
    # Exibir cada JSON em um expander
    for item, km_contador, distancia, df_c, df_d in dados_filtrados:
        with st.expander(f"{item['uf']} - BR {item['br']} - KM {item['br']}"):
            # Dividir em colunas para melhor visualização
            col1,col2,col3 = st.columns(3)
            
            with col1:
                st.subheader("Informações Básicas")
                st.json({
                    "id_tabela": item['id_tabela'],
                    "BR": item['br'],
                    "KM": item['km_interdicao'],
                    "Data": item['data'],
                    "Hora": item['hora'],
                    "Feridos Leves": item['feridos_leves'],
                    "Feridos Graves": item['feridos_graves'],
                    "Mortos": item['feridos_mortos'],
                    "Janela busca inicio": item['hora_extensao_inicio'],
                    "Janela busca fim": item['hora_extensao_fim'],
                    "Sentido": item['sentido']
                })
                
                st.markdown(f'**Km do contador:** {km_contador}')
                st.markdown(f'**Distância** do local ao contador: {distancia}')
                
            with col2:
                st.subheader("Km Crescente")
                st.dataframe(
                    df_c,
                    hide_index=True
                )
                
            
            with col3:
                st.subheader("Km Decrescente")
                st.dataframe(
                    df_d,
                    hide_index=True
                )

