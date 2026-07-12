import requests
import math
from datetime import datetime

# ── Config ─────────────────────────────────────────────────────────────────────
API_KEY  = ""
BASE     = "https://v5.oddspapi.io/en"

ALL_BOOKMAKERS = [
    "bet365", "betfair-ex", "betway", "boylesports", "bwin",
    "casumo", "coral", "grosvenor", "ladbrokes", "lottoland",
    "paddypower", "partypoker", "pinnacle", "sportingbet", "unibet",
    "virginbet", "williamhill", "betmgm.co.uk", "betuk", "vave",
    "mystake", "allbritishcasino", "leovegas.uk", "fun88.co.uk",
    "888sport", "32red",
]

BENCHMARK_BM     = "betfair-ex"
EXCLUDED_FROM_EV = {"betfair-ex", "betfair-spb"}

BOOKMAKER_LABELS = {
    "32red":           "32Red",
    "888sport":        "888sport",
    "allbritishcasino":"AllBritish",
    "bet365":          "bet365",
    "betfair-ex":      "Betfair Ex",
    "betfair-spb":     "Betfair SPB",
    "betmgm.co.uk":    "BetMGM",
    "betuk":           "BetUK",
    "betway":          "Betway",
    "boylesports":     "BoyleSports",
    "bwin":            "bwin",
    "casumo":          "Casumo",
    "coral":           "Coral",
    "fun88.co.uk":     "Fun88",
    "mystake":         "MyStake",
    "grosvenor":       "Grosvenor",
    "ladbrokes":       "Ladbrokes",
    "leovegas.uk":     "LeoVegas",
    "lottoland":       "Lottoland",
    "paddypower":      "Paddy Power",
    "partypoker":      "PartyPoker",
    "pinnacle":        "Pinnacle",
    "sportingbet":     "Sportingbet",
    "vave":            "Vave",
    "unibet":          "Unibet",
    "virginbet":       "VirginBet",
    "williamhill":     "William Hill",
}

# ── Market definitions ─────────────────────────────────────────────────────────
# Full Time Result: marketId=101, outcomes 101=Home 102=Draw 103=Away
# Both Teams Score: marketId=104, outcomes 104=Yes  105=No
# Over/Under lines: each line is its own marketId, Over=marketId, Under=marketId+1
#   0.5 → 106/107  |  1.5 → 108/109  |  2.5 → 1010/1011
#   3.5 → 1012/13  |  4.5 → 1014/15  |  5.5 → 1016/17
# Half Time Result: marketId=10799, outcomes 10799=Home 10800=Draw (10801=Away likely)
# HT/FT:           marketId=101905, outcomes 101905=1/1 101906=1/X 101907=1/2 etc
# Double Chance:   marketId=10168, outcomes 10168=1X  10169=X2
# Draw No Bet:     marketId=10214, outcomes 10214=Home 10215=Away
# Asian Handicap:  marketId=10300/10302 (lines vary)
# Correct Score:   marketId=10336, outcomes=individual scorelines

MARKETS = {
    "Full Time Result": {
        "id": 101,
        "outcomes": {101: "Home", 102: "Draw", 103: "Away"},
    },
    "Both Teams to Score": {
        "id": 104,
        "outcomes": {104: "Yes", 105: "No"},
    },
    "Over/Under 0.5": {
        "id": 106,
        "outcomes": {106: "Over 0.5", 107: "Under 0.5"},
    },
    "Over/Under 1.5": {
        "id": 108,
        "outcomes": {108: "Over 1.5", 109: "Under 1.5"},
    },
    "Over/Under 2.5": {
        "id": 1010,
        "outcomes": {1010: "Over 2.5", 1011: "Under 2.5"},
    },
    "Over/Under 3.5": {
        "id": 1012,
        "outcomes": {1012: "Over 3.5", 1013: "Under 3.5"},
    },
    "Over/Under 4.5": {
        "id": 1014,
        "outcomes": {1014: "Over 4.5", 1015: "Under 4.5"},
    },
    "Over/Under 5.5": {
        "id": 1016,
        "outcomes": {1016: "Over 5.5", 1017: "Under 5.5"},
    },
    "Double Chance": {
        "id": 10168,
        "outcomes": {10168: "Home or Draw", 10169: "Draw or Away"},
    },
    "Draw No Bet": {
        "id": 10214,
        "outcomes": {10214: "Home", 10215: "Away"},
    },
    "Half Time Result": {
        "id": 10799,
        "outcomes": {10799: "Home", 10800: "Draw", 10801: "Away"},
    },
    "Half Time / Full Time": {
        "id": 101905,
        "outcomes": {
            101905: "Home / Home",
            101906: "Home / Draw",
            101907: "Home / Away",
            101908: "Draw / Home",
            101909: "Draw / Draw",
            101910: "Draw / Away",
            101911: "Away / Home",
            101912: "Away / Draw",
            101913: "Away / Away",
        },
    },
}

