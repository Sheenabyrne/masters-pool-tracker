from flask import Flask, jsonify, render_template
import requests
import json
import unicodedata

app = Flask(__name__)

# 🔤 Normalize names
def normalize(name):
    return unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode().lower().strip()


# 🎯 YOUR PLAYER LIST (MASTER LIST)
TRACKED_PLAYERS = [
    "Scottie Scheffler","Tommy Fleetwood","Collin Morikawa","Patrick Reed",
    "Viktor Hovland","Bubba Watson","Corey Conners","Nicolai Hojgaard",
    "Harry Hall","Wyndham Clark","Jordan Spieth","Sam Burns",
    "Bryson DeChambeau","Hideki Matsuyama","Akshay Bhatia","Justin Rose",
    "Charl Schwartzel","Adam Scott","Jake Knapp","Cameron Smith",
    "Sungjae Im","Jacob Bridgeman","Cameron Young","Matt Fitzpatrick",
    "Dustin Johnson","Si Woo Kim","Tom McKibbin","Max Homa",
    "Brooks Koepka","Sepp Straka","Rasmus Neergaard-Petersen",
    "Shane Lowry","Alexander Noren","Jon Rahm","Min Woo Lee",
    "Marco Penge","Ben Griffin","Tyrrell Hatton","Rasmus Hojgaard",
    "J.J. Spaun","Danny Willett","Ryan Gerard","Patrick Cantlay",
    "Maverick McNealy","Robert MacIntyre"
]


# 🌐 LIVE CBS DATA
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

            # Convert score
            if score_raw == "E":
                score = 0
            else:
                try:
                    score = int(score_raw)
                except:
                    score = 0

            # Fix "Last, First"
            if "," in name:
                parts = name.split(",")
                name = parts[1].strip() + " " + parts[0].strip()

            players[name] = score

    except Exception as e:
        print("CBS fetch failed:", e)

    # 🔥 Ensure ALL tracked players exist (default = 0)
    normalized_live = {normalize(k): v for k, v in players.items()}

    final_players = {}

    for player in TRACKED_PLAYERS:
        key = normalize(player)

        if key in normalized_live:
            final_players[player] = normalized_live[key]
        else:
            final_players[player] = 0  # not started or not found

    return final_players


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
        "leaderboard": leaderboard,
        "results": results
    })


if __name__ == "__main__":
    app.run()
