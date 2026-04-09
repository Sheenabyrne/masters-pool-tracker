def get_leaderboard():
    url = "https://site.web.api.espn.com/apis/v2/sports/golf/leaderboard"

    players = {}

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        events = data.get("events", [])

        for event in events:
            event_name = event.get("name", "")

            # Look for Masters Tournament
            if "Masters" in event_name:
                competitions = event.get("competitions", [])

                if not competitions:
                    continue

                competitors = competitions[0].get("competitors", [])

                for player in competitors:
                    athlete = player.get("athlete", {})
                    name = athlete.get("displayName", "Unknown")

                    score = player.get("score", "0")

                    # Safe score conversion
                    if score == "E":
                        score = 0
                    else:
                        try:
                            score = int(score)
                        except:
                            score = 0

                    players[name] = score

        if not players:
            print("No Masters data found from ESPN")

    except Exception as e:
        print("ESPN fetch failed:", e)

    return players
