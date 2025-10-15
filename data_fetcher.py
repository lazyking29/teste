# data_fetcher.py
import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_atletico_games():
    """
    Busca dados reais do Atlético de Madrid na La Liga diretamente do FBref.
    Retorna um DataFrame com as estatísticas básicas de cada jogo.
    """
    url = "https://fbref.com/en/squads/206d90db/schedule/Atl%C3%A9tico-de-Madrid-Scores-and-Fixtures-La-Liga"
    res = requests.get(url)
    if res.status_code != 200:
        raise ValueError(f"Erro ao acessar FBref: {res.status_code}")

    soup = BeautifulSoup(res.text, "lxml")

    # Pegar a primeira tabela visível (match logs)
    table = soup.find("table")
    if table is None:
        raise ValueError("Tabela de jogos não encontrada na página.")

    df = pd.read_html(str(table))[0]

    # Algumas colunas podem ter MultiIndex, simplificamos
    df.columns = [c[1] if isinstance(c, tuple) else c for c in df.columns]

    # Selecionar colunas úteis e renomear
    cols = ["Date", "Opponent", "Result", "GF", "GA", "xG", "xGA", "Poss", "Sh"]
    df = df[cols]
    df.columns = ["Data","Adversário","Resultado","Gols_Atlético","Gols_Adversário","xG_Atlético","xG_Adversário","Posse","Remates"]

    # Converter data
    df["Data"] = pd.to_datetime(df["Data"], errors="coerce")
    df = df.sort_values("Data", ascending=False).reset_index(drop=True)

    return df
