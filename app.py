from flask import Flask, jsonify, render_template
import json
import unicodedata
import requests
from bs4 import BeautifulSoup
import time

app = Flask(__name__)

# 🔤 Normalize names (handles accents, spacing, case)
def normalize(name):
    return unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode().lower().strip()


# 🎯 PLAYER LIST
TRACKED_PLAYERS = [
    "Adam Scott","Akshay Bhatia","Alexander Noren","Ben Griffin",
    "Brooks Koepka","Bryson DeChambeau","Bubba Watson","Cameron Smith",
    "Cameron Young","Charl Schwartzel","Collin Morikawa","Corey Conners",
    "Danny Willett","Dustin Johnson","Harry Hall","Hideki Matsuyama",
    "Jacob Bridgeman","Jake Knapp","J.J. Spaun","Jon Rahm",
    "Jordan Spieth","Justin Rose","Ludvig Aberg","Marco Penge",
    "Matt Fitzpatrick","Maverick McNealy","Max Homa","Min Woo Lee",
    "Nicolai Hojgaard","Patrick Cantlay","Patrick Reed","Rasmus Hojgaard",
    "Rasmus Neergaard-Petersen","Robert MacIntyre","Rory McIlroy",
    "Sam Burns","Sepp Straka","Shane Lowry","Si Woo Kim",
    "Sungjae Im","Tommy Fleetwood","Tom McKibbin","Tyrrell Hatton",
    "Viktor Hovland","Wyndham Clark","Ryan Gerard"
]


# 🌐 Fetch live scores (scraping Masters leaderboard)
def fetch_live_scores():
    url = "https://www.masters.com/en_US/scores/index.html"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    scores = {}

    rows = soup.select("tr")

    for row in rows:
        name_tag = row.select_one(".player-name")
        score_tag = row.select_one(".player-score")

        if name_tag and score_tag:
            name = name_tag.text.strip()
            score_text = score_tag.text.strip()

            # Convert score
            if score_text == "E":
                score = 0
            else:
                try:
                    score = int(score_text)
                except:
                    continue

            scores[name] = score

    return scores


# ⚡ Cache (reduces load + speeds up app)
CACHE = {
    "data": None,
    "timestamp": 0
}


# 🌐 Build leaderboard
def get_leaderboard():
    # ⏱ Cache for 60 seconds
    if time.time() - CACHE["timestamp"] < 60 and CACHE["data"]:
        return CACHE["data"]

    live_scores = fetch_live_scores()

    normalized_live = {
        normalize(name): score for name, score in live_scores.items()
    }

    final_players = {}

    for player in TRACKED_PLAYERS:
        key = normalize(player)
        final_players[player] = normalized_live.get(key, 0)

    CACHE["data"] = final_players
    CACHE["timestamp"] = time.time()

    return final_players


# 🧮 Calculate pool scores
def calculate_scores(leaderboard):
    with open("picks.json") as f:
        picks = json.load(f)

    normalized_leaderboard = {
        normalize(name): score for name, score in leaderboard.items()
    }

    results = []

    for person, players in picks.items():
        total = 0
        missing = []

        for player in players:
            key = normalize(player)

            if key in normalized_leaderboard:
                total += normalized_leaderboard[key]
            else:
                missing.append(player)

        results.append({
            "name": person,
            "total": total,
            "missing": missing
        })

    return sorted(results, key=lambda x: x["total"])


# 🏠 Dashboard
@app.route("/")
def home():
    leaderboard = get_leaderboard()
    results = calculate_scores(leaderboard)
    return render_template("index.html", results=results)


# 🔍 Debug API
@app.route("/api")
def api():
    leaderboard = get_leaderboard()
    results = calculate_scores(leaderboard)

    return jsonify({
        "leaderboard": leaderboard,
        "results": results
    })


if __name__ == "__main__":
    app.run(debug=True)
