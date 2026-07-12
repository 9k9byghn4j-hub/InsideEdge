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
EXCLUDED_FROM_BM = {"betfair-ex", "betfair-spb"}

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

# Tournaments to always try — add more IDs here as needed
PINNED_TOURNAMENT_IDS = {16, 17, 132, 8, 35, 6}  # WC, EPL, UCL, La Liga, Bundesliga, Serie A

# ── Market definitions ─────────────────────────────────────────────────────────
# Markets we show and how to label them
# key = marketId, value = (display_name, is_player_market, exclude_from_comparison)
MARKET_CONFIG = {
    101:    ("Full Time Result",      False, False),
    104:    ("Both Teams to Score",   False, False),
    106:    ("Over/Under Goals",      False, False),
    108:    ("Over/Under Goals",      False, False),
    1010:   ("Over/Under Goals",      False, False),
    1012:   ("Over/Under Goals",      False, False),
    1014:   ("Over/Under Goals",      False, False),
    1016:   ("Over/Under Goals",      False, False),
    10168:  ("Double Chance",         False, False),
    10214:  ("Draw No Bet",           False, False),
    10799:  ("Half Time Result",      False, False),
    101905: ("Half Time / Full Time", False, False),
    10336:  ("Correct Score",         False, True),   # excluded from comparison — prices too varied
    10730:  ("Anytime Goalscorer",    True,  False),
    10731:  ("First Goalscorer",      True,  False),
    10732:  ("Last Goalscorer",       True,  False),
    10733:  ("Score 2+ Goals",        True,  False),
    10738:  ("Score Outside Box",     True,  False),
    10743:  ("Player Shots",          True,  False),
    10753:  ("Player Shots on Target",True,  False),
    102590: ("Goalkeeper Saves",      True,  False),
    102606: ("Player Assists",        True,  False),
    102624: ("Player Shots on Target",True,  False),
    102626: ("Player Shots",          True,  False),
    102659: ("Player Tackles",        True,  False),
    102700: ("Player Fouls Committed",True,  False),
    102706: ("Player Fouls Won",      True,  False),
    102716: ("Player Passes",         True,  False),
    102732: ("Player Cards",          True,  False),
}

# outcomeId → label (confirmed from price analysis + OddsPapi structure)
OUTCOME_LABELS = {
    # Full Time Result
    101: "Home", 102: "Draw", 103: "Away",
    # BTTS
    104: "Yes", 105: "No",
    # Draw No Bet (team names substituted at runtime)
    10214: "Home (DNB)", 10215: "Away (DNB)",
    # Double Chance (team names substituted at runtime)
    10168: "Home or Draw", 10169: "Draw or Away", 10170: "Home or Away",
    # Half Time Result (team names substituted at runtime)
    10799: "HT Home", 10800: "HT Draw", 10801: "HT Away",
    # HT/FT (team names substituted at runtime)
    101905: "Home/Home", 101906: "Home/Draw", 101907: "Home/Away",
    101908: "Draw/Home", 101909: "Draw/Draw", 101910: "Draw/Away",
    101911: "Away/Home", 101912: "Away/Draw", 101913: "Away/Away",
    # Over/Under Goals
    106: "Over 0.5", 107: "Under 0.5",
    108: "Over 1.5", 109: "Under 1.5",
    1010: "Over 2.5", 1011: "Under 2.5",
    1012: "Over 3.5", 1013: "Under 3.5",
    1014: "Over 4.5", 1015: "Under 4.5",
    1016: "Over 5.5", 1017: "Under 5.5",
    # Goalscorer
    10730: "Anytime", 10731: "First", 10732: "Last", 10733: "2+ Goals",
    # Player Shots
    10744: "Over 0.5", 10745: "Over 1.5", 10746: "Over 2.5",
    10747: "Over 3.5", 10748: "Over 4.5",
    # Player SoT
    10754: "Over 0.5", 10755: "Over 1.5", 10756: "Over 2.5",
    102624: "Over 0.5", 102625: "Over 1.5",
    # Player Shots alt
    102626: "Over 0.5", 102627: "Over 1.5", 102628: "Over 2.5",
    # Player Fouls
    102701: "Over 0.5", 102702: "Over 1.5", 102703: "Over 2.5",
    # Player Cards
    102733: "Over 0.5", 102734: "Over 1.5",
    # Player Tackles
    102660: "Over 0.5", 102661: "Over 1.5", 102662: "Over 2.5",
    # Saves
    102591: "Over 0.5", 102592: "Over 1.5", 102593: "Over 2.5",
    # Assists
    102607: "Over 0.5", 102608: "Over 1.5",
    # Fouls Won
    102706: "Over 0.5", 102707: "Over 1.5",
}

