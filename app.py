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
    "Adam Scott","Scottie Scheffler","Akshay Bhatia","Alexander Noren","Ben Griffin",
    "Brooks Koepka","Bryson DeChambeau","Bubba Watson","Cameron Smith",
    "Cameron Young","Charl Schwartzel","Collin Morikawa","Corey Conners",
    "Danny Willett","Dustin Johnson","Harry Hall","Hideki Matsuyama",
    "Jacob Bridgeman","Jake Knapp","J.J. Spaun","Jon Rahm",
    "Jordan Spieth","Justin Rose","Ludvig Aberg","Marco Penge",
    "Matt Fitzpatrick","Maverick McNealy","Max Homa","Min Woo Lee",
    "Nicolai Hojgaard","Patrick Cantlay","Patrick Reed","Rasmus Hojgaard",
    "Rasmus Neergaard-Petersen","Robert MacIntyre","Rory McIlroy",
    "Sam Burns","Scottie Scheffler","Sepp Straka","Shane Lowry","Si Woo Kim",
    "Sungjae Im","Tommy Fleetwood","Tom McKibbin","Tyrrell Hatton",
    "Viktor Hovland","Wyndham Clark","Ryan Gerard"
]


# ✏️ MANUAL SCORES
MANUAL_SCORES = {
    "Adam Scott": 0,
    "Scottie Scheffler": -7,
    "Akshay Bhatia": 6,
    "Alexander Noren": 1,
    "Ben Griffin": -5,
    "Brooks Koepka": -4,
    "Bryson DeChambeau": 6,
    "Bubba Watson": 5,
    "Cameron Smith": 7,
    "Cameron Young": -11,
    "Charl Schwartzel": 9,
    "Collin Morikawa": -5,
    "Corey Conners": 3,
    "Danny Willett": 5,
    "Dustin Johnson": 3,
    "Harry Hall": 5,
    "Hideki Matsuyama": -2,
    "Jacob Bridgeman": -2,
    "Jake Knapp": -5,
    "J.J. Spaun": 5,
    "Jon Rahm": 5,
    "Jordan Spieth": -1,
    "Justin Rose": -8,
    "Ludvig Aberg": -3,
    "Marco Penge": 0,
    "Matt Fitzpatrick": -3,
    "Maverick McNealy": 1,
    "Max Homa": -3,
    "Min Woo Lee": 11,
    "Nicolai Hojgaard": 6,
    "Patrick Cantlay": -6,
    "Patrick Reed": -6,
    "Rasmus Hojgaard": 5,
    "Rasmus Neergaard-Petersen": 7,
    "Robert MacIntyre": 7,
    "Rory McIlroy": -11,
    "Sam Burns": -10,
    "Sepp Straka": -2,
    "Shane Lowry": -9,
    "Si Woo Kim": 4,
    "Sungjae Im": -2,
    "Tommy Fleetwood": -4,
    "Tom McKibbin": 7,
    "Tyrrell Hatton": -4,
    "Viktor Hovland": 1,
    "Wyndham Clark": -4,
    "Ryan Gerard": -4
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
