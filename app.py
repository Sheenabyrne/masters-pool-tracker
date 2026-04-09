def get_leaderboard():
    url = "https://site.api.cbssports.com/golf/leaderboard/live"

    players = {}

    try:
        response = requests.get(url, timeout=10)

        # 🔥 Check if response is valid
        if response.status_code != 200:
            print("CBS request failed:", response.status_code)
            return players

        try:
            data = response.json()
        except Exception as e:
            print("JSON parse failed:", e)
            return players

        leaderboard = data.get("leaderboard", [])

        for player in leaderboard:
            try:
                name = player.get("player_name", "").strip()

                score_raw = player.get("score", "0")

                if score_raw == "E":
                    score = 0
                else:
                    score = int(score_raw)

                if "," in name:
                    parts = name.split(",")
                    name = parts[1].strip() + " " + parts[0].strip()

                players[name] = score

            except Exception as inner_error:
                print("Player parse error:", inner_error)
                continue

    except Exception as e:
        print("CBS fetch failed:", e)

    return players
