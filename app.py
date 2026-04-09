from flask import Flask, jsonify, render_template
import requests
from bs4 import BeautifulSoup
import json

app = Flask(__name__)

URL = "https://mastersmadness.com/leaderboard"

def get_leaderboard():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")

    players = {}
    rows = soup.select("table tbody tr")

    for row in rows:
        cols = row.find_all("td")
        if len(cols) > 2:
            name = cols[1].text.strip()
            score = cols[2].text.strip()

            if score == "E":
                score = 0
            else:
                score = int(score.replace("+", ""))

            players[name] = score

    return players

def calculate_scores(leaderboard):
    with open("picks.json") as f:
        picks = json.load(f)

    results = []

    for person, players in picks.items():
        total = 0
        missing = []

        for player in players:
            if player in leaderboard:
                total += leaderboard[player]
            else:
                missing.append(player)

        results.append({
            "name": person,
            "total": total,
            "missing": missing
        })

    return sorted(results, key=lambda x: x["total"])

@app.route("/")
def home():
    leaderboard = get_leaderboard()
    results = calculate_scores(leaderboard)
    return render_template("index.html", results=results)

@app.route("/api")
def api():
    leaderboard = get_leaderboard()
    results = calculate_scores(leaderboard)
    return jsonify(results)

if __name__ == "__main__":
    app.run()