# Correct score is special — many outcomes, parse dynamically
CORRECT_SCORE_MARKET_ID = 10336

# ── Player prop market IDs ─────────────────────────────────────────────────────
PLAYER_MARKETS = {
    "Anytime Goalscorer":    {"id": 10730, "over_under": False},
    "First Goalscorer":      {"id": 10731, "over_under": False},
    "Last Goalscorer":       {"id": 10732, "over_under": False},
    "Score 2+ Goals":        {"id": 10733, "over_under": False},
    "Shots on Target":       {"id": 10753, "over_under": True},
    "Shots":                 {"id": 10743, "over_under": True},
    "Fouls Committed":       {"id": 102700, "over_under": True},
    "Cards":                 {"id": 102732, "over_under": True},
}

# outcomeId meaning for over/under player markets
# For shots/fouls etc: lower outcomeId = over, higher = under
# e.g. 10743=Shots market: 10744=Over 0.5, 10745=Over 1.5, 10746=Over 2.5 etc
SHOTS_OUTCOME_LINES = {10744: 0.5, 10745: 1.5, 10746: 2.5, 10747: 3.5, 10748: 4.5}
SOT_OUTCOME_LINES   = {10754: 0.5, 10755: 1.5, 10756: 2.5}
FOULS_OUTCOME_LINES = {102701: 0.5, 102702: 1.5, 102703: 2.5}
CARDS_OUTCOME_LINES = {102733: 0.5, 102734: 1.5}

# Tab groupings for the UI
MARKET_TABS = {
    "Match Result":     ["Full Time Result", "Double Chance", "Draw No Bet"],
    "Goals":            ["Over/Under 2.5", "Over/Under 1.5", "Over/Under 3.5",
                         "Over/Under 0.5", "Over/Under 4.5", "Over/Under 5.5",
                         "Both Teams to Score"],
    "Half Time":        ["Half Time Result", "Half Time / Full Time"],
    "Correct Score":    ["correct_score"],
}

SPORTS = {
    "⚽  World Cup":        {"id": 16,  "sport": 10},
    "⚽  Premier League":   {"id": 17,  "sport": 10},
    "⚽  Champions League": {"id": 132, "sport": 10},
    "⚽  La Liga":          {"id": 8,   "sport": 10},
    "⚽  Bundesliga":       {"id": 35,  "sport": 10},
}

# ── Helpers ────────────────────────────────────────────────────────────────────

def bm_label(slug):
    return BOOKMAKER_LABELS.get(slug, slug)

def fmt_time(unix_ts):
    try:
        dt = datetime.utcfromtimestamp(unix_ts)
        return dt.strftime("%d %b %H:%M")
    except Exception:
        return "—"

def calc_true_prob(bf_odds):
    if bf_odds and bf_odds > 1:
        return 1 / bf_odds
    return None

def calc_ev(true_prob, bm_odds):
    return (true_prob * bm_odds) - 1

def best_odds(bm_price_dict):
    if not bm_price_dict:
        return None, None
    best_bm = max(bm_price_dict, key=lambda b: bm_price_dict[b])
    return bm_price_dict[best_bm], best_bm

def all_odds_ranked(bm_price_dict):
    return sorted(bm_price_dict.items(), key=lambda x: x[1], reverse=True)

