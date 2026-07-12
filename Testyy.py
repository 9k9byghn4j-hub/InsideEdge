import requests
from collections import defaultdict

API_KEY = "REDACTED_API_KEY"
BASE = "https://v5.oddspapi.io/en"

r = requests.get(f"{BASE}/fixtures/odds",
    params={"apiKey": API_KEY,
            "fixtureId": "id1000001653452533",
            "bookmakers": "bet365,coral",
            "mainLine": False})

odds = r.json().get("odds", {})

TARGET = {10336: "Correct Score", 10168: "Double Chance",
          10214: "Draw No Bet", 101905: "HT/FT",
          10799: "Half Time Result", 101: "Full Time Result"}

seen = {}
for bm, bm_odds in odds.items():
    for odd_id, odd in bm_odds.items():
        mid = odd.get("marketId")
        if mid in TARGET:
            oid = odd.get("outcomeId")
            if (mid, oid) not in seen:
                seen[(mid, oid)] = odd.get("price")

by_market = defaultdict(list)
for (mid, oid), price in seen.items():
    by_market[mid].append((oid, price))

for mid, outcomes in sorted(by_market.items()):
    print(f"\n{TARGET[mid]} (marketId={mid}):")
    for oid, price in sorted(outcomes, key=lambda x: x[1]):
        print(f"  outcomeId={oid}  price={price:.2f}")