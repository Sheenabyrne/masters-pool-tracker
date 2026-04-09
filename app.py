from flask import Flask, jsonify, render_template
import requests
import json
import unicodedata

app = Flask(__name__)

# 🔤 Normalize names (handles accents, spacing, case)
def normalize(name):
    return unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode().lower().strip()


# 🌐 ESPN LIVE LEADERBOARD
def get_leaderboard():
    url = "https://site.web.api.espn.com/apis/v2/sports/golf/leaderboard"

    players = {}

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        competitors = data["events"][0]["competitions"][0]["competitors"]

        for player in competitors:
            name = player["athlete"]["displayName"]
            score = player["score"]

            # Convert score properly
            if score == "E":
                score = 0
            else:
                score = int(score)

            players[name] = score

    except Exception as e:
        print("ESPN fetch failed:", e)

    return players


# 🧮 Calculate scores
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
        "leaderboard_sample": list(leaderboard.items())[:15],
        "results": results
    })


if __name__ == "__main__":
    app.run()