def prop_true_prob(bm_prices_all):
    """Tiered true-probability estimate for player props.

    Priority:
      1. Betfair Exchange price (no margin — exchange).
      2. Pinnacle price with ~4% margin share stripped.
      3. Median implied prob across books (min 3) with ~5% margin share stripped.

    bm_prices_all should INCLUDE exchange prices (pass raw parse before exclusion).
    Returns (true_prob, benchmark_label) or (None, None) if not enough data.
    """
    import statistics

    bf_price = bm_prices_all.get(BENCHMARK_BM)
    if bf_price and bf_price > 1:
        return 1 / bf_price, "Betfair Ex"

    pinn = bm_prices_all.get("pinnacle")
    if pinn and pinn > 1:
        # strip approx one-sided margin share (~4%)
        return min(0.99, (1 / pinn) * 0.96), "Pinnacle (devig est)"

    books = {bm: p for bm, p in bm_prices_all.items()
             if bm not in EXCLUDED_FROM_EV and p and p > 1}
    if len(books) >= 3:
        implieds = [1 / p for p in books.values()]
        med = statistics.median(implieds)
        # strip approx one-sided soft-book margin share (~5%)
        return min(0.99, med * 0.95), f"Median ({len(books)} books)"

    return None, None

def ev_opportunities(bm_price_dict, true_prob, min_ev=0.0):
    if not true_prob:
        return []
    opps = []
    for bm, price in bm_price_dict.items():
        ev = calc_ev(true_prob, price)
        if ev >= min_ev:
            opps.append({"bookmaker": bm, "price": price, "ev": ev})
    return sorted(opps, key=lambda x: x["ev"], reverse=True)

# ── API ────────────────────────────────────────────────────────────────────────

def _get(endpoint, params, retries=3):
    """GET with retry and backoff — handles trial-key rate limits."""
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
                # Rate limited — back off and retry
                time.sleep(0.6 * (attempt + 1))
                continue
            return None
        except Exception:
            time.sleep(0.4 * (attempt + 1))
    return None

def fetch_fixtures(tournament_id, status_id=0):
    data = _get("fixtures", {
        "tournamentId": tournament_id,
        "statusId":     status_id,
        "bookmakers":   ",".join(ALL_BOOKMAKERS[:5]),
    })
    if not data or not isinstance(data, list):
        return []

    fixtures = []
    for f in data:
        p = f.get("participants", {})
        fixtures.append({
            "fixtureId":  f["fixtureId"],
            "home":       p.get("participant1Name", "?"),
            "away":       p.get("participant2Name", "?"),
            "home_abbr":  p.get("participant1Abbr", ""),
            "away_abbr":  p.get("participant2Abbr", ""),
            "start":      fmt_time(f.get("startTime", 0)),
            "start_ts":   f.get("startTime", 0),
            "comp":       f.get("tournament", {}).get("tournamentName", ""),
            "venue":      f.get("venue", {}).get("venueName", ""),
            "status":     f.get("status", {}).get("statusId", 0),
        })
    return fixtures

def fetch_fixture_odds(fixture_id):
    """Fetch odds across all bookmakers — chunks fetched concurrently (3 workers
    to stay under trial-key rate limits). _get handles retry/backoff on 429s.
    Returns everything including player props (playerId != 0)."""
    from concurrent.futures import ThreadPoolExecutor, as_completed

    all_odds = {}
    chunks = [ALL_BOOKMAKERS[i:i+5] for i in range(0, len(ALL_BOOKMAKERS), 5)]

    def fetch_chunk(chunk):
        data = _get("fixtures/odds", {
            "fixtureId":  fixture_id,
            "bookmakers": ",".join(chunk),
            "mainLine":   False,
        })
        if data and "odds" in data:
            return data["odds"]
        return {}

    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = [pool.submit(fetch_chunk, chunk) for chunk in chunks]
        for future in as_completed(futures):
            chunk_odds = future.result()
            for bm, bm_odds in chunk_odds.items():
                if bm not in all_odds:
                    all_odds[bm] = {}
                all_odds[bm].update(bm_odds)

    return all_odds

