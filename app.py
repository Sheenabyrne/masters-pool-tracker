def get_leaderboard():
    # ESPN Masters Tournament endpoint (event-specific)
    url = "https://site.web.api.espn.com/apis/v2/sports/golf/pga/leaderboard"

    players = {}

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        # Find the Masters event
        events = data.get("events", [])

        masters_event = None
        for event in events:
            if "Masters" in event.get("name", ""):
                masters_event = event
                break

        if not masters_event:
            print("Masters event not found")
            return {}

        competitors = masters_event["competitions"][0]["competitors"]

        for player in competitors:
            name = player["athlete"]["displayName"]
            score = player.get("score", "0")

            # Convert score safely
            if score == "E":
                score = 0
            else:
                try:
                    score = int(score)
                except:
                    score = 0

            players[name] = score

    except Exception as e:
        print("ESPN fetch failed:", e)

    return players
