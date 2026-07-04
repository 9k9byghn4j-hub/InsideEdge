import requests

# Test if OddsPapi playerIds match SofaScore playerIds
test_ids = [290927, 1848612, 1564490, 2716582]

for pid in test_ids:
    r = requests.get(
        f"https://api.sofascore.com/api/v1/player/{pid}",
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
            "Referer": "https://www.sofascore.com"
        },
        timeout=5
    )
    if r.status_code == 200:
        name = r.json().get("player", {}).get("name", "?")
        print(f"{pid} → {name}")
    else:
        print(f"{pid} → {r.status_code}")