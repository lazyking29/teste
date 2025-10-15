# app.py
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from data_fetcher import fetch_atletico_games

st.set_page_config(page_title="Atlético Predictor - Dados Reais", layout="wide", page_icon="⚽")
st.title("⚽ Atlético Predictor - Dados Reais (Versão Inicial)")

# ------------------------
# Fetch dados reais
# ------------------------
try:
    games_df = fetch_atletico_games()
except Exception as e:
    st.error(f"Erro ao buscar dados: {e}")
    games_df = pd.DataFrame({
        "Data":["2025-10-20"], "Adversário":["Real Betis"],
        "xG_Atlético":[1.6], "xG_Adversário":[1.1],
        "Posse":[58], "Remates":[14], "Resultado":["2-1"]
    })

# Pegar último jogo como referência
ultimo_jogo = games_df.iloc[0]

# ------------------------
# Layout principal
# ------------------------
col_left, col_right = st.columns([1,2])

# ------------------------
# Sliders à esquerda por categorias
# ------------------------
with col_left:
    st.header("⚙️ Ajusta as Variáveis")

    # Equipa
    st.subheader("Equipe")
    forma = st.slider(f"Forma recente (0-100) | Último jogo: 70", 0, 100, 70, 1)
    adversario_forca = st.slider(f"Força do adversário (0-100) | {ultimo_jogo['Adversário']}", 0, 100, 60, 1)

    # Ataque
    st.subheader("Ataque")
    xg = st.slider(f"xG médio Atlético | Último jogo: {ultimo_jogo['xG_Atlético']}", 0.0, 3.0, float(ultimo_jogo['xG_Atlético']), 0.1)
    remates = st.slider(f"Remates por jogo | Último jogo: {ultimo_jogo['Remates']}", 0, 25, int(ultimo_jogo['Remates']), 1)

    # Defesa
    st.subheader("Defesa")
    defesa = st.slider("Interceções / Recuperações (0-100) | Exemplo: 70", 0, 100, 70, 1)

    # Passe
    st.subheader("Passe")
    passes_sucesso = st.slider(f"Taxa de sucesso de passes (%) | Último jogo: 84", 50, 95, 84, 1)
    passes_prog = st.slider("Passes progressivos (%) | Exemplo: 60", 0, 100, 60, 1)

    # Bolas Paradas
    st.subheader("Bolas Paradas")
    cantos = st.slider("Cantos por jogo | Exemplo: 5", 0, 15, 5, 1)
    faltas = st.slider("Faltas cometidas por jogo | Exemplo: 10", 0, 15, 10, 1)

# ------------------------
# Próximo jogo à direita
# ------------------------
with col_right:
    st.header("🔮 Próximo Jogo")

    jogo_idx = st.selectbox(
        "Escolhe o próximo jogo",
        range(len(games_df)),
        format_func=lambda x: f"{games_df.loc[x,'Data'].date()} vs {games_df.loc[x,'Adversário']} ({'Casa' if x%2==0 else 'Fora'})"
    )

    jogo = games_df.loc[jogo_idx]

    # Modelo simples de probabilidades
    score = (
        xg*0.4 +
        (jogo["Posse"]/100)*0.2 +
        (forma/100)*0.2 +
        (passes_sucesso/100)*0.1 +
        (remates/15*0.05) -
        (adversario_forca/100*0.3)
    )
    prob_vitoria = np.clip(score, 0, 1)
    prob_empate = (1 - abs(0.5 - prob_vitoria)) * 0.4
    prob_derrota = 1 - (prob_vitoria + prob_empate)
    probs = {
        "Vitória Atlético": prob_vitoria,
        "Empate": prob_empate,
        "Vitória Adversário": prob_derrota
    }

    pred_result = max(probs, key=probs.get)
    st.metric(label="Resultado provável", value=pred_result)
    st.metric(label="Probabilidade de vitória Atlético", value=f"{probs['Vitória Atlético']*100:.1f}%")

    # Gráfico compacto
    fig = go.Figure(go.Bar(
        x=list(probs.keys()),
        y=[v*100 for v in probs.values()],
        marker_color=["green","orange","red"]
    ))
    fig.update_layout(
        yaxis_title="Probabilidade (%)",
        xaxis_title="Resultado",
        height=300,
        margin=dict(l=20,r=20,t=30,b=20),
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)

# ------------------------
# Calendário abaixo
# ------------------------
st.header("📅 Últimos Jogos Atlético")
st.dataframe(games_df[["Data","Adversário","xG_Atlético","xG_Adversário","Posse","Remates","Resultado"]], use_container_width=True)
