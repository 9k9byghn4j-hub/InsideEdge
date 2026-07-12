import requests

API_KEY = "REDACTED_API_KEY"
BASE = "https://v5.oddspapi.io/en"

chunk = "casumo,coral,grosvenor,ladbrokes,lottoland"

r = requests.get(f"{BASE}/fixtures/odds",
    params={"apiKey": API_KEY,
            "fixtureId": "id1000001653452533",
            "bookmakers": chunk,
            "mainLine": False})

data = r.json()
odds = data.get("odds", {})
print(f"Bookmakers returned: {list(odds.keys())}")
for bm, bm_odds in odds.items():
    props = sum(1 for o in bm_odds.values() if o.get("playerId", 0) != 0)
    print(f"  {bm}: {len(bm_odds)} odds, {props} player props")