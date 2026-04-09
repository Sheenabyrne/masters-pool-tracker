from flask import Flask, jsonify, render_template
import json
import unicodedata
from datetime import datetime
from zoneinfo import ZoneInfo

app = Flask(__name__)

# 🔤 Normalize names
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


# ✏️ MANUAL SCORES (UPDATED)
MANUAL_SCORES = {
    "Adam Scott": 0,
    "Akshay Bhatia": 1,
    "Alexander Noren": 5,
    "Ben Griffin": 0,
    "Brooks Koepka": 0,
    "Bryson DeChambeau": 4,
    "Bubba Watson": 4,
    "Cameron Smith": 2,
    "Cameron Young": 1,
    "Charl Schwartzel": 3,
    "Collin Morikawa": 2,
    "Corey Conners": 3,
    "Danny Willett": 4,
    "Dustin Johnson": 1,
    "Harry Hall": 5,
    "Hideki Matsuyama": 0,
    "Jacob Bridgeman": -1,
    "Jake Knapp": 1,
    "J.J. Spaun": 2,
    "Jon Rahm": 6,
    "Jordan Spieth": 0,
    "Justin Rose": -2,
    "Ludvig Aberg": 2,
    "Marco Penge": 4,
    "Matt Fitzpatrick": 2,
    "Maverick McNealy": 5,
    "Max Homa": 0,
    "Min Woo Lee": 6,
    "Nicolai Hojgaard": 4,
    "Patrick Cantlay": 5,
    "Patrick Reed": -3,
    "Rasmus Hojgaard": 6,
    "Rasmus Neergaard-Petersen": 5,
    "Robert MacIntyre": 8,
    "Rory McIlroy": -5,
    "Sam Burns": -5,
    "Sepp Straka": 1,
    "Shane Lowry": -2,
    "Si Woo Kim": 3,
    "Sungjae Im": 4,
    "Tommy Fleetwood": -1,
    "Tom McKibbin": 3,
    "Tyrrell Hatton": 2,
    "Viktor Hovland": 3,
    "Wyndham Clark": 0,
    "Ryan Gerard": 0
}


# 🌐 Build leaderboard
def get_leaderboard():
    normalized_manual = {
        normalize(name): score for name, score in MANUAL_SCORES.items()
    }

    final_players = {}

    for player in TRACKED_PLAYERS:
        key = normalize(player)
        final_players[player] = normalized_manual.get(key, 0)

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


# 🏠 Dashboard (NEWFOUNDLAND TIME)
@app.route("/")
def home():
    leaderboard = get_leaderboard()
    results = calculate_scores(leaderboard)

    last_updated = datetime.now(ZoneInfo("America/St_Johns")).strftime("%Y-%m-%d %H:%M:%S")

    return render_template("index.html", results=results, last_updated=last_updated)


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
