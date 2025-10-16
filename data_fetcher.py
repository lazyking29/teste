import requests
import pandas as pd
import os

# URL base da API de futebol
BASE_URL = "https://api.football-data.org/v4"
LEAGUE_ID = "PD"  # La Liga

def get_team_matches(team_name="Atlético de Madrid", season=2024):
    """
    Vai buscar todos os jogos da La Liga para o Atlético de Madrid
    na época especificada.
    """
    api_key = os.getenv("FOOTBALL_API_KEY")  # chave de API no ambiente Streamlit Cloud
    headers = {"X-Auth-Token": api_key}

    url = f"{BASE_URL}/competitions/{LEAGUE_ID}/matches?season={season}"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Erro na API: {response.status_code} - {response.text}")

    data = response.json()

    matches = []
    for match in data["matches"]:
        home = match["homeTeam"]["name"]
        away = match["awayTeam"]["name"]
        if team_name in [home, away]:
            matches.append({
                "Date": match["utcDate"][:10],
                "Home": home,
                "Away": away,
                "Score": f"{match['score']['fullTime']['home']} - {match['score']['fullTime']['away']}",
                "Status": match["status"]
            })

    df = pd.DataFrame(matches)
    return df

def get_next_match(team_name="Atlético de Madrid", season=2024):
    """
    Retorna o próximo jogo do Atlético de Madrid.
    """
    df = get_team_matches(team_name, season)
    upcoming = df[df["Status"] == "SCHEDULED"]
    if not upcoming.empty:
        return upcoming.iloc[0]
    return None
