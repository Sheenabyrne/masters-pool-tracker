from flask import Flask, jsonify, render_template
import json
import unicodedata

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


# ✏️ MANUAL SCORES (UPDATED)
MANUAL_SCORES = {
    "Adam Scott": 0,
    "Akshay Bhatia": 1,
    "Alexander Noren": 0,
    "Ben Griffin": 0,
    "Brooks Koepka": 2,
    "Bryson DeChambeau": 0,
    "Bubba Watson": 2,
    "Cameron Smith": -1,
    "Cameron Young": 1,
    "Charl Schwartzel": 2,
    "Collin Morikawa": 0,
    "Corey Conners": 0,
    "Danny Willett": 2,
    "Dustin Johnson": 2,
    "Harry Hall": 1,
    "Hideki Matsuyama": -2,
    "Jacob Bridgeman": 1,
    "Jake Knapp": 1,
    "J.J. Spaun": 1,
    "Jon Rahm": 0,
    "Jordan Spieth": 0,
    "Justin Rose": -4,
    "Ludvig Aberg": -1,
    "Marco Penge": 0,
    "Matt Fitzpatrick": 1,
    "Maverick McNealy": 0,
    "Max Homa": 1,
    "Min Woo Lee": 1,
    "Nicolai Hojgaard": 0,
    "Patrick Cantlay": 0,
    "Patrick Reed": -3,
    "Rasmus Hojgaard": 0,
    "Rasmus Neergaard-Petersen": 0,
    "Robert MacIntyre": 1,
    "Rory McIlroy": -1,
    "Sam Burns": -2,
    "Sepp Straka": -1,
    "Shane Lowry": 0,
    "Si Woo Kim": 1,
    "Sungjae Im": -2,
    "Tommy Fleetwood": -3,
    "Tom McKibbin": 0,
    "Tyrrell Hatton": 2,
    "Viktor Hovland": 1,
    "Wyndham Clark": 1,
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

        if key in normalized_manual:
            final_players[player] = normalized_manual[key]
        else:
            final_players[player] = 0

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
