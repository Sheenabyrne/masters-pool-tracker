from flask import Flask, jsonify, render_template
import requests
import json
import unicodedata

app = Flask(__name__)

# 🔤 Normalize names (fix accents, spacing, case)
def normalize(name):
    return unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode().lower().strip()


# 🌐 CBS SPORTS LEADERBOARD (LIVE DATA)
def get_leaderboard():
    url = "https://site.api.cbssports.com/golf/leaderboard/live"

    players = {}

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        leaderboard = data.get("leaderboard", [])

        for player in leaderboard:
            name = player.get("player_name", "").strip()

            score_raw = player.get("score", "0")

            # Convert score safely
            if score_raw == "E":
                score = 0
            else:
                try:
                    score = int(score_raw)
                except:
                    score = 0

            # Fix format if name is "Last, First"
            if "," in name:
                parts = name.split(",")
                name = parts[1].strip() + " " + parts[0].strip()

            players[name] = score

        if not players:
            print("⚠️ No CBS leaderboard data found")

    except Exception as e:
        print("❌ CBS fetch failed:", e)

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
