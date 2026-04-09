def calculate_scores(leaderboard):
    with open("picks.json") as f:
        picks = json.load(f)

    # Normalize leaderboard names
    normalized_leaderboard = {
        normalize(name): score for name, score in leaderboard.items()
    }

    results = []

    for person, players in picks.items():
        total = 0
        missing = []
        matched_players = []

        for player in players:
            key = normalize(player)

            # 🔥 Try direct match
            if key in normalized_leaderboard:
                total += normalized_leaderboard[key]
                matched_players.append(player)
            else:
                # 🔥 Try fuzzy match (partial match)
                found = False
                for lb_name, lb_score in normalized_leaderboard.items():
                    if key in lb_name or lb_name in key:
                        total += lb_score
                        matched_players.append(player)
                        found = True
                        break

                if not found:
                    missing.append(player)

        results.append({
            "name": person,
            "total": total,
            "missing": missing,
            "matched": matched_players
        })

    return sorted(results, key=lambda x: x["total"])
