# data_fetcher.py
from sportsreference.fbref import Team
import pandas as pd

def fetch_atletico_games():
    """
    Obtém os dados reais do Atlético de Madrid na La Liga utilizando sportsreference.
    """
    team = Team('ATM')  # Código do Atlético de Madrid
    games = team.schedule

    # Seleciona colunas úteis
    games_df = games[['date', 'opponent', 'result', 'goals', 'opponent_goals', 'xg', 'opponent_xg', 'possession', 'shots']]
    
    # Renomeia para português
    games_df.columns = ['Data', 'Adversário', 'Resultado', 'Gols_Atlético', 'Gols_Adversário', 'xG_Atlético', 'xG_Adversário', 'Posse', 'Remates']
    
    # Converte a coluna 'Data' para datetime
    games_df['Data'] = pd.to_datetime(games_df['Data'])
    
    # Ordena os jogos mais recentes primeiro
    games_df = games_df.sort_values(by='Data', ascending=False).reset_index(drop=True)
    
    return games_df
