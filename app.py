# app.py
import streamlit as st
import pandas as pd
from data_fetcher import fetch_atletico_games

st.set_page_config(page_title="Atlético Stats Viewer", layout="wide", page_icon="⚽")
st.title("⚽ Atlético Stats Viewer - Dados Reais")

# ------------------------
# Buscar dados reais
# ------------------------
try:
    games_df = fetch_atletico_games()
except Exception as e:
    st.error(f"Erro ao buscar dados: {e}")
    st.stop()

ultimo_jogo = games_df.iloc[0]

# ------------------------
# Layout principal
# ------------------------
col_left, col_right = st.columns([1,2])

# ------------------------
# Sliders à esquerda
# ------------------------
with col_left:
    st.header("⚙️ Estatísticas do Último Jogo")

    st.subheader("Ataque")
    st.slider("xG Atlético", 0.0, 3.0, float(ultimo_jogo['xG_Atlético']))
    if st.button("ℹ️", key="info_xg"):
        st.info("xG (Gols Esperados): estima a quantidade de gols que a equipe deve marcar baseado nas chances criadas.")

    st.slider("Remates", 0, 25, int(ultimo_jogo['Remates']))
    if st.button("ℹ️", key="info_remates"):
        st.info("Remates: número total de chutes ao gol por jogo.")

    st.subheader("Posse")
    st.slider("Posse (%)", 0, 100, int(ultimo_jogo['Posse']))
    if st.button("ℹ️", key="info_posse"):
        st.info("Posse de bola: percentual de tempo que a equipe manteve a posse da bola.")

    st.subheader("Resultado")
    st.text(f"{ultimo_jogo['Resultado']} ({ultimo_jogo['Gols_Atlético']} - {ultimo_jogo['Gols_Adversário']})")

# ------------------------
# Próximo jogo à direita (informações simples)
# ------------------------
with col_right:
    st.header("📅 Últimos Jogos")

    for i, row in games_df.iterrows():
        st.write(f"{row['Data'].date()} vs {row['Adversário']} - Resultado: {row['Resultado']}")
