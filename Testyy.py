import requests

API_KEY = "REDACTED_API_KEY"
BASE = "https://v5.oddspapi.io/en"

r = requests.get(f"{BASE}/fixtures/odds",
    params={
        "apiKey": API_KEY,
        "fixtureId": "id1000001653452519",
        "bookmakers": "bet365,ladbrokes,coral,paddypower,williamhill",
    })

odds = r.json().get("odds", {})

# Show full detail of first 5 player props across all markets
print("=== SAMPLE PLAYER PROP ODDS ===")
count = 0
for bm, bm_odds in odds.items():
    for odd_id, odd in bm_odds.items():
        if odd.get("playerId", 0) != 0 and count < 20:
            print(f"oddId: {odd_id}")
            print(f"  bm={bm} marketId={odd.get('marketId')} outcomeId={odd.get('outcomeId')}")
            print(f"  playerId={odd.get('playerId')} playerName={odd.get('playerName')}")
            print(f"  handicap={odd.get('handicap')} price={odd.get('price')} active={odd.get('active')}")
            print()
            count += 1