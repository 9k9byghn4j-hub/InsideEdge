import requests

API_KEY = "REDACTED_API_KEY"
BASE = "https://v5.oddspapi.io/en"

# Get current WC fixture
r = requests.get(f"{BASE}/fixtures",
    params={"apiKey": API_KEY, "tournamentId": 16, "statusId": 0,
            "bookmakers": "bet365"})
fixtures = r.json()
fid = fixtures[0]["fixtureId"]
home = fixtures[0]["participants"]["participant1Name"]
away = fixtures[0]["participants"]["participant2Name"]
print(f"Fixture: {home} v {away}")

# Get bet365 correct score odds
r2 = requests.get(f"{BASE}/fixtures/odds",
    params={"apiKey": API_KEY, "fixtureId": fid,
            "bookmakers": "bet365", "mainLine": False})
odds = r2.json().get("odds", {}).get("bet365", {})

cs = [(odd.get("outcomeId"), odd.get("price"))
      for odd in odds.values() if odd.get("marketId") == 10336]

print(f"\nbet365 Correct Score — {home} v {away}")
print("outcomeId | price | our label")
print("-" * 45)

CURRENT_MAP = {
    10336: "1-0", 10337: "2-0", 10338: "2-1", 10339: "3-0",
    10340: "3-1", 10341: "3-2", 10342: "4-0", 10343: "4-1",
    10344: "0-0", 10345: "1-1", 10346: "2-2", 10347: "3-3",
    10352: "0-1", 10353: "0-2", 10354: "1-2", 10355: "0-3",
    10356: "1-3", 10357: "2-3",
}

for oid, price in sorted(cs, key=lambda x: x[1]):
    label = CURRENT_MAP.get(oid, "UNKNOWN")
    print(f"  {oid}  |  {price:6.2f}  |  {label}")