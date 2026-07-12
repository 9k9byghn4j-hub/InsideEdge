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

# ── Outcome labels ────────────────────────────────────────────────────────────
# Maps outcomeId → human-readable label
# Correct score: IDs follow blocks — home wins 10336-10343, draws 10344-10346,
# away wins 10345+ (overlapping blocks by score group)
OUTCOME_LABELS = {
    # Full Time Result
    101: "Home", 102: "Draw", 103: "Away",

    # Both Teams to Score
    104: "Yes", 105: "No",

    # Draw No Bet — labels substituted with team names at runtime
    10214: "Home (DNB)", 10215: "Away (DNB)",

    # Double Chance
    10168: "Home or Draw", 10169: "Draw or Away", 10170: "Home or Away",

    # Half Time Result
    10799: "HT Home", 10800: "HT Draw", 10801: "HT Away",

    # HT/FT
    101905: "Home / Home", 101906: "Home / Draw", 101907: "Home / Away",
    101908: "Draw / Home", 101909: "Draw / Draw", 101910: "Draw / Away",
    101911: "Away / Home", 101912: "Away / Draw", 101913: "Away / Away",

    # Correct Score — block structure confirmed from multi-bookmaker price analysis
    # Home wins block (10336-10343)
    10336: "1-0",  10337: "2-0",  10338: "2-1",  10339: "3-0",
    10340: "3-1",  10341: "3-2",  10342: "4-0",  10343: "4-1",
    # Draws block (10344-10351)
    10344: "0-0",  10345: "1-1",  10346: "2-2",  10347: "3-3",
    10348: "4-4",  10349: "5-5",  10350: "6-6",  10351: "7-7",
    # Away wins block (10352-10359)
    10352: "0-1",  10353: "0-2",  10354: "1-2",  10355: "0-3",
    10356: "1-3",  10357: "2-3",  10358: "0-4",  10359: "1-4",
    # Higher scores (10360+)
    10360: "2-4",  10361: "3-4",  10362: "4-3",
    10363: "4-2",  10364: "5-0",  10365: "0-5",
    10368: "5-1",  10369: "1-5",  10370: "5-2",  10371: "2-5",
    10372: "Other Score",
    10377: "6-0",  10378: "0-6",

    # Over/Under Goals
    106: "Over 0.5 Goals",  107: "Under 0.5 Goals",
    108: "Over 1.5 Goals",  109: "Under 1.5 Goals",
    1010: "Over 2.5 Goals", 1011: "Under 2.5 Goals",
    1012: "Over 3.5 Goals", 1013: "Under 3.5 Goals",
    1014: "Over 4.5 Goals", 1015: "Under 4.5 Goals",
    1016: "Over 5.5 Goals", 1017: "Under 5.5 Goals",

    # Player Shots (marketId 10743)
    10744: "Over 0.5 Shots", 10745: "Over 1.5 Shots", 10746: "Over 2.5 Shots",
    10747: "Over 3.5 Shots", 10748: "Over 4.5 Shots",
    # Player Shots on Target (marketId 10753)
    10754: "Over 0.5 SoT",   10755: "Over 1.5 SoT",   10756: "Over 2.5 SoT",
    # Player Fouls Committed (marketId 102700)
    102701: "Over 0.5 Fouls", 102702: "Over 1.5 Fouls", 102703: "Over 2.5 Fouls",
    # Player Cards (marketId 102732)
    102733: "Over 0.5 Cards", 102734: "Over 1.5 Cards",
    # Player Tackles (marketId 102659)
    102660: "Over 0.5 Tackles", 102661: "Over 1.5 Tackles", 102662: "Over 2.5 Tackles",
    # Goalkeeper Saves (marketId 102590)
    102591: "Over 0.5 Saves", 102592: "Over 1.5 Saves", 102593: "Over 2.5 Saves",
    # Player Assists (marketId 102606)
    102607: "Over 0.5 Assists", 102608: "Over 1.5 Assists",
    # Player SoT alt IDs
    102624: "Over 0.5 SoT",  102625: "Over 1.5 SoT",
    # Player Shots alt IDs
    102626: "Over 0.5 Shots", 102627: "Over 1.5 Shots", 102628: "Over 2.5 Shots",
    # Player Fouls Won (marketId 102706)
    102706: "Over 0.5 Fouls Won", 102707: "Over 1.5 Fouls Won",
    # Anytime / First / Last goalscorer
    10730: "Anytime Goalscorer", 10731: "First Goalscorer",
    10732: "Last Goalscorer",    10733: "Score 2+ Goals",
}

