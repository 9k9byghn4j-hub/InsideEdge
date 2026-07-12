import requests

API_KEY = "REDACTED_API_KEY"
BASE = "https://v5.oddspapi.io/en"

r = requests.get(f"{BASE}/fixtures/odds",
    params={"apiKey": API_KEY,
            "fixtureId": "id1000001653452533",
            "bookmakers": "williamhill",
            "mainLine": False})

odds = r.json().get("odds", {}).get("williamhill", {})

print("=== WILLIAM HILL CORRECT SCORE ===")
cs = [(odd.get("outcomeId"), odd.get("price"), odd.get("outcomeName",""), odd.get("name",""))
      for odd in odds.values()
      if odd.get("marketId") == 10336]

for oid, price, name, n2 in sorted(cs, key=lambda x: x[1]):
    print(f"  outcomeId={oid}  price={price:.2f}  name='{name}'  n2='{n2}'")