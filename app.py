import streamlit as st
import pandas as pd
from data_fetcher import get_team_matches, get_next_match

st.set_page_config(page_title="Atleti Analyzer", layout="wide")

st.title("⚽ Atlético de Madrid — Analisador de Jogos (La Liga)")

# Colunas principais
col1, col2 = st.columns([1, 2])

with col1:
    st.header("Ajustes e Estatísticas")

    with st.expander("🏟️ Equipa"):
        st.slider("Moral da Equipa", 0, 100, 70, help="Nível de confiança e forma atual da equipa.")
        st.slider("Coesão Tática", 0, 100, 80, help="Quão bem a equipa entende o esquema tático.")

    with st.expander("⚔️ Ataque"):
        st.slider("Eficiência Ofensiva", 0, 100, 75, help="Capacidade de converter oportunidades em golos.")
        st.slider("Pressão Alta", 0, 100, 60, help="Frequência e sucesso na recuperação de bola no ataque.")

    with st.expander("🧱 Defesa"):
        st.slider("Organização Defensiva", 0, 100, 85, help="Coordenação da linha defensiva.")
        st.slider("Desarmes e Interceções", 0, 100, 78, help="Efetividade na recuperação da bola.")

with col2:
    st.header("📊 Dados Reais — La Liga")

    try:
        matches_df = get_team_matches()
        st.dataframe(matches_df.tail(5), use_container_width=True)

        next_match = get_next_match()
        if next_match is not None:
            st.subheader("🔮 Próximo Jogo")
            st.markdown(
                f"**{next_match['Home']} 🆚 {next_match['Away']}**  \n📅 {next_match['Date']}"
            )
        else:
            st.info("Nenhum jogo futuro encontrado.")

    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
