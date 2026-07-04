import requests

API_KEY = "REDACTED_API_KEY"
BASE = "https://v5.oddspapi.io/en"

r = requests.get(f"{BASE}/markets",
    params={"apiKey": API_KEY, "sportId": 10})
data = r.json()

print("=== PLAYER MARKETS ===")
for m in data:
    if m.get("playerMarket") == True:
        print(f"  {m['marketId']} — {m['marketName']}")