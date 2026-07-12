import requests
import statistics
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# ── Config ─────────────────────────────────────────────────────────────────────
API_KEY = ""
BASE    = "https://v5.oddspapi.io/en"

ALL_BOOKMAKERS = [
    "bet365", "betfair-ex", "betway", "boylesports", "bwin",
    "casumo", "coral", "grosvenor", "ladbrokes", "lottoland",
    "paddypower", "partypoker", "pinnacle", "sportingbet", "unibet",
    "virginbet", "williamhill", "betmgm.co.uk", "betuk", "vave",
    "mystake", "allbritishcasino", "leovegas.uk", "fun88.co.uk",
    "888sport", "32red",
]

EXCHANGE_BOOKS   = {"betfair-ex", "betfair-spb"}
EXCLUDED_FROM_BM = {"betfair-ex", "betfair-spb"}  # don't compare vs exchanges

BOOKMAKER_LABELS = {
    "32red": "32Red", "888sport": "888sport", "allbritishcasino": "AllBritish",
    "bet365": "bet365", "betfair-ex": "Betfair Ex", "betfair-spb": "Betfair SPB",
    "betmgm.co.uk": "BetMGM", "betuk": "BetUK", "betway": "Betway",
    "boylesports": "BoyleSports", "bwin": "bwin", "casumo": "Casumo",
    "coral": "Coral", "fun88.co.uk": "Fun88", "mystake": "MyStake",
    "grosvenor": "Grosvenor", "ladbrokes": "Ladbrokes", "leovegas.uk": "LeoVegas",
    "lottoland": "Lottoland", "paddypower": "Paddy Power", "partypoker": "PartyPoker",
    "pinnacle": "Pinnacle", "sportingbet": "Sportingbet", "vave": "Vave",
    "unibet": "Unibet", "virginbet": "VirginBet", "williamhill": "William Hill",
}

SPORTS = {
    "⚽  Football": 10,
    "⛳  Golf":      2,
    "🏏  Cricket":   7,
}

PINNED_TOURNAMENT_IDS = {16, 17, 132}  # World Cup, EPL, UCL

# ── Outcome line labels ─────────────────────────────────────────────────────────
# Maps outcomeId → human-readable label for over/under player markets
PLAYER_LINE_LABELS = {
    # Shots (marketId 10743)
    10744: "Over 0.5 Shots", 10745: "Over 1.5 Shots", 10746: "Over 2.5 Shots",
    10747: "Over 3.5 Shots", 10748: "Over 4.5 Shots",
    # Shots on Target (marketId 10753)
    10754: "Over 0.5 SoT",   10755: "Over 1.5 SoT",   10756: "Over 2.5 SoT",
    # Fouls (marketId 102700)
    102701: "Over 0.5 Fouls", 102702: "Over 1.5 Fouls", 102703: "Over 2.5 Fouls",
    # Cards (marketId 102732)
    102733: "Over 0.5 Cards", 102734: "Over 1.5 Cards",
    # Goals (various over/under goal markets share outcome patterns)
    106: "Over 0.5 Goals", 107: "Under 0.5 Goals",
    108: "Over 1.5 Goals", 109: "Under 1.5 Goals",
    1010: "Over 2.5 Goals", 1011: "Under 2.5 Goals",
    1012: "Over 3.5 Goals", 1013: "Under 3.5 Goals",
    1014: "Over 4.5 Goals", 1015: "Under 4.5 Goals",
    1016: "Over 5.5 Goals", 1017: "Under 5.5 Goals",
}

# ── Helpers ────────────────────────────────────────────────────────────────────

def bm_label(slug):
    return BOOKMAKER_LABELS.get(slug, slug)

def fmt_time(unix_ts):
    try:
        return datetime.utcfromtimestamp(unix_ts).strftime("%d %b %H:%M")
    except Exception:
        return "—"

def best_odds(bm_price_dict):
    if not bm_price_dict:
        return None, None
    best_bm = max(bm_price_dict, key=lambda b: bm_price_dict[b])
    return bm_price_dict[best_bm], best_bm

def all_odds_ranked(bm_price_dict):
    return sorted(bm_price_dict.items(), key=lambda x: x[1], reverse=True)

def market_avg(bm_price_dict):
    """Average odds across all bookmakers — used for comparison."""
    prices = [p for p in bm_price_dict.values() if p and p > 1]
    return sum(prices) / len(prices) if prices else None

def pct_above_avg(price, avg):
    """How much above the market average is this price, as a percentage."""
    if not avg or avg <= 0:
        return 0
    return ((price - avg) / avg) * 100

# ── API ────────────────────────────────────────────────────────────────────────

def _get(endpoint, params, retries=3):
    import time
    for attempt in range(retries):
        try:
            r = requests.get(
                f"{BASE}/{endpoint}",
                params={**params, "apiKey": API_KEY},
                timeout=15,
            )
            if r.status_code == 200:
                return r.json()
            if r.status_code == 429:
                time.sleep(0.8 * (attempt + 1))
                continue
            return None
        except Exception:
            time.sleep(0.4 * (attempt + 1))
    return None

def fetch_tournaments(sport_id):
    data = _get("tournaments", {"sportId": sport_id})
    return data if isinstance(data, list) else []