# Correct score outcome → score label (home-away format)
# Confirmed block structure: home wins 10336-10343, draws 10344-10351, away wins 10352+
CORRECT_SCORE_LABELS = {
    # Home wins
    10336: "1-0", 10337: "2-0", 10338: "2-1", 10339: "3-0",
    10340: "3-1", 10341: "3-2", 10342: "4-0", 10343: "4-1",
    # Draws
    10344: "0-0", 10345: "1-1", 10346: "2-2", 10347: "3-3",
    10348: "4-4", 10349: "5-5",
    # Away wins
    10352: "0-1", 10353: "0-2", 10354: "1-2", 10355: "0-3",
    10356: "1-3", 10357: "2-3", 10358: "0-4", 10359: "1-4",
    10360: "2-4", 10361: "3-4",
    10362: "4-3", 10363: "4-2",
    10364: "5-0", 10365: "0-5",
    10368: "5-1", 10369: "1-5", 10370: "5-2", 10371: "2-5",
    10372: "Any Other", 10377: "6-0", 10378: "0-6",
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
    prices = [p for p in bm_price_dict.values() if p and p > 1]
    return sum(prices) / len(prices) if prices else None

def pct_above_avg(price, avg):
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
        })
    return fixtures

def fetch_fixture_odds(fixture_id):
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
    for i in range(0, len(player_ids), 50):
        batch = list(player_ids)[i:i+50]
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

def scan_all_markets(all_odds):
    """Scan all odds, only process markets defined in MARKET_CONFIG.
    Returns list of result dicts, one per unique (marketId, outcomeId, playerId, handicap).
    """
    MIN_EDGE_PCT     = 1.0
    MIN_BOOKS_MATCH  = 4
    MIN_BOOKS_PLAYER = 2
    MAX_PRICE_RATIO  = 3.0  # skip if best > avg * this (data error / illiquid)

    raw = {}
    for bm, bm_odds in all_odds.items():
        for odd_id, odd in bm_odds.items():
            if not odd.get("active", True):
                continue
            mid = odd.get("marketId")
            # Only process markets we have config for
            if mid not in MARKET_CONFIG:
                continue
            price = odd.get("price")
            if not price or price <= 1:
                continue
            oid = odd.get("outcomeId")
            pid = odd.get("playerId", 0)
            hcp = odd.get("handicap")
            key = (mid, oid, pid, hcp)
            if key not in raw:
                mkt_name, _, _ = MARKET_CONFIG[mid]
                raw[key] = {
                    "marketId":   mid,
                    "marketName": mkt_name,
                    "outcomeId":  oid,
                    "playerId":   pid,
                    "handicap":   hcp,
                    "bookmakers": {},
                }
            if bm not in EXCLUDED_FROM_BM:
                raw[key]["bookmakers"][bm] = price

    results = []
    for key, g in raw.items():
        mid = g["marketId"]
        mkt_name, is_player, exclude = MARKET_CONFIG[mid]
        bm_prices = g["bookmakers"]

        min_books = MIN_BOOKS_PLAYER if is_player else MIN_BOOKS_MATCH
        if len(bm_prices) < min_books:
            continue

        avg = market_avg(bm_prices)
        best_price, best_bm = best_odds(bm_prices)
        if not avg or not best_price:
            continue

        # Skip wildly illiquid / data-error prices
        if best_price > avg * MAX_PRICE_RATIO:
            continue

        pct = pct_above_avg(best_price, avg)

        # Match markets: must beat average by MIN_EDGE_PCT
        # Player markets & excluded markets: show all
        if not is_player and not exclude and pct < MIN_EDGE_PCT:
            continue

        # Build outcome label
        oid = g["outcomeId"]
        pid = g["playerId"]
        hcp = g["handicap"]

        if mid == 10336:
            # Correct score — use confirmed mapping, show as Home-Away format
            score = CORRECT_SCORE_LABELS.get(oid)
            outcome_label = score if score else f"Score {oid}"
        else:
            base = OUTCOME_LABELS.get(oid, mkt_name)
            outcome_label = base
            if hcp is not None and str(hcp) not in outcome_label:
                outcome_label += f" {hcp}"

        results.append({
            "marketId":      mid,
            "marketName":    mkt_name,
            "outcomeId":     oid,
            "playerId":      pid,
            "handicap":      hcp,
            "outcome_label": outcome_label,
            "bookmakers":    bm_prices,
            "avg_odds":      round(avg, 3),
            "best_price":    best_price,
            "best_bm":       best_bm,
            "pct_above":     pct,
            "is_player":     is_player,
            "exclude":       exclude,
        })

    return sorted(results, key=lambda x: x["pct_above"], reverse=True)