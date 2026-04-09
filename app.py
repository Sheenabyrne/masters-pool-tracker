from flask import Flask, jsonify, render_template
import json
import unicodedata

app = Flask(__name__)

# 🔤 Normalize names (fix accents, case, spacing)
def normalize(name):
    return unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode().lower().strip()


# 🌐 STATIC LEADERBOARD (YOUR PROVIDED SCORES)
def get_leaderboard():
    return {
        "Scottie Scheffler": 0,
        "Tommy Fleetwood": -3,
        "Collin Morikawa": 0,
        "Patrick Reed": -3,
        "Viktor Hovland": 1,
        "Bubba Watson": 2,
        "Corey Conners": 0,
        "Nicolai Hojgaard": 0,
        "Harry Hall": 1,
        "Wyndham Clark": 1,
        "Jordan Spieth": 0,
        "Sam Burns": -2,
        "Bryson DeChambeau": 0,
        "Hideki Matsuyama": -2,
        "Akshay Bhatia": 1,
        "Justin Rose": -4,
        "Charl Schwartzel": 2,
        "Adam Scott": 0,
        "Jake Knapp": 1,
        "Cameron Smith": -1,
        "Sungjae Im": -2,
        "Jacob Bridgeman": 1,
        "Cameron Young": 1,
        "Matt Fitzpatrick": 1,
        "Dustin Johnson": 2,
        "Si Woo Kim": 1,
        "Tom McKibbin": 0,
        "Max Homa": 1,
        "Brooks Koepka": 2,
        "Sepp Straka": -1,
        "Rasmus Neergaard-Petersen": 0,
        "Shane Lowry": 0,
        "Alexander Noren": 0,
        "Jon Rahm": 0,
        "Min Woo Lee": 1,
        "Marco Penge": 0,
        "Ben Griffin": 0,
        "Tyrrell Hatton": 2,
        "Rasmus Hojgaard": 0,
        "J.J. Spaun": 1,
        "Danny Willett": 2,
        "Ryan Gerard": 0,
        "Patrick Cantlay": 0,
        "Maverick McNealy": 0,
        "Robert MacIntyre": 1
    }


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
        "leaderboard_count": len(leaderboard),
        "leaderboard_sample": list(leaderboard.items())[:10],
        "results": results
    })


if __name__ == "__main__":
    app.run()
