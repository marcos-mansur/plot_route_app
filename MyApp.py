import pandas as pd
import folium
import streamlit as st
from streamlit_folium import folium_static
import os
from folium.plugins.beautify_icon import BeautifyIcon

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


def plota_mapa(m, df_rotas, rota, cor, icone_tipo):
    """ retorna um mapa com os pontos, linhas retas para rota e um círculo no ponto inicial"""
    # reseta a var coord_anterior para não plotar a rota do último ponto de volta ao primeiro
    coord_anterior = []
    k=0
    for i, row in df_rotas[rota].iterrows():
        k += 1
        if icone_tipo == 'Number by stop order':
            icon = BeautifyIcon(number=round(k),
                        border_color=cor,
                        text_color=cor)
        else:
            icon = folium.Icon(color=cor)

        # plota os pontos de entrega
        folium.Marker([row['Lat'],row['Long']],
                      popup="Ponto " + str(i)+ ": " + str([row['Lat'],
                                                           row['Long']]),
                      icon= icon,
                      ).add_to(m)
        # plota as rotas
        if len(coord_anterior)==0:
            folium.CircleMarker((row['Lat'],row['Long']),
                                color=cor,
                                fill=True,
                                radius = 20,
                                popup="Ponto inicial").add_to(m)
        coord_anterior.append((row['Lat'],row['Long']))

    folium.vector_layers.PolyLine(coord_anterior,
                                  color=cor).add_to(m)

    return m


st.set_page_config(page_icon='random',
                   initial_sidebar_state='expanded',
                   menu_items={
'About': "You should hire me, I need a job and I make cool "
         "web apps and lots of machine learning. "
         "\nhttps://github.com/marcos-mansur "
         "\nhttps://www.linkedin.com/in/marcos-mansur-550a59173/"}
)

# salva o endereço do diretório
# cwd = os.getcwd()
# carrega os dados
df = pd.read_csv('https://raw.githubusercontent.com/marcos-mansur/plot_route_app/main/Data/Data.csv',  #os.path.join(cwd, 'Data\Data.csv'),
                 header=0,
                 index_col=0)
# separa os dataframes por rota
df_rotas = split_df_rotas(df)

# Título
st.title('Plot Routes on map')
st.write('This app plots routes from a data set of random locations '
         'at São Paulo - Brazil. It works for any dataset with columns named'
         '"Rota" (route name), "Lat" (latitude) and "Long" (longitude).')
st.write('Select how many and which routes do you want to plot in the sidebar at the left.')
# select slide na sidebar para definir o número de rotas a serem plotadas
n_rotas = st.sidebar.slider('How many routes do you wish to plot?',
                            max_value = df['Rota'].nunique())

# botão de selecionar o tipo de icone
icone_tipo = st.sidebar.radio('Select the icon type: ',
                              ['Pin', 'Number by stop order'],
                              )

# create list to receive the routes the must be ploted
rota_select = [0 for x in range(df["Rota"].nunique())]
# lista de cores para os marcadores e linhas
cores = ['teal', 'red', 'blue', 'gray', 'darkred',
        'purple', 'orange', 'beige', 'green',
        'darkgreen', 'lightgreen', 'darkblue', 'black']

# automatiza a sidebar com os seletores de rotas de acordo com a quantidade de rotas a plotar definida na var "n_rotas"
for i in range(n_rotas):
    rota_select[i] = st.sidebar.selectbox(f'Select the route: ',
                                          df['Rota'].unique(),
                                          key=str(i)+"tico")
    st.sidebar.write(str(rota_select[i]) + " color: " + cores[rota_select[i]], key=cores[int(rota_select[i])])
# cria o mapa
m = folium.Map(location=[df['Lat'].mean(),df['Long'].mean()],
               zoom_start=11)
# plota as rotas
for j in [x for x in rota_select if x>0]:
    m = plota_mapa(m, df_rotas, j, cores[j],icone_tipo)

# plota mapa
folium_static(m)