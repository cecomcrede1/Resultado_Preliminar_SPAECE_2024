#-------------------
# IMPORTAR BIBLIOTECAS
#-------------------

import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import os
from dotenv import load_dotenv
import plotly.graph_objects as go
import io
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

#-------------------
# CONFIGURAR PÁGINA
#-------------------

# Configuração para tela cheia (modo wide)
st.set_page_config(layout="wide", page_title="Resultados Preliminares SPAECE", page_icon="spaece.png")
st.info("Para melhor visualização, recomendamos usar o tema claro. Você pode alterar o tema nas configurações do Streamlit (Menu (⋮) > Settings > Theme).")

# Adicionando Kanit via CSS no Streamlit
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;700&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Kanit', sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)
#-------------------
# AUTENTICAÇÃO
#-------------------
#USERS = {"crede01": "0", "aquiraz": "0", "caucaia": "0", "eusebio": "0","guaiuba":"0","itaitinga":"0","maracanau":"0","maranguape":"0","pacatuba":"0"}
USERS ={"crede01": "x3f7h9", "aquiraz": "p8l2m5", "caucaia": "k4t9y7", "eusebio": "m1n5z8", "guaiuba": "h2v8j6", "itaitinga": "q9w6x4", "maracanau": "r3y7m1", "maranguape": "n5t4v9", "pacatuba": "j8k2h5"}
MUNICIPIOS = {"crede01": "Crede 01", "aquiraz": "AQUIRAZ", "caucaia": "CAUCAIA", "eusebio": "EUSEBIO", "guaiuba":"GUAIUBA","itaitinga":"ITAITINGA", "maracanau":"MARACANAU", "maranguape":"MARANGUAPE", "pacatuba":"PACATUBA" }

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    col1, col2, col3 = st.columns([1,8,1])
    with col2:
            st.image("banner.png", use_container_width=True)
    
    st.title("Entre")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if USERS.get(username) == password:
            st.session_state.update({"authenticated": True, "username": username, "municipio": MUNICIPIOS.get(username, "Desconhecido")})
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos!")
else:
    usuario = st.session_state["username"]
    municipio_usuario = st.session_state["municipio"]

    st.sidebar.image("spaece.png", width=250)
    
    col1, col2, col3 = st.columns([1,8,1])
    with col2:
            st.image("banner.png", use_container_width=True)

    # col1, col2, col3 = st.columns([0.3,0.3,0.3])
    
    # with col1:
    #     st.image("logo_governo_preto_SEDUC.png", width=250)
        
    # with col2:
    #     st.image("crede.png", width=300)   
        
    # with col3:
    #     st.image("cecom.png", width=230)
    
    st.markdown('---')
    st.markdown(f"<h3 style='font-family: Kanit; font-size: 20px; font-weight: bold;'>Seja bem-vindo gestor de {municipio_usuario}!</h3>", unsafe_allow_html=True)
    
    st.markdown(
        "<h3 style='font-family: Kanit; font-size: 25px; font-weight: normal;'>Baixe aqui os resultados preliminares do SPAECE 2024 organizados por escola, por turma ou por Estudante.</h3>",
        unsafe_allow_html=True
    )

    # Adicionar linha divisória
    st.write("---")
    #-------------------
    # EXIBIÇÃO DE CÓDIGO CONDICIONAL POR USUÁRIO
    #-------------------
    if usuario == "crede01":
        st.subheader("Visão Administrativa")
        st.write("Este conteúdo é visível apenas para usuários da CREDE 01.")
        st.markdown(
        f"<h3 style='font-family: Kanit; font-size: 20px; font-weight: bold;'>Município: {municipio_usuario}</h3>",
        unsafe_allow_html=True
        )
        
        st.markdown(
            f"<h3 style='font-family: Kanit;color: red; font-size: 50px;text-align: left; font-weight: bold;'>Conteúdo Exclusivo!</h3>",
            unsafe_allow_html=True
        )
