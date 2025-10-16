import requests
import pandas as pd
import datetime
import os

# ------------------------ #
#  🔧 CONFIGURAÇÕES GERAIS
# ------------------------ #
BASE_URL = "https://api.football-data.org/v4"
LEAGUE_ID = "PD"  # La Liga
SOFASCORE_API = "https://api.sofascore.com/api/v1"
CURRENT_SEASON = 2025  # Atualizado para a época 2025/26

# ------------------------ #
#  ⚙️ FUNÇÕES PRINCIPAIS
# ------------------------ #
def get_headers():
    api_key = os.getenv("FOOTBALL_API_KEY")
    if not api_key:
        raise Exception("⚠️ API key não encontrada. Define FOOTBALL_API_KEY nos secrets do Streamlit Cloud.")
    return {"X-Auth-Token": api_key}


# ---------------------------------------------------- #
# 1️⃣  EQUIPAS E JOGOS — via API oficial football-data
# ---------------------------------------------------- #
def get_team_id(team_name="Atlético de Madrid", season=CURRENT_SEASON):
    url = f"{BASE_URL}/competitions/{LEAGUE_ID}/teams?season={season}"
    res = requests.get(url, headers=get_headers())
    res.raise_for_status()
    data = res.json()
    for t in data["teams"]:
        if team_name.lower() in t["name"].lower():
            return t["id"]
    raise Exception("Equipa não encontrada na La Liga.")


def get_team_matches(team_name="Atlético de Madrid", season=CURRENT_SEASON):
    team_id = get_team_id(team_name, season)
    url = f"{BASE_URL}/teams/{team_id}/matches?competitions={LEAGUE_ID}&season={season}"
    res = requests.get(url, headers=get_headers())
    res.raise_for_status()
    matches = res.json().get("matches", [])

    df = pd.DataFrame([
        {
            "Date": m["utcDate"][:10],
            "Home": m["homeTeam"]["name"],
            "Away": m["awayTeam"]["name"],
            "Score": f"{m['score']['fullTime']['home']} - {m['score']['fullTime']['away']}",
            "Status": m["status"],
        }
        for m in matches
    ])

    # Filtra só jogos da época atual (em caso de confusão de datas)
    df["Date"] = pd.to_datetime(df["Date"])
    df = df[df["Date"].dt.year >= 2025]

    return df


# ------------------------------------------------ #
# 2️⃣  ESTATÍSTICAS DETALHADAS — via API SofaScore
# ------------------------------------------------ #
def get_sofascore_team_id(team_name="Atletico Madrid"):
    search = requests.get(f"{SOFASCORE_API}/search/all?q={team_name}")
    if search.status_code != 200:
        return None
    data = search.json()
    try:
        return data["teams"][0]["id"]
    except (KeyError, IndexError):
        return None


def get_last_match_stats(team_name="Atletico Madrid"):
    team_id = get_sofascore_team_id(team_name)
    if not team_id:
        raise Exception("Erro: não foi possível encontrar o ID da equipa no SofaScore.")

    fixtures = requests.get(f"{SOFASCORE_API}/team/{team_id}/events/last/0")
    fixtures.raise_for_status()
    last_match = fixtures.json()["events"][0]

    # Só aceitar jogos da época atual (25/26)
    match_year = datetime.datetime.fromtimestamp(last_match["startTimestamp"]).year
    if match_year < 2025:
        raise Exception("O último jogo encontrado não pertence à época 2025/26.")

    match_id = last_match["id"]
    stats_url = f"{SOFASCORE_API}/event/{match_id}/statistics"
    stats_res = requests.get(stats_url)
    stats_res.raise_for_status()

    stats = stats_res.json().get("statistics", [])
    flat_stats = {}
    for section in stats:
        for group in section.get("groups", []):
            for item in group.get("statisticsItems", []):
                name = item["name"]
                home_val = item.get("home", "-")
                away_val = item.get("away", "-")
                flat_stats[name] = {"Atlético": home_val, "Adversário": away_val}

    df = pd.DataFrame(flat_stats).T
    df.reset_index(inplace=True)
    df.columns = ["Estatística", "Atlético", "Adversário"]

    return df, last_match


# --------------------------------------- #
# 3️⃣  PRÓXIMO JOGO — via API SofaScore
# --------------------------------------- #
def get_next_match(team_name="Atletico Madrid"):
    team_id = get_sofascore_team_id(team_name)
    if not team_id:
        return None
    fixtures = requests.get(f"{SOFASCORE_API}/team/{team_id}/events/next/0")
    if fixtures.status_code != 200:
        return None
    data = fixtures.json().get("events", [])
    if not data:
        return None
    next_match = data[0]
    return {
        "date": next_match["startTimestamp"],
        "home": next_match["homeTeam"]["name"],
        "away": next_match["awayTeam"]["name"],
        "tournament": next_match["tournament"]["name"],
    }
