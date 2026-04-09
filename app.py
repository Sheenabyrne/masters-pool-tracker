def get_leaderboard():
    url = "https://site.api.espn.com/apis/site/v2/sports/golf/leaderboard"

    players = {}

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        events = data.get("events", [])

        for event in events:
            name = event.get("name", "")

            # Only grab Masters Tournament
            if "Masters" not in name:
                continue

            competitions = event.get("competitions", [])
            if not competitions:
                continue

            competitors = competitions[0].get("competitors", [])

            for player in competitors:
                athlete = player.get("athlete", {})
                display_name = athlete.get("displayName", "Unknown")

                score_raw = player.get("score", "0")

                if score_raw == "E":
                    score = 0
                else:
                    try:
                        score = int(score_raw)
                    except:
                        score = 0

                players[display_name] = score

        if not players:
            print("⚠️ No Masters players found")

    except Exception as e:
        print("❌ ESPN fetch failed:", e)

    return players