def parse_market(all_odds, market_def, home_name=None, away_name=None):
    """Parse a market definition.
    Returns:
      result    — {outcome_label: {bm: price}} bettable books only (no exchanges)
      bf_probs  — {outcome_label: prob} normalised Betfair Exchange probs ({} if absent)
      raw       — {outcome_label: {bm: price}} ALL books incl. exchanges (for fallback benchmark)
    """
    market_id   = market_def["id"]
    outcome_map = market_def["outcomes"]

    result  = {label: {} for label in outcome_map.values()}
    raw     = {label: {} for label in outcome_map.values()}
    bf_raw  = {}

    for bm, bm_odds in all_odds.items():
        for odd_id, odd in bm_odds.items():
            if odd.get("marketId") != market_id:
                continue
            if not odd.get("active", True):
                continue
            oid   = odd.get("outcomeId")
            label = outcome_map.get(oid)
            if not label:
                continue
            price = odd.get("price")
            if not price or price <= 1:
                continue

            # Substitute real team names
            if home_name and label == "Home":
                label = home_name
            if away_name and label == "Away":
                label = away_name

            raw.setdefault(label, {})[bm] = price
            if bm == BENCHMARK_BM:
                bf_raw[label] = calc_true_prob(price)
            elif bm not in EXCLUDED_FROM_EV:
                result.setdefault(label, {})[bm] = price

    # Normalise Betfair probs (only when Betfair priced ALL outcomes of the market;
    # a partial book can't be normalised meaningfully)
    if bf_raw and len(bf_raw) == len(outcome_map):
        total = sum(v for v in bf_raw.values() if v)
        if total > 0:
            bf_raw = {k: v / total for k, v in bf_raw.items() if v}
    elif bf_raw:
        bf_raw = {}  # partial Betfair coverage — fall back to tiered benchmark

    return result, bf_raw, raw

def parse_correct_score(all_odds):
    """Parse correct score market — outcomes are dynamic scorelines."""
    result = {}
    bf_raw = {}

    for bm, bm_odds in all_odds.items():
        for odd_id, odd in bm_odds.items():
            if odd.get("marketId") != CORRECT_SCORE_MARKET_ID:
                continue
            if not odd.get("active", True):
                continue
            price = odd.get("price")
            if not price or price <= 1:
                continue
            oid   = odd.get("outcomeId")
            label = f"Score {oid}"  # we'll decode below

            if bm == BENCHMARK_BM:
                bf_raw[label] = calc_true_prob(price)
            elif bm not in EXCLUDED_FROM_EV:
                result.setdefault(label, {})[bm] = price

    if bf_raw:
        total = sum(v for v in bf_raw.values() if v)
        if total > 0:
            bf_raw = {k: v / total for k, v in bf_raw.items() if v}

    return result, bf_raw

# ── Player name lookup ─────────────────────────────────────────────────────────

def fetch_player_names(player_ids, api_key=None):
    """Fetch player names via /players endpoint using playerIds filter.
    Response format: [{"playerId": 511, "playerName": "Skjelbred, Per"}, ...]
    Player names come as 'Surname, Firstname' — we reformat to 'Firstname Surname'.
    Returns {playerId: display_name}"""
    if not player_ids:
        return {}
    key = api_key or API_KEY
    names = {}
    pid_list = list(player_ids)

    # Fetch in batches of 50 (URL length safety)
    for i in range(0, len(pid_list), 50):
        batch = pid_list[i:i+50]
        ids_str = ",".join(str(pid) for pid in batch)
        data = _get("players", {"playerIds": ids_str})
        if data and isinstance(data, list):
            for p in data:
                pid  = p.get("playerId")
                raw  = p.get("playerName", "")
                if pid and raw:
                    names[pid] = _format_player_name(raw)
    return names

def _format_player_name(raw):
    """Convert 'Surname, Firstname' -> 'F. Surname' for compact display."""
    if "," in raw:
        surname, firstname = [s.strip() for s in raw.split(",", 1)]
        if firstname:
            return f"{firstname[0]}. {surname}"
        return surname
    return raw

