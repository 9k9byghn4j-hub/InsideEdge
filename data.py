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

def _get(endpoint, params):
    try:
        r = requests.get(
            f"{BASE}/{endpoint}",
            params={**params, "apiKey": API_KEY},
            timeout=12,
        )
        if r.status_code == 200:
            return r.json()
        return None
    except Exception:
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
    """Fetch odds across all bookmakers in chunks of 5."""
    all_odds = {}
    chunks = [ALL_BOOKMAKERS[i:i+5] for i in range(0, len(ALL_BOOKMAKERS), 5)]
    for chunk in chunks:
        data = _get("fixtures/odds", {
            "fixtureId":  fixture_id,
            "bookmakers": ",".join(chunk),
            "mainLine":   False,
        })
        if data and "odds" in data:
            for bm, bm_odds in data["odds"].items():
                if bm not in all_odds:
                    all_odds[bm] = {}
                all_odds[bm].update(bm_odds)
    return all_odds

def parse_market(all_odds, market_def, home_name=None, away_name=None):
    """Parse a market definition into {outcome_label: {bm: price}} and bf_probs.
    If home_name/away_name provided, substitutes 'Home'/'Away' labels."""
    market_id   = market_def["id"]
    outcome_map = market_def["outcomes"]

    result  = {label: {} for label in outcome_map.values()}
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

            if bm == BENCHMARK_BM:
                bf_raw[label] = calc_true_prob(price)
            elif bm not in EXCLUDED_FROM_EV:
                result.setdefault(label, {})[bm] = price

    # Normalise Betfair probs
    if bf_raw:
        total = sum(v for v in bf_raw.values() if v)
        if total > 0:
            bf_raw = {k: v / total for k, v in bf_raw.items() if v}

    return result, bf_raw

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