# Keep old name for backwards compat
PLAYER_LINE_LABELS = {
    # Shots (marketId 10743)
    10744: "Over 0.5 Shots", 10745: "Over 1.5 Shots", 10746: "Over 2.5 Shots",
    10747: "Over 3.5 Shots", 10748: "Over 4.5 Shots",
    # Shots on Target (marketId 10753)
    10754: "Over 0.5 SoT",   10755: "Over 1.5 SoT",   10756: "Over 2.5 SoT",
    # Fouls committed (marketId 102700)
    102701: "Over 0.5 Fouls", 102702: "Over 1.5 Fouls", 102703: "Over 2.5 Fouls",
    # Cards (marketId 102732)
    102733: "Over 0.5 Cards", 102734: "Over 1.5 Cards",
    # Passes (marketId 102716)
    102717: "Over 29.5 Passes", 102718: "Over 39.5 Passes", 102719: "Over 49.5 Passes",
    # Tackles (marketId 102659)
    102660: "Over 0.5 Tackles", 102661: "Over 1.5 Tackles", 102662: "Over 2.5 Tackles",
    # Saves (marketId 102590)
    102591: "Over 0.5 Saves", 102592: "Over 1.5 Saves", 102593: "Over 2.5 Saves",
    # Assists (marketId 102606)
    102607: "Over 0.5 Assists", 102608: "Over 1.5 Assists",
    # Anytime goalscorer related
    10730: "Anytime Goalscorer", 10731: "First Goalscorer", 10732: "Last Goalscorer",
    10733: "Score 2+ Goals",
    # Player shots on target (marketId 102624/102626)
    102624: "Over 0.5 SoT", 102625: "Over 1.5 SoT",
    102626: "Over 0.5 Shots", 102627: "Over 1.5 Shots", 102628: "Over 2.5 Shots",
    # Player fouls won (marketId 102706)
    102706: "Over 0.5 Fouls Won", 102707: "Over 1.5 Fouls Won",
    # Goals (various over/under goal markets)
    106: "Over 0.5 Goals",  107: "Under 0.5 Goals",
    108: "Over 1.5 Goals",  109: "Under 1.5 Goals",
    1010: "Over 2.5 Goals", 1011: "Under 2.5 Goals",
    1012: "Over 3.5 Goals", 1013: "Under 3.5 Goals",
    1014: "Over 4.5 Goals", 1015: "Under 4.5 Goals",
    1016: "Over 5.5 Goals", 1017: "Under 5.5 Goals",
}

# Market ID → friendly name for markets not covered by the /markets endpoint
MARKET_NAME_OVERRIDES = {
    10730: "Anytime Goalscorer",
    10731: "First Goalscorer",
    10732: "Last Goalscorer",
    10733: "Score 2+ Goals",
    10738: "Score Outside Box",
    10743: "Player Shots",
    10753: "Player Shots on Target",
    102590: "Goalkeeper Saves",
    102606: "Player Assists",
    102624: "Player Shots on Target",
    102626: "Player Shots",
    102659: "Player Tackles",
    102700: "Player Fouls Committed",
    102706: "Player Fouls Won",
    102716: "Player Passes",
    102732: "Player Cards",
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

# Player prop market IDs — these are shown in full regardless of edge
PLAYER_MARKET_IDS = {
    10730, 10731, 10732, 10733, 10738,
    10743, 10753,
    102590, 102606, 102624, 102626,
    102659, 102700, 102706, 102716, 102732,
}

def scan_all_markets(all_odds, market_names):
    """Group every odd by (marketId, outcomeId, playerId, handicap).
    
    Match markets: only return where best price is >= MIN_EDGE_PCT above average.
    Player markets: return ALL entries regardless of edge (show every player/line).
    """
    MIN_EDGE_PCT = 1.0   # minimum % above average for match markets
    MIN_BOOKS_MATCH  = 4  # match markets need 4+ books for reliable avg
    MIN_BOOKS_PLAYER = 2  # player props need 2+ books

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
                    "marketName": (MARKET_NAME_OVERRIDES.get(mid)
                               or market_names.get(mid)
                               or f"Market {mid}"),
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
        is_player_mkt = g.get("playerId", 0) != 0 or mid in PLAYER_MARKET_IDS
        min_books = MIN_BOOKS_PLAYER if is_player_mkt else MIN_BOOKS_MATCH
        if len(bm_prices) < min_books:
            continue

        avg = market_avg(bm_prices)
        best_price, best_bm = best_odds(bm_prices)
        if not avg or not best_price:
            continue

        pct = pct_above_avg(best_price, avg)
        is_player = g["marketId"] in PLAYER_MARKET_IDS or g["playerId"] != 0

        # Exclude correct score from match market comparison —
        # prices vary too wildly across books to give meaningful averages
        EXCLUDE_FROM_COMPARISON = {10336}
        if g["marketId"] in EXCLUDE_FROM_COMPARISON:
            continue

        # Match markets: only show if above average by MIN_EDGE_PCT
        # Player markets: show everything (even pct=0) so all lines visible
        if not is_player and pct < MIN_EDGE_PCT:
            continue

        # Sanity check: if best price is more than 3x the average,
        # this is likely a data error or wildly illiquid market — skip it
        if best_price > avg * 3:
            continue

        # Build outcome label
        oid = g["outcomeId"]
        pid = g["playerId"]
        hcp = g["handicap"]
        mkt = g["marketName"]

        # Use known outcome labels where available
        if g["marketId"] == 10336:
            # Correct score — don't guess labels, show TBC until confirmed from OddsPapi
            outcome_label = f"Score (ID {oid})"
        else:
            outcome_label = OUTCOME_LABELS.get(oid) or PLAYER_LINE_LABELS.get(oid) or mkt
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