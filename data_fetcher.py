import requests
import pandas as pd
import os

BASE_URL = "https://api.football-data.org/v4"
LEAGUE_ID = "PD"  # La Liga

def get_headers():
    api_key = os.getenv("FOOTBALL_API_KEY")
    if not api_key:
        raise Exception("⚠️ API key não encontrada. Define FOOTBALL_API_KEY nos secrets do Streamlit Cloud.")
    return {"X-Auth-Token": api_key}

def get_teams_in_la_liga(season=2024):
    """
    Busca todas as equipas da La Liga para a época dada.
    """
    url = f"{BASE_URL}/competitions/{LEAGUE_ID}/teams?season={season}"
    response = requests.get(url, headers=get_headers())

    if response.status_code != 200:
        raise Exception(f"Erro ao obter equipas: {response.status_code} — {response.text}")

    data = response.json()
    teams = pd.DataFrame(data["teams"])
    return teams[["id", "name", "shortName", "tla"]]

def get_team_id(team_name="Atlético de Madrid", season=2024):
    """
    Procura o ID da equipa pelo nome (flexível: aceita 'Atlético', 'Ath Madrid', etc.).
    """
    teams = get_teams_in_la_liga(season)
    filtered = teams[teams["name"].str.lower().str.contains(team_name.lower()) |
                     teams["shortName"].str.lower().str.contains(team_name.lower()) |
                     teams["tla"].str.lower().str.contains(team_name.lower())]
    if filtered.empty:
        raise Exception(f"Nenhuma equipa encontrada para '{team_name}'. Verifica o nome ou a época.")
    return int(filtered.iloc[0]["id"])

def get_team_matches(team_name="Atlético de Madrid", season=2024):
    """
    Busca todos os jogos da equipa na La Liga.
    """
    team_id = get_team_id(team_name, season)
    url = f"{BASE_URL}/teams/{team_id}/matches?competitions={LEAGUE_ID}&season={season}"
    response = requests.get(url, headers=get_headers())

    if response.status_code != 200:
        raise Exception(f"Erro ao obter jogos: {response.status_code} — {response.text}")

    data = response.json()
    matches = data.get("matches", [])
    if not matches:
        raise Exception("Nenhum jogo encontrado para a equipa.")

    df = pd.DataFrame([{
        "Date": m["utcDate"][:10],
        "Home": m["homeTeam"]["name"],
        "Away": m["awayTeam"]["name"],
        "Score": f"{m['score']['fullTime']['home']} - {m['score']['fullTime']['away']}",
        "Status": m["status"]
    } for m in matches])

    return df

def get_next_match(team_name="Atlético de Madrid", season=2024):
    df = get_team_matches(team_name, season)
    upcoming = df[df["Status"].isin(["SCHEDULED", "TIMED"])]
    if not upcoming.empty:
        return upcoming.iloc[0]
    return None
