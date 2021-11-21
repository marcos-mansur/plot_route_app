import pandas as pd
import folium
import streamlit as st
from streamlit_folium import folium_static
import os

# salva o endereço do diretório
cwd = os.getcwd()
# carrega os dados
df = pd.read_csv(os.path.join(cwd, 'Data\HBR.csv'), header=0, sep=';', decimal=',')


@st.cache
def split_df_rotas(df):
    """ Retorna uma lista com os dados separados por rota"""
    # lista com número das rotas
    rotas_unique = df['Rota'].unique()
    # cria lista para receber os dfs com pontos de cada rota como itens
    df_rotas = ["" for x in range(len(rotas_unique)+1)]
    # preenche a lista com os dfs separados por rota
    for j in range(len(rotas_unique)+1):
        df_rotas[j] = df[df['Rota'] ==j]
    return df_rotas


def plota_mapa(m, df_rotas, rota, cor):
    """ retorna um mapa com os pontos, linhas retas para rota e um círculo no ponto inicial"""
    # reseta a var coord_anterior para não plotar a rota do último ponto de volta ao primeiro
    coord_anterior = 0

    for i, row in df_rotas[rota].iterrows():
        # plota os pontos de entrega
        folium.Marker([row['Lat'],row['Long']],
                      popup="Ponto " + str(i)+ ": " +str([row['Lat'],row['Long']]),
                      icon=folium.Icon(color=cor)).add_to(m)
        # plota as rotas
        try:
            folium.vector_layers.PolyLine([(row['Lat'],row['Long']),coord_anterior], color=cor).add_to(m)
        except:
            pass
        if coord_anterior == 0:
            folium.CircleMarker((row['Lat'],row['Long']),
                            color="green",
                            fill=True,
                            radius = 20,
                            popup="Ponto inicial").add_to(m)
        coord_anterior = (row['Lat'],row['Long'])
    return m

df_rotas = split_df_rotas(df)
st.title('Plotar Rotas no mapa')
m = folium.Map(location=[df['Lat'].mean(),df['Long'].mean()], zoom_start=11)
rota_select = st.selectbox('Escolha a rota',df['Rota'].unique())

# adicionar mais uma rota
add_rota = st.checkbox('Adicionar +1 rota')
if add_rota:
    rota_select2 = st.selectbox('Escolha a rota extra', df['Rota'].unique())
    m = plota_mapa(m, df_rotas, rota_select2, 'red')

# plota mapa
folium_static(plota_mapa(m, df_rotas,rota_select,'black'))