def parse_player_props(all_odds, market_name):
    """Parse player prop market from raw odds.
    Returns list of {playerId, playerName, marketId, outcomeId, line, bm_prices}"""
    mdef = PLAYER_MARKETS.get(market_name)
    if not mdef:
        return [], set()

    market_id   = mdef["id"]
    is_ou       = mdef["over_under"]
    props       = {}  # (playerId, outcomeId) -> {bm: price}
    all_pids    = set()

    for bm, bm_odds in all_odds.items():
        for odd_id, odd in bm_odds.items():
            if odd.get("marketId") != market_id:
                continue
            if not odd.get("active", True):
                continue
            pid   = odd.get("playerId", 0)
            if pid == 0:
                continue
            price = odd.get("price")
            if not price or price <= 1:
                continue
            oid   = odd.get("outcomeId")
            key   = (pid, oid)
            if key not in props:
                props[key] = {"playerId": pid, "outcomeId": oid,
                              "bookmakers": {}, "all_prices": {}}
            # all_prices includes exchanges (for benchmarking)
            props[key]["all_prices"][bm] = price
            # bookmakers excludes exchanges (for EV betting targets)
            if bm not in EXCLUDED_FROM_EV:
                props[key]["bookmakers"][bm] = price
            all_pids.add(pid)

    # Decode lines for over/under markets
    line_maps = {
        10743: SHOTS_OUTCOME_LINES,
        10753: SOT_OUTCOME_LINES,
        102700: FOULS_OUTCOME_LINES,
        102732: CARDS_OUTCOME_LINES,
    }
    line_map = line_maps.get(market_id, {})

    results = []
    for (pid, oid), pdata in props.items():
        line = line_map.get(oid) if is_ou else None
        results.append({
            "playerId":   pid,
            "playerName": f"Player {pid}",  # filled in after name lookup
            "marketId":   market_id,
            "outcomeId":  oid,
            "line":       line,
            "bookmakers": pdata["bookmakers"],
            "all_prices": pdata["all_prices"],
        })

    return results, all_pids

# ── v2: dynamic sports, tournaments, market names ──────────────────────────────

def fetch_sports():
    """List all sports available. Returns [{sportId, sportName}, ...]"""
    data = _get("sports", {})
    return data if isinstance(data, list) else []

def fetch_tournaments(sport_id):
    """List tournaments for a sport."""
    data = _get("tournaments", {"sportId": sport_id})
    return data if isinstance(data, list) else []

def fetch_market_names(sport_id):
    """Map marketId -> marketName for a sport."""
    data = _get("markets", {"sportId": sport_id})
    if isinstance(data, list):
        return {m.get("marketId"): m.get("marketName") for m in data if m.get("marketId")}
    return {}

def market_true_prob(all_prices):
    """True probability = implied prob of the LOWEST odds in the market
    (the sharpest price). Requires at least 2 books to be meaningful.
    Returns (true_prob, benchmark_label) or (None, None)."""
    prices = [p for p in all_prices.values() if p and p > 1]
    if len(prices) < 2:
        return None, None
    return 1 / min(prices), "Sharpest Price"

def scan_all_markets(all_odds, market_names):
    """Generic scanner: group EVERY odd across bookmakers by
    (marketId, outcomeId, playerId, handicap). Nothing pre-mapped, nothing missed.
    Returns list of groups: {marketId, marketName, outcomeId, playerId, handicap,
                             all_prices, bookmakers}"""
    groups = {}
    for bm, bm_odds in all_odds.items():
        for odd_id, odd in bm_odds.items():
            if not odd.get("active", True):
                continue
            price = odd.get("price")
            if not price or price <= 1:
                continue
            mid  = odd.get("marketId")
            oid  = odd.get("outcomeId")
            pid  = odd.get("playerId", 0)
            hcp  = odd.get("handicap")
            key  = (mid, oid, pid, hcp)
            if key not in groups:
                groups[key] = {
                    "marketId":   mid,
                    "marketName": market_names.get(mid, f"Market {mid}"),
                    "outcomeId":  oid,
                    "playerId":   pid,
                    "handicap":   hcp,
                    "all_prices": {},   # every book incl exchanges (benchmark)
                    "bookmakers": {},   # bettable books only (EV targets)
                }
            g = groups[key]
            g["all_prices"][bm] = price
            if bm not in EXCLUDED_FROM_EV:
                g["bookmakers"][bm] = price
    return list(groups.values())
