import requests
from bs4 import BeautifulSoup

def fetch_live_scores():
    url = "https://www.masters.com/en_US/scores/index.html"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    scores = {}

    # Masters site uses structured rows
    rows = soup.select("tr")

    for row in rows:
        name_tag = row.select_one(".player-name")
        score_tag = row.select_one(".player-score")

        if name_tag and score_tag:
            name = name_tag.text.strip()
            score_text = score_tag.text.strip()

            # Convert score
            if score_text == "E":
                score = 0
            else:
                try:
                    score = int(score_text)
                except:
                    continue

            scores[name] = score

    return scores
