import requests
import pandas as pd
import os

BASE_URL = "https://api.football-data.org/v4"
LEAGUE_ID = "PD"  # La Liga

def get_team_matches(team_name="Atletico de Madrid", season=2024):
    """
    Vai buscar todos os jogos da La Liga para o Atlético de Madrid
    na época especificada.
    """
    api_key = os.getenv("FOOTBALL_API_KEY")
    if not api_key:
        raise Exception("API key não encontrada. Define FOOTBALL_API_KEY nos secrets do Streamlit Cloud.")

    headers = {"X-Auth-Token": api_key}
    url = f"{BASE_URL}/competitions/{LEAGUE_ID}/matches?season={season}"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Erro na API: {response.status_code} - {response.text}")

    data = response.json()

    if "matches" not in data:
        raise Exception("Resposta inesperada da API (sem campo 'matches').")

    matches = []
    for match in data["matches"]:
        home = match.get("homeTeam", {}).get("name", "")
        away = match.get("awayTeam", {}).get("name", "")

        # Só adiciona jogos do Atlético
        if team_name.lower().replace("é", "e") in home.lower() or team_name.lower().replace("é", "e") in away.lower():
            matches.append({
                "Date": match.get("utcDate", "")[:10],
                "Home": home,
                "Away": away,
                "Score": f"{match.get('score', {}).get('fullTime', {}).get('home', '-')} - {match.get('score', {}).get('fullTime', {}).get('away', '-')}",
                "Status": match.get("status", "Unknown")  # Corrigido aqui!
            })

    df = pd.DataFrame(matches)

    if df.empty:
        raise Exception("Nenhum jogo encontrado. Verifica o nome da equipa ou a época.")

    return df


def get_next_match(team_name="Atletico de Madrid", season=2024):
    """
    Retorna o próximo jogo do Atlético de Madrid.
    """
    df = get_team_matches(team_name, season)
    upcoming = df[df["Status"].isin(["SCHEDULED", "TIMED"])]
    if not upcoming.empty:
        return upcoming.iloc[0]
    return None
