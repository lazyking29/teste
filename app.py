# app.py
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Atlético Predictor - versão simples", layout="wide")

st.title("⚽ Previsor Interativo — Atlético de Madrid (versão simples)")
st.markdown("""
Esta é a **versão de teste** do programa.  
Permite ajustar manualmente variáveis importantes (xG, posse, forma, etc.)  
e ver uma **previsão de resultado** provável.
""")

col1, col2 = st.columns(2)

with col1:
    xg = st.slider("xG médio do Atlético (últimos jogos)", 0.0, 3.0, 1.6, 0.1)
    posse = st.slider("Posse de bola (%)", 30, 80, 58, 1)
    forma = st.slider("Forma recente (0–100)", 0, 100, 70, 1)

with col2:
    passes_sucesso = st.slider("Taxa de sucesso de passes (%)", 50, 95, 84, 1)
    remates = st.slider("Remates por jogo", 0, 25, 14, 1)
    adversario_forca = st.slider("Força do adversário (0=fraco, 100=muito forte)", 0, 100, 60, 1)

score = (
    xg * 0.4 +
    (posse / 100) * 0.3 +
    (forma / 100) * 0.2 +
    (passes_sucesso / 100) * 0.1 -
    (adversario_forca / 100) * 0.4
)
prob_vitoria = np.clip(score, 0, 1)

prob_empate = (1 - abs(0.5 - prob_vitoria)) * 0.4
prob_derrota = 1 - (prob_vitoria + prob_empate)
probs = {
    "Vitória Atlético": prob_vitoria,
    "Empate": prob_empate,
    "Derrota Atlético": prob_derrota
}

st.subheader("🔮 Previsão de Resultado")
pred_result = max(probs, key=probs.get)

col3, col4 = st.columns([1, 2])
with col3:
    st.metric(label="Resultado provável", value=pred_result)
    st.metric(label="Probabilidade de vitória", value=f"{probs['Vitória Atlético']*100:.1f}%")

with col4:
    fig, ax = plt.subplots()
    ax.bar(probs.keys(), [v * 100 for v in probs.values()])
    ax.set_ylabel("Probabilidade (%)")
    ax.set_title("Distribuição de probabilidades previstas")
    st.pyplot(fig)

st.markdown("## 📅 Próximos jogos (simulação)")
mock_games = pd.DataFrame({
    "Data": ["20 Out 2025", "27 Out 2025", "2 Nov 2025"],
    "Adversário": ["Real Betis", "Villarreal", "Barcelona"],
    "Local": ["Casa", "Fora", "Casa"],
    "Previsão Vitória (%)": [62, 48, 37]
})
st.dataframe(mock_games, use_container_width=True)

st.markdown("""
---
💡 **Como funciona:**  
- O modelo é apenas ilustrativo (não usa dados reais ainda).  
- Serve para testares a interface e perceber como as variáveis influenciam as previsões.  
- Quando estiveres confortável, passamos à **versão completa** com scraping real e modelo preditivo de verdade.
""")
