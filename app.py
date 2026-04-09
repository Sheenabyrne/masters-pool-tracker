def get_leaderboard():
    url = "https://site.web.api.espn.com/apis/v2/sports/golf/leaderboard"

    players = {}

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        # 🔍 DEBUG: print structure
        print("Top-level keys:", list(data.keys()))

        events = data.get("events", [])
        print("Number of events:", len(events))

        for event in events:
            print("Event found:", event.get("name"))

            competitions = event.get("competitions", [])
            if not competitions:
                continue

            competitors = competitions[0].get("competitors", [])
            print("Competitors count:", len(competitors))

            for player in competitors:
                try:
                    name = player.get("athlete", {}).get("displayName", "Unknown")
                    score_raw = player.get("score", "0")

                    if score_raw == "E":
                        score = 0
                    else:
                        score = int(score_raw)

                    players[name] = score

                except Exception as inner_error:
                    print("Player parse error:", inner_error)
                    continue

        if not players:
            print("⚠️ No players parsed from ESPN")

    except Exception as e:
        print("❌ ESPN fetch failed:", e)

    return players
