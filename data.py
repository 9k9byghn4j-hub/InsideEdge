import requests
import math
import statistics
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

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

EXCHANGE_BOOKS    = {"betfair-ex", "betfair-spb"}
EXCLUDED_FROM_EV  = {"betfair-ex", "betfair-spb"}

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
    "⛳  Golf":     2,
    "🏏  Cricket":  7,
}

# Tournament IDs always fetched first for football
PINNED_TOURNAMENT_IDS = {16, 17, 132}  # World Cup, EPL, UCL

# ── Helpers ────────────────────────────────────────────────────────────────────

def bm_label(slug):
    return BOOKMAKER_LABELS.get(slug, slug)

def fmt_time(unix_ts):
    try:
        return datetime.utcfromtimestamp(unix_ts).strftime("%d %b %H:%M")
    except Exception:
        return "—"

def calc_ev(true_prob, bm_odds):
    return (true_prob * bm_odds) - 1

def best_odds(bm_price_dict):
    if not bm_price_dict:
        return None, None
    best_bm = max(bm_price_dict, key=lambda b: bm_price_dict[b])
    return bm_price_dict[best_bm], best_bm

def all_odds_ranked(bm_price_dict):
    return sorted(bm_price_dict.items(), key=lambda x: x[1], reverse=True)

# ── True probability ───────────────────────────────────────────────────────────

def true_prob_for_market(outcome_all_prices_list):
    """Given a list of {bm: price} dicts (one per outcome in a market),
    compute true probability for each outcome using the best available benchmark.

    Key rules:
    - Requires at least 2 outcomes in the market group before normalising.
      Single-outcome groups would normalise to 100% — a nonsense result.
    - True prob is capped at 0.95 to prevent degenerate EV on near-certainties.
    - Returns list of (true_prob, benchmark) in same order as input.
    """
    n = len(outcome_all_prices_list)
    if n == 0:
        return []

    # Require at least 2 outcomes for meaningful normalisation
    # Single-outcome markets (e.g. one side of a handicap with no other side priced)
    # cannot be reliably benchmarked — skip them
    if n < 2:
        return [(None, None)]

    # --- Try Betfair Exchange ---
    # Need BF price for ALL outcomes; total implied 0.90–1.15 = liquid
    bf_implieds = []
    for prices in outcome_all_prices_list:
        bf_p = prices.get("betfair-ex") or prices.get("betfair-spb")
        if bf_p and bf_p > 1:
            bf_implieds.append(1 / bf_p)
        else:
            bf_implieds.append(None)

    if all(v is not None for v in bf_implieds):
        bf_total = sum(bf_implieds)
        if 0.90 <= bf_total <= 1.15:
            return [(min(0.95, v / bf_total), "Betfair Ex") for v in bf_implieds]

    # --- Devigged median + market normalisation ---
    raw_medians = []
    book_counts = []
    for prices in outcome_all_prices_list:
        bm_p = [p for bm, p in prices.items() if bm not in EXCHANGE_BOOKS and p and p > 1]
        if not bm_p:
            raw_medians.append(None)
            book_counts.append(0)
            continue
        implieds = sorted(1/p for p in bm_p)
        # Trim outliers when enough books
        if len(implieds) >= 6:
            implieds = implieds[1:-1]
        raw_medians.append(statistics.median(implieds))
        book_counts.append(len(bm_p))

    # Need at least 2 outcomes with actual prices to normalise meaningfully
    priced_count = sum(1 for v in raw_medians if v is not None)
    if priced_count < 2:
        return [(None, None)] * n

    total = sum(v for v in raw_medians if v)
    if total <= 0:
        return [(None, None)] * n

    results = []
    for v, bc in zip(raw_medians, book_counts):
        if v is not None:
            results.append((min(0.95, v / total), f"Devigged ({bc} books)"))
        else:
            results.append((None, None))
    return results

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
        return {m.get("marketId"): m.get("marketName") for m in data if m.get("marketId")}
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
    """Fetch all odds concurrently across all bookmakers."""
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
    """Fetch player names via /players?playerIds=... endpoint."""
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
                    names[pid] = _fmt_player_name(raw)
    return names

def _fmt_player_name(raw):
    if "," in raw:
        surname, firstname = [s.strip() for s in raw.split(",", 1)]
        return f"{firstname[0]}. {surname}" if firstname else surname
    return raw

# ── Generic market scanner ─────────────────────────────────────────────────────

def scan_all_markets(all_odds, market_names):
    """Scan every odd, group by market+outcome+player+handicap, compute true probs
    at market level with normalisation. Returns list of opportunity dicts."""

    # Step 1: collect raw data per group
    # key = (marketId, outcomeId, playerId, handicap)
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
                    "all_prices": {},
                    "bookmakers": {},
                }
            raw[key]["all_prices"][bm] = price
            if bm not in EXCLUDED_FROM_EV:
                raw[key]["bookmakers"][bm] = price

    # Step 2: group keys by market context
    # For non-player markets: group by (marketId, handicap) — all outcomes of a market
    # For player markets: group by (marketId, playerId) — all lines for one player+market
    market_ctx = {}
    for key, g in raw.items():
        mid, oid, pid, hcp = key
        if pid:
            ctx = ("player", mid, pid)    # player: group by market+player
        else:
            ctx = ("market", mid, hcp)    # non-player: group by market+handicap
        if ctx not in market_ctx:
            market_ctx[ctx] = []
        market_ctx[ctx].append(key)

    # Step 3: compute true probs per market context
    results = []
    for ctx, keys in market_ctx.items():
        groups = [raw[k] for k in keys]
        price_lists = [g["all_prices"] for g in groups]
        probs = true_prob_for_market(price_lists)

        for g, (tp, bm_label_str) in zip(groups, probs):
            g["true_prob"] = tp
            g["benchmark"] = bm_label_str
            results.append(g)

    return results