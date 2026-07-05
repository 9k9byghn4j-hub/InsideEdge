import requests

API_KEY = "REDACTED_API_KEY"
BASE = "https://v5.oddspapi.io/en"

# Known player ID from Brazil v Norway odds
test_pid = 290927

patterns = [
    ("players bulk",      f"{BASE}/players",              {"apiKey": API_KEY, "sportId": 10}),
    ("players by fixture",f"{BASE}/players",              {"apiKey": API_KEY, "fixtureId": "id1000001653452519"}),
    ("player single",     f"{BASE}/players/{test_pid}",   {"apiKey": API_KEY}),
    ("participants sport",f"{BASE}/participants",         {"apiKey": API_KEY, "sportId": 10, "type": "player"}),
    ("squads",            f"{BASE}/squads",               {"apiKey": API_KEY, "fixtureId": "id1000001653452519"}),
    ("lineups",           f"{BASE}/lineups",              {"apiKey": API_KEY, "fixtureId": "id1000001653452519"}),
]

for name, url, params in patterns:
    try:
        r = requests.get(url, params=params, timeout=8)
        print(f"{name}: {r.status_code} — {str(r.json())[:120]}")
    except Exception as e:
        print(f"{name}: ERROR {e}")