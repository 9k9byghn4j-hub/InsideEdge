import requests

API_KEY = "REDACTED_API_KEY"
r = requests.get("https://v5.oddspapi.io/en/fixtures/odds",
    params={"apiKey": API_KEY,
            "fixtureId": "id1000001653452519",  # use a current fixture ID
            "bookmakers": "paddypower,boylesports,888sport"})
print(r.json().get("odds", {}).keys())