def fetch_market_names(sport_id):
    data = _get("markets", {"sportId": sport_id})
    if isinstance(data, list):
        return {m.get("marketId"): m.get("marketName")
                for m in data if m.get("marketId")}
    return {}

def fetch_fixtures(tournament_id):
    data = _get("fixtures", {
        "tournamentId": tournament_id,
        "statusId":     0,
        "bookmakers":   ",".join(ALL_BOOKMAKERS[:5]),
    })
    if not data or not isinstance(data, list):
        return []
    fixtures = []
    for f in data:
        p = f.get("participants", {})
        fixtures.append({
            "fixtureId": f["fixtureId"],
            "home":      p.get("participant1Name", "?"),
            "away":      p.get("participant2Name", "?"),
            "home_abbr": p.get("participant1Abbr", ""),
            "away_abbr": p.get("participant2Abbr", ""),
            "start":     fmt_time(f.get("startTime", 0)),
            "start_ts":  f.get("startTime", 0),
            "comp":      f.get("tournament", {}).get("tournamentName", ""),
            "venue":     f.get("venue", {}).get("venueName", ""),
        })
    return fixtures

def fetch_fixture_odds(fixture_id):
    """Fetch all odds concurrently across all bookmaker chunks."""
    all_odds = {}
    chunks = [ALL_BOOKMAKERS[i:i+5] for i in range(0, len(ALL_BOOKMAKERS), 5)]

    def fetch_chunk(chunk):
        data = _get("fixtures/odds", {
            "fixtureId":  fixture_id,
            "bookmakers": ",".join(chunk),
            "mainLine":   False,
        })
        return data["odds"] if data and "odds" in data else {}

    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = [pool.submit(fetch_chunk, chunk) for chunk in chunks]
        for future in as_completed(futures):
            for bm, bm_odds in future.result().items():
                if bm not in all_odds:
                    all_odds[bm] = {}
                all_odds[bm].update(bm_odds)

    return all_odds

def fetch_player_names(player_ids):
    if not player_ids:
        return {}
    names = {}
    pid_list = list(player_ids)
    for i in range(0, len(pid_list), 50):
        batch = pid_list[i:i+50]
        data = _get("players", {"playerIds": ",".join(str(p) for p in batch)})
        if data and isinstance(data, list):
            for p in data:
                pid = p.get("playerId")
                raw = p.get("playerName", "")
                if pid and raw:
                    names[pid] = _fmt_name(raw)
    return names

def _fmt_name(raw):
    if "," in raw:
        surname, firstname = [s.strip() for s in raw.split(",", 1)]
        return f"{firstname[0]}. {surname}" if firstname else surname
    return raw

# ── Scanner ────────────────────────────────────────────────────────────────────

def scan_all_markets(all_odds, market_names):
    """Group every odd by (marketId, outcomeId, playerId, handicap).
    For each group compute:
      - bookmakers: {bm: price} for bettable books
      - avg_odds:   market average across all bettable books
      - best_price, best_bm: top price
      - pct_above:  how much best price beats the average (%)
    Only returns groups where best price is above average by MIN_EDGE%.
    """
    MIN_EDGE_PCT = 1.5   # minimum % above average to show
    MIN_BOOKS    = 3     # need at least this many books to compare meaningfully

    raw = {}
    for bm, bm_odds in all_odds.items():
        for odd_id, odd in bm_odds.items():
            if not odd.get("active", True):
                continue
            price = odd.get("price")
            if not price or price <= 1:
                continue
            mid = odd.get("marketId")
            oid = odd.get("outcomeId")
            pid = odd.get("playerId", 0)
            hcp = odd.get("handicap")
            key = (mid, oid, pid, hcp)
            if key not in raw:
                raw[key] = {
                    "marketId":   mid,
                    "marketName": market_names.get(mid, f"Market {mid}"),
                    "outcomeId":  oid,
                    "playerId":   pid,
                    "handicap":   hcp,
                    "bookmakers": {},
                }
            if bm not in EXCLUDED_FROM_BM:
                raw[key]["bookmakers"][bm] = price

    results = []
    for key, g in raw.items():
        bm_prices = g["bookmakers"]
        if len(bm_prices) < MIN_BOOKS:
            continue

        avg = market_avg(bm_prices)
        best_price, best_bm = best_odds(bm_prices)
        if not avg or not best_price:
            continue

        pct = pct_above_avg(best_price, avg)
        if pct < MIN_EDGE_PCT:
            continue

        # Build outcome label
        oid = g["outcomeId"]
        pid = g["playerId"]
        hcp = g["handicap"]
        mkt = g["marketName"]

        # Use known line labels where available
        outcome_label = PLAYER_LINE_LABELS.get(oid, mkt)
        if hcp is not None and str(hcp) not in outcome_label:
            outcome_label += f" {hcp}"

        results.append({
            "marketId":     g["marketId"],
            "marketName":   mkt,
            "outcomeId":    oid,
            "playerId":     pid,
            "handicap":     hcp,
            "outcome_label": outcome_label,
            "bookmakers":   bm_prices,
            "avg_odds":     round(avg, 3),
            "best_price":   best_price,
            "best_bm":      best_bm,
            "pct_above":    pct,
        })

    return sorted(results, key=lambda x: x["pct_above"], reverse=True)