#-------------------
# IMPORTA OS DADOS (df)
#-------------------

    df = pd.read_csv("df_final.csv")
    # st.text('df')
    # st.dataframe(df, height=400, width=1000)
    
#-------------------
# FILTROS ()
#-------------------
    # FILTROS ESPECIAIS PARA CREDE01
    if st.session_state.get("username") == "crede01":
        municipios_disponiveis = ["Todos"] + sorted(df["MUNICÍPIO"].unique().tolist())
        municipio_filtro = st.sidebar.selectbox("Selecione o Município", municipios_disponiveis)
        if municipio_filtro != "Todos":
            df = df[df["MUNICÍPIO"] == municipio_filtro]
    else:
        df = df[df["MUNICÍPIO"] == municipio_usuario]
    #-------------------
    # FILTROS GERAIS
    escolas_disponiveis = ["Todas"] + sorted(df["ESCOLA"].unique().tolist())
    escola_filtro = st.sidebar.selectbox("Selecione a Escola", escolas_disponiveis)
    
    df_filtrado_escola = df[df["ESCOLA"] == escola_filtro]
    # Filtrando etapas
    etapas_disponiveis = ["Todas"] + sorted(df_filtrado_escola["ETAPA"].unique().tolist())
    
    etapa_filtro = st.sidebar.selectbox("Selecione a Etapa", etapas_disponiveis)

    df_filtrado_etapa = df_filtrado_escola if etapa_filtro == "Todas" else df_filtrado_escola[df_filtrado_escola["ETAPA"] == etapa_filtro]
    
    # Filtrando turmas
    turmas_disponiveis = ["Todas"] + sorted(df_filtrado_etapa["TURMA"].unique().tolist())
    turma_filtro = st.sidebar.selectbox("Selecione a Turma", turmas_disponiveis)

    # Filtrando estudantes
    df_filtrado_turma = df_filtrado_escola if turma_filtro == "Todas" else df_filtrado_escola[df_filtrado_escola["TURMA"] == turma_filtro]
    estudantes_disponiveis = ["Todos"] + sorted(df_filtrado_turma["ESTUDANTE"].unique().tolist())
    estudante_filtro = st.sidebar.selectbox("Selecione o Estudante", estudantes_disponiveis)

    # Filtrando componentes curriculares
    componentes_disponiveis = ["Todos"] + sorted(df_filtrado_turma["COMPONENTE CURRICULAR"].unique().tolist())
    componente_filtro = st.sidebar.selectbox("Selecione o Componente Curricular", componentes_disponiveis)
    




    # Botão para aplicar os filtros
    #if st.sidebar.button("Aplicar Filtros"):
    # Aplicando todos os filtros
    df_final = df[
        ((df["ESCOLA"] == escola_filtro) | (escola_filtro == "Todas")) &
        ((df["ETAPA"] == etapa_filtro) | (etapa_filtro == "Todas")) &
        ((df["TURMA"] == turma_filtro) | (turma_filtro == "Todas")) &
        ((df["ESTUDANTE"] == estudante_filtro) | (estudante_filtro == "Todos")) &
        ((df["COMPONENTE CURRICULAR"] == componente_filtro)| (componente_filtro == "Todos"))
    ].copy()
    
    st.dataframe(data=df_final,hide_index=True)
    
    # Converter DataFrame para Excel em memória
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_final.to_excel(writer, index=False, sheet_name='Dados')
        writer.close()  # Certifique-se de fechar o writer antes de ler o conteúdo
        processed_data = output.getvalue()

    # Criar botão para download
    st.download_button(
        label="Baixar Tabela de Dados em Excel",
        data=processed_data,
        file_name='tabela_de_dados.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
        
    st.markdown("---")

        #RESUMO
    st.markdown(
        "<h3 style='font-family: Kanit; font-size: 20px; font-weight: bold;'>RESUMO</h3>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<h3 style='font-family: Kanit; font-size: 18px; font-weight: bold;'>Proficiência:</h3>",
        unsafe_allow_html=True
    )
    
    # Filtrar apenas os estudantes avaliados
    df_avaliados = df_final[df_final['AVALIADO'] == 'SIM']
    
    # Calcular a média das proficiências
    media_proficiencia = int(df_avaliados['PROFICIENCIA MÉDIA'].astype(float).mean())

    st.metric(label="Média dos alunos presentes", value=media_proficiencia)
    
    st.markdown(
        "<h3 style='font-family: Kanit; font-size: 18px; font-weight: bold;'>Frequência:</h3>",
        unsafe_allow_html=True
    )

    avaliados = df_final[df_final['AVALIADO'] == 'SIM']['ESTUDANTE'].nunique()
    n_avaliados = df_final[df_final['AVALIADO'] == 'NÃO']['ESTUDANTE'].nunique()
    
    # Criar três colunas
    col1, col2, col3 = st.columns(3)

    # Exibir os dados nas colunas
    col1.metric(label="Total de Estudantes", value=avaliados+n_avaliados)
    col2.metric(label="Avaliados", value=avaliados)
    col3.metric(label="Não Avaliados", value=n_avaliados)

    # Definir a ordem desejada das faixas
    # Definir a ordem desejada das faixas
    ordem_faixas = [
        "ALFABETIZAÇÃO INCOMPLETA", "MUITO CRÍTICO", "CRÍTICO", "ABAIXO DO BÁSICO", 
        "BÁSICO", "INTERMEDIÁRIO", "SUFICIENTE", "DESEJÁVEL", "ADEQUADO", 
        "PROFICIENTE", "AVANÇADO"
    ]
    
    # Definir cores personalizadas para cada faixa
    cores_faixas = {
        "ALFABETIZAÇÃO INCOMPLETA": "#D32F2F",  # Vermelho escuro
        "MUITO CRÍTICO": "#F44336",             # Vermelho
        "CRÍTICO": "#FF5722",                   # Laranja avermelhado
        "ABAIXO DO BÁSICO": "#FF9800",          # Laranja
        "BÁSICO": "#FFC107",                    # Amarelo escuro
        "INTERMEDIÁRIO": "#FFEB3B",             # Amarelo claro
        "SUFICIENTE": "#8BC34A",                # Verde claro
        "DESEJÁVEL": "#4CAF50",                 # Verde médio
        "ADEQUADO": "#388E3C",                  # Verde escuro
        "PROFICIENTE": "#2196F3",               # Azul
        "AVANÇADO": "#673AB7"                   # Roxo
    }
    
    # Contar a quantidade de estudantes únicos para cada faixa (somente os avaliados "SIM")
    faixa_counts = df_final[df_final['AVALIADO'] == 'SIM'].groupby('FAIXAS')['ESTUDANTE'].nunique()
    
    # Reorganizar os dados conforme a ordem desejada, removendo faixas com valor 0
    faixa_counts = {faixa: faixa_counts.get(faixa, 0) for faixa in ordem_faixas}
    faixa_counts = {faixa: count for faixa, count in faixa_counts.items() if count > 0}  # Remove os zeros
    
    
    # Criar colunas dinamicamente com as faixas filtradas
    cols = st.columns(len(faixa_counts)) 
    
    # Exibir cada faixa na ordem definida
    #for col, (faixa, count) in zip(cols, faixa_counts.items()):
    #    col.metric(label=faixa, value=count)

    # Criar DataFrame para o gráfico
    df_faixas = pd.DataFrame(list(faixa_counts.items()), columns=["Faixa", "Quantidade"])
    
    # Criar gráfico de barras
    fig = px.bar(df_faixas, x="Faixa", y="Quantidade", text="Quantidade",
                 title="Distribuição de Estudantes por Faixa",
                 labels={"Faixa": "Faixa de Proficiência", "Quantidade": "Número de Estudantes"},
                 color="Faixa",
                 color_discrete_map=cores_faixas) # Adiciona cores diferentes para cada faixa
    
    fig.update_traces(textposition="outside")  # Exibir valores fora das barras

    st.plotly_chart(fig)
        
    if st.sidebar.button("Sair"):
        st.session_state.clear()
        st.rerun()
