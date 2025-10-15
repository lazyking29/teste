import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="Atlético Predictor - Interface Funcional",
    layout="wide",
    page_icon="⚽"
)

st.title("⚽ Atlético Predictor - Interface Funcional")

# ------------------------
# Mock dos próximos jogos
# ------------------------
mock_games = pd.DataFrame({
    "Data": ["20 Out 2025", "27 Out 2025", "2 Nov 2025"],
    "Adversário": ["Real Betis", "Villarreal", "Barcelona"],
    "Local": ["Casa", "Fora", "Casa"],
    "xG Atlético": [1.6, 1.4, 1.1],
    "xG Adversário": [1.1, 1.5, 1.8],
    "Posse Atlético": [58, 55, 52],
    "Forma Atlético": [70, 68, 65],
    "Passes Sucesso": [84, 82, 80],
    "Remates": [14, 13, 11],
    "Força Adversário": [60, 65, 85]
})

# ------------------------
# Layout principal
# ------------------------
col_left, col_right = st.columns([1, 2])

# ------------------------
# Sliders à esquerda por categorias
# ------------------------
with col_left:
    st.header("⚙️ Ajusta as Variáveis")

    # Equipa
    st.subheader("Equipe")
    forma = st.slider("Forma recente (0-100)", 0, 100, 70, 1)
    adversario_forca = st.slider("Força do adversário (0-100)", 0, 100, 60, 1)

    # Ataque
    st.subheader("Ataque")
    xg = st.slider("xG médio do Atlético", 0.0, 3.0, 1.6, 0.1)
    remates = st.slider("Remates por jogo", 0, 25, 14, 1)

    # Defesa
    st.subheader("Defesa")
    defesa = st.slider("Interceções / Recuperações (0-100)", 0, 100, 70, 1)

    # Passe
    st.subheader("Passe")
    passes_sucesso = st.slider("Taxa de sucesso de passes (%)", 50, 95, 84, 1)
    passes_prog = st.slider("Passes progressivos (%)", 0, 100, 60, 1)

    # Bolas Paradas
    st.subheader("Bolas Paradas")
    cantos = st.slider("Cantos por jogo", 0, 15, 5, 1)
    faltas = st.slider("Faltas cometidas por jogo", 0, 15, 10, 1)

# ------------------------
# Próximo jogo à direita
# ------------------------
with col_right:
    st.header("🔮 Próximo Jogo")

    # Seleção de jogo
    jogo_idx = st.selectbox(
        "Escolhe o próximo jogo",
        range(len(mock_games)),
        format_func=lambda x: f"{mock_games.loc[x,'Data']} vs {mock_games.loc[x,'Adversário']} ({mock_games.loc[x,'Local']})"
    )

    jogo = mock_games.loc[jogo_idx]

    # Modelo simples
    score = (
        xg * 0.4 +
        (jogo["Posse Atlético"]/100) * 0.2 +
        (forma / 100) * 0.2 +
        (passes_sucesso / 100) * 0.1 +
        (remates / 15 * 0.05) -
        (adversario_forca / 100 * 0.3)
    )
    prob_vitoria = np.clip(score, 0, 1)
    prob_empate = (1 - abs(0.5 - prob_vitoria)) * 0.4
    prob_derrota = 1 - (prob_vitoria + prob_empate)
    probs = {
        "Vitória Atlético": prob_vitoria,
        "Empate": prob_empate,
        "Vitória Adversário": prob_derrota
    }

    # Resultado provável
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
st.header("📅 Próximos Jogos")
st.markdown("Seleciona o próximo jogo acima para ver detalhes.")

st.dataframe(
    mock_games[["Data","Adversário","Local","xG Atlético","xG Adversário"]],
    use_container_width=True
)

st.markdown("""
💡 **Notas:**
- Sliders à esquerda, divididos por categorias.
- Próximo jogo à direita com gráfico compacto colorido.
- Calendário abaixo apenas informativo.
- Totalmente funcional no Streamlit Cloud.
""")
