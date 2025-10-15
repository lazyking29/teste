# data_fetcher.py
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def fetch_atletico_games(season="2024-25"):
    """
    Busca dados básicos do Atlético de Madrid na La Liga diretamente do FBref.
    Retorna DataFrame com algumas estatísticas.
    """
    # URL da página de stats do Atlético
    url = "https://fbref.com/en/squads/206d90db/Atlético-de-Madrid-Stats"

    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    # Encontrar tabela padrão (id pode variar conforme a página)
    table = soup.find("table", {"id": "stats_standard"})
    if table is None:
        raise ValueError("Tabela de jogos não encontrada. Verifica o id da tabela no FBref.")

    df = pd.read_html(str(table))[0]

    # Selecionar apenas algumas colunas úteis
    df = df[["Date", "Opponent", "xG", "xGA", "Poss", "Sh", "Result"]]

    # Renomear colunas para mais clareza
    df.columns = ["Data", "Adversário", "xG_Atlético", "xG_Adversário", "Posse", "Remates", "Resultado"]

    # Converter coluna de Data para datetime
    df["Data"] = pd.to_datetime(df["Data"], errors="coerce")

    # Ordenar por data
    df = df.sort_values("Data", ascending=False).reset_index(drop=True)

    return df.head(10)  # últimos 10 jogos para teste
