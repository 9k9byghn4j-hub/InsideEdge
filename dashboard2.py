import streamlit as st
import requests
from datetime import datetime

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EDGEVIEW",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Styling ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0a0a0f;
    color: #e8e8f0;
}
.stApp { background-color: #0a0a0f; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1rem 1.5rem 2rem 1.5rem; max-width: 100%; }

.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid #1e1e2e;
    padding-bottom: 0.75rem;
    margin-bottom: 1.25rem;
}
.logo {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.25rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    color: #00e5a0;
}
.logo span { color: #5a5a7a; }
.timestamp { font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: #5a5a7a; }

.section-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 0.2em;
    color: #5a5a7a;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
    border-left: 2px solid #00e5a0;
    padding-left: 0.5rem;
}

.ev-card {
    background: #12121a;
    border: 1px solid #1e1e2e;
    border-radius: 6px;
    padding: 0.85rem 1rem;
    margin-bottom: 0.6rem;
    position: relative;
    overflow: hidden;
}
.ev-card:hover { border-color: #2e2e4e; }
.ev-card-accent {
    position: absolute; top: 0; left: 0; height: 100%;
    background: linear-gradient(90deg, rgba(0,229,160,0.07), transparent);
    border-left: 3px solid #00e5a0;
    pointer-events: none;
}
.match-name { font-size: 0.82rem; font-weight: 600; color: #e8e8f0; margin-bottom: 0.2rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.match-meta { font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; color: #5a5a7a; margin-bottom: 0.55rem; }
.card-row { display: flex; align-items: center; justify-content: space-between; gap: 0.5rem; }
.outcome-label { font-size: 0.75rem; color: #9a9ab0; flex: 1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.bookie-tag { font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; background: #1e1e2e; color: #9a9ab0; padding: 0.15rem 0.4rem; border-radius: 3px; }
.odds-value { font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; font-weight: 500; color: #e8e8f0; min-width: 2.5rem; text-align: right; }
.ev-badge { font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; font-weight: 700; color: #00e5a0; min-width: 3.5rem; text-align: right; }
.ev-bar-wrap { height: 3px; background: #1e1e2e; border-radius: 2px; margin-top: 0.55rem; overflow: hidden; }
.ev-bar-fill { height: 100%; border-radius: 2px; background: linear-gradient(90deg, #00e5a0, #00ffb3); }

.explorer-card { background: #12121a; border: 1px solid #1e1e2e; border-radius: 6px; padding: 1rem; margin-bottom: 0.6rem; }
.explorer-match-header { font-size: 0.9rem; font-weight: 600; color: #e8e8f0; margin-bottom: 0.25rem; }
.explorer-meta { font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; color: #5a5a7a; margin-bottom: 0.75rem; }
.odds-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 0.5rem; margin-bottom: 0.5rem; }
.odds-cell { background: #0a0a0f; border: 1px solid #1e1e2e; border-radius: 4px; padding: 0.5rem; text-align: center; }
.odds-cell-label { font-size: 0.6rem; color: #5a5a7a; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.2rem; }
.odds-cell-value { font-family: 'JetBrains Mono', monospace; font-size: 0.9rem; font-weight: 700; color: #00e5a0; }
.odds-cell-bookie { font-family: 'JetBrains Mono', monospace; font-size: 0.6rem; color: #5a5a7a; }

.stat-pill { display: inline-block; font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; background: #1e1e2e; color: #9a9ab0; padding: 0.2rem 0.5rem; border-radius: 3px; margin-right: 0.3rem; margin-bottom: 0.3rem; }
.stat-pill-green { background: rgba(0,229,160,0.12); color: #00e5a0; }


.prob-row {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-top: 0.6rem;
    padding-top: 0.6rem;
    border-top: 1px solid #1e1e2e;
}
.prob-item { display: flex; flex-direction: column; }
.prob-label { font-family: 'JetBrains Mono', monospace; font-size: 0.58rem; color: #5a5a7a; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.15rem; }
.prob-value-dim { font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; font-weight: 600; color: #5a5a7a; }
.prob-value-green { font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; font-weight: 700; color: #00e5a0; }
.prob-arrow { color: #2e2e4e; font-size: 0.9rem; margin-top: 0.8rem; }
.match-ev-row { display: flex; align-items: center; gap: 0.5rem; padding: 0.35rem 0; border-bottom: 1px solid #1e1e2e; }
.match-ev-row:last-child { border-bottom: none; }

div[data-testid="stSelectbox"] > div > div { background: #12121a !important; border: 1px solid #1e1e2e !important; color: #e8e8f0 !important; font-family: 'JetBrains Mono', monospace !important; font-size: 0.8rem !important; }
div[data-testid="stSlider"] label { color: #5a5a7a !important; font-size: 0.75rem !important; }
div[data-testid="stMultiSelect"] > div > div { background: #12121a !important; border: 1px solid #1e1e2e !important; }
.stButton > button { background: #12121a !important; border: 1px solid #1e1e2e !important; color: #9a9ab0 !important; font-family: 'JetBrains Mono', monospace !important; font-size: 0.7rem !important; letter-spacing: 0.1em !important; border-radius: 4px !important; }
.stButton > button:hover { border-color: #00e5a0 !important; color: #00e5a0 !important; }
div[data-testid="stMetric"] { background: #12121a; border: 1px solid #1e1e2e; border-radius: 6px; padding: 0.75rem 1rem; }
div[data-testid="stMetric"] label { font-family: 'JetBrains Mono', monospace !important; font-size: 0.65rem !important; color: #5a5a7a !important; text-transform: uppercase !important; letter-spacing: 0.1em !important; }
div[data-testid="stMetric"] div[data-testid="stMetricValue"] { font-family: 'JetBrains Mono', monospace !important; font-size: 1.4rem !important; color: #e8e8f0 !important; }
</style>
""", unsafe_allow_html=True)

# ── Config ─────────────────────────────────────────────────────────────────────
ODDSPAPI_KEY  = st.secrets.get("ODDSPAPI_KEY", "")
ODDSAPI_KEY   = st.secrets.get("ODDS_API_KEY", "")   # Betfair benchmark only

ODDSPAPI_BASE = "https://api.oddspapi.io/v4"
ODDSAPI_BASE  = "https://api.the-odds-api.com/v4/sports"

# OddsPapi tournament IDs
SPORTS = {
    "⚽ World Cup":          {"oddspapi_id": 16,  "oddsapi_key": "soccer_fifa_world_cup"},
    "⚽ Premier League":     {"oddspapi_id": 17,  "oddsapi_key": "soccer_epl"},
    "⚽ Champions League":   {"oddspapi_id": 132, "oddsapi_key": "soccer_uefa_champions_league"},
}

# OddsPapi market ID for Full Time Result (1X2)
H2H_MARKET = 101
# Outcome IDs within market 101: 101=Home, 102=Draw, 103=Away

EXCLUDED_BOOKMAKERS = {"betfair-ex", "matchbook", "smarkets"}

# ── Betfair Exchange: true probabilities via The Odds API ──────────────────────
@st.cache_data(ttl=60)
def fetch_betfair_probs(oddsapi_key):
    """Returns dict: fixture_key -> {team_name: prob}
       fixture_key = 'home_team|away_team' lowercased"""
    probs = {}
    for sport_cfg in SPORTS.values():
        sport_key = sport_cfg["oddsapi_key"]
        try:
            r = requests.get(
                f"{ODDSAPI_BASE}/{sport_key}/odds",
                params={
                    "apiKey": oddsapi_key,
                    "regions": "uk",
                    "markets": "h2h",
                    "oddsFormat": "decimal",
                    "bookmakers": "betfair_ex_uk",
                },
                timeout=10,
            )
            if r.status_code != 200:
                continue
            for game in r.json():
                for bm in game.get("bookmakers", []):
                    if bm["key"] != "betfair_ex_uk":
                        continue
                    for market in bm.get("markets", []):
                        if market["key"] != "h2h":
                            continue
                        outcomes = [o for o in market["outcomes"] if o["price"] > 1]
                        total_implied = sum(1 / o["price"] for o in outcomes)
                        if total_implied == 0:
                            continue
                        fixture_key = f"{game['home_team'].lower()}|{game['away_team'].lower()}"
                        probs[fixture_key] = {
                            o["name"]: (1 / o["price"]) / total_implied
                            for o in outcomes
                        }
        except Exception:
            pass
    return probs

# ── OddsPapi: fixtures + odds ──────────────────────────────────────────────────
@st.cache_data(ttl=60)
def fetch_oddspapi_fixtures(tournament_id, api_key):
    try:
        r = requests.get(
            f"{ODDSPAPI_BASE}/fixtures",
            params={"apiKey": api_key, "tournamentId": tournament_id},
            timeout=10,
        )
        if r.status_code == 200:
            return [f for f in r.json() if f.get("statusId") in [0, 1]]
        return []
    except Exception:
        return []

@st.cache_data(ttl=60)
def fetch_oddspapi_odds(fixture_id, api_key):
    try:
        r = requests.get(
            f"{ODDSPAPI_BASE}/odds",
            params={"apiKey": api_key, "fixtureId": fixture_id},
            timeout=10,
        )
        if r.status_code == 200:
            return r.json().get("bookmakerOdds", {})
        return {}
    except Exception:
        return {}

@st.cache_data(ttl=60)
def fuzzy_match(name, candidates):
    """Find best matching team name from Betfair's candidate list."""
    name_lower = name.lower().strip()
    # Exact match
    for c in candidates:
        if c.lower().strip() == name_lower:
            return c
    # Starts with
    for c in candidates:
        if c.lower().startswith(name_lower) or name_lower.startswith(c.lower()):
            return c
    # One name contains the other
    for c in candidates:
        if name_lower in c.lower() or c.lower() in name_lower:
            return c
    return None

def parse_fixture_time(start_time):
    try:
        dt = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
        return dt.strftime("%d %b %H:%M")
    except Exception:
        return start_time[:10]

def get_h2h_odds(bookmaker_odds):
    """Extract H2H (market 101) odds from OddsPapi bookmakerOdds dict.
    Returns: list of {bookmaker, home_odds, draw_odds, away_odds}"""
    results = []
    market_id = str(H2H_MARKET)
    for bm_key, bm_data in bookmaker_odds.items():
        if bm_key in EXCLUDED_BOOKMAKERS:
            continue
        if not bm_data.get("bookmakerIsActive", True):
            continue
        markets = bm_data.get("markets", {})
        if market_id not in markets:
            continue
        market = markets[market_id]
        if not market.get("marketActive", True) is not False:
            pass  # include inactive markets (pre-match they show as False)
        outcomes = market.get("outcomes", {})
        try:
            home = outcomes.get("101", {}).get("players", {}).get("0", {}).get("price")
            draw = outcomes.get("102", {}).get("players", {}).get("0", {}).get("price")
            away = outcomes.get("103", {}).get("players", {}).get("0", {}).get("price")
            if home and draw and away:
                results.append({
                    "bookmaker": bm_key,
                    "home": home,
                    "draw": draw,
                    "away": away,
                })
        except Exception:
            continue
    return results



# ── Default sport (before UI renders) ────────────────────────────────────────
sport_cfg = SPORTS[list(SPORTS.keys())[0]]

# ── Key check ─────────────────────────────────────────────────────────────────
if not ODDSPAPI_KEY:
    st.error("Add ODDSPAPI_KEY to Streamlit secrets.")
    st.stop()
if not ODDSAPI_KEY:
    st.error("Add ODDS_API_KEY to Streamlit secrets (used for Betfair benchmark only).")
    st.stop()

# ── Fetch data ─────────────────────────────────────────────────────────────────
with st.spinner(""):
    betfair_probs = fetch_betfair_probs(ODDSAPI_KEY)
    fixtures = fetch_oddspapi_fixtures(sport_cfg["oddspapi_id"], ODDSPAPI_KEY)

if not fixtures:
    st.markdown("""
    <div style="text-align:center; padding:4rem; color:#5a5a7a;
         font-family:'JetBrains Mono',monospace; font-size:0.8rem;">
        NO UPCOMING FIXTURES FOUND
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── Build match data ───────────────────────────────────────────────────────────
all_opportunities = []
match_summaries = []

# All Betfair team names for fuzzy matching
all_bf_names = list({name for probs in betfair_probs.values() for name in probs.keys()})

for fixture in fixtures[:20]:
    fid       = fixture["fixtureId"]
    home_name = fixture.get("participant1Name", f"Team {fixture.get('participant1Id')}")
    away_name = fixture.get("participant2Name", f"Team {fixture.get('participant2Id')}")
    start_fmt = parse_fixture_time(fixture.get("startTime", ""))
    match_name = f"{home_name} v {away_name}"

    # Betfair true probs — fuzzy match team names
    bf_home = fuzzy_match(home_name, all_bf_names)
    bf_away = fuzzy_match(away_name, all_bf_names)
    bf = {}
    if bf_home and bf_away:
        fk1 = f"{bf_home.lower()}|{bf_away.lower()}"
        fk2 = f"{bf_away.lower()}|{bf_home.lower()}"
        raw_bf = betfair_probs.get(fk1) or betfair_probs.get(fk2) or {}
        # Remap Betfair names back to OddsPapi names
        if raw_bf:
            bf = {
                home_name: raw_bf.get(bf_home, 0),
                away_name: raw_bf.get(bf_away, 0),
            }

    # OddsPapi odds
    bm_odds  = fetch_oddspapi_odds(fid, ODDSPAPI_KEY)
    h2h_list = get_h2h_odds(bm_odds)

    # Best odds per outcome
    best_home = (0, "")
    best_draw = (0, "")
    best_away = (0, "")
    for row in h2h_list:
        if row["home"] > best_home[0]:
            best_home = (row["home"], row["bookmaker"])
        if row["draw"] > best_draw[0]:
            best_draw = (row["draw"], row["bookmaker"])
        if row["away"] > best_away[0]:
            best_away = (row["away"], row["bookmaker"])

    home_prob = bf.get(home_name, 0)
    away_prob = bf.get(away_name, 0)
    draw_prob = max(0, 1 - home_prob - away_prob)

    match_summaries.append({
        "match":      match_name,
        "home":       home_name,
        "away":       away_name,
        "start":      start_fmt,
        "best_home":  best_home,
        "best_draw":  best_draw,
        "best_away":  best_away,
        "bf":         bf,
        "home_prob":  home_prob,
        "draw_prob":  draw_prob,
        "away_prob":  away_prob,
        "bookmakers": len(h2h_list),
    })

    # EV calculation
    if not bf or home_prob == 0:
        continue

    outcome_probs = {
        home_name: home_prob,
        "Draw":    draw_prob,
        away_name: away_prob,
    }

    for row in h2h_list:
        for outcome_label, odds_val, prob_key in [
            (home_name, row["home"], home_name),
            ("Draw",    row["draw"], "Draw"),
            (away_name, row["away"], away_name),
        ]:
            prob = outcome_probs.get(prob_key, 0)
            if prob <= 0:
                continue
            ev = (prob * odds_val) - 1
            if ev > 0:  # capture all positive EV; display filters applied later
                all_opportunities.append({
                    "match":     match_name,
                    "start":     start_fmt,
                    "outcome":   outcome_label,
                    "bookmaker": row["bookmaker"],
                    "odds":      odds_val,
                    "true_prob": prob,
                    "ev":        ev,
                })

all_opportunities.sort(key=lambda x: x["ev"], reverse=True)

# ── Top bar ────────────────────────────────────────────────────────────────────
now = datetime.utcnow().strftime("%d %b %Y  %H:%M UTC")
st.markdown(f"""
<div class="topbar">
    <div class="logo">EDGE<span>VIEW</span></div>
    <div class="timestamp">LIVE ● {now}</div>
</div>
""", unsafe_allow_html=True)

# ── Filters ────────────────────────────────────────────────────────────────────
f1, f2, f3, f4 = st.columns([2, 2, 1.5, 0.8])
with f1:
    sport_label = st.selectbox("Sport", list(SPORTS.keys()), label_visibility="collapsed")
    new_sport_cfg = SPORTS[sport_label]
    if new_sport_cfg["oddspapi_id"] != sport_cfg["oddspapi_id"]:
        sport_cfg = new_sport_cfg
        st.rerun()
    sport_cfg = new_sport_cfg
with f2:
    all_bookmakers = sorted(set(o["bookmaker"] for o in all_opportunities))
    selected_bookmakers = st.multiselect(
        "Bookmakers",
        options=all_bookmakers,
        default=[],
        placeholder="All bookmakers",
        label_visibility="collapsed",
    )
with f3:
    min_ev_pct = st.slider("Min EV", 0, 20, 0, label_visibility="collapsed")
    min_ev_filter = min_ev_pct / 100
with f4:
    st.write("")
    if st.button("↻ REFRESH"):
        st.cache_data.clear()
        st.rerun()

# ── Apply filters ──────────────────────────────────────────────────────────────
filtered = all_opportunities
if selected_bookmakers:
    filtered = [o for o in filtered if o["bookmaker"] in selected_bookmakers]
if min_ev_filter > 0:
    filtered = [o for o in filtered if o["ev"] >= min_ev_filter]

st.write("")

# ── Top 5 EV cards ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Best Bets Right Now</div>', unsafe_allow_html=True)

if not filtered:
    st.markdown("""
    <div style="padding:2rem; text-align:center; color:#5a5a7a;
         font-family:'JetBrains Mono',monospace; font-size:0.75rem;
         border:1px dashed #1e1e2e; border-radius:6px;">
        NO OPPORTUNITIES — try adjusting filters or refreshing
    </div>
    """, unsafe_allow_html=True)
else:
    for opp in filtered[:5]:
        ev_pct      = opp["ev"] * 100
        bar_width   = min(ev_pct * 4, 100)
        true_prob   = opp["true_prob"]
        bm_implied  = 1 / opp["odds"]  # raw implied, no margin removal
        edge        = true_prob - bm_implied

        st.markdown(f"""
        <div class="ev-card">
            <div class="ev-card-accent"></div>
            <div class="match-name">{opp['match']}</div>
            <div class="match-meta">{opp['start']}</div>
            <div class="card-row">
                <span class="outcome-label">{opp['outcome']}</span>
                <span class="bookie-tag">{opp['bookmaker']}</span>
                <span class="odds-value">{opp['odds']:.2f}</span>
                <span class="ev-badge">+{ev_pct:.1f}%</span>
            </div>
            <div class="prob-row">
                <div class="prob-item">
                    <div class="prob-label">Bookie Implied</div>
                    <div class="prob-value-dim">{bm_implied*100:.1f}%</div>
                </div>
                <div class="prob-arrow">→</div>
                <div class="prob-item">
                    <div class="prob-label">True Prob (Betfair)</div>
                    <div class="prob-value-green">{true_prob*100:.1f}%</div>
                </div>
                <div class="prob-item" style="margin-left:auto">
                    <div class="prob-label">Edge</div>
                    <div class="prob-value-green">+{edge*100:.1f}pp</div>
                </div>
            </div>
            <div class="ev-bar-wrap">
                <div class="ev-bar-fill" style="width:{bar_width}%"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.write("")

# ── Match search ───────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Match Search</div>', unsafe_allow_html=True)

query = st.text_input(
    "Search matches",
    placeholder="Type a team name...",
    label_visibility="collapsed",
)

if query.strip():
    suggestions = [m["match"] for m in match_summaries if query.lower() in m["match"].lower()]

    if not suggestions:
        st.markdown(f'<div style="color:#5a5a7a; font-family:JetBrains Mono,monospace; font-size:0.75rem; padding:0.5rem">No matches found for "{query}"</div>', unsafe_allow_html=True)
    else:
        selected_match = st.selectbox(
            "Select match",
            options=suggestions,
            label_visibility="collapsed",
        )

        m = next((x for x in match_summaries if x["match"] == selected_match), None)
        if m:
            h_o, h_b = m["best_home"]
            d_o, d_b = m["best_draw"]
            a_o, a_b = m["best_away"]

            def fmt(o, b):
                return (f"{o:.2f}", b) if o else ("—", "—")

            h_o, h_b = fmt(h_o, h_b)
            d_o, d_b = fmt(d_o, d_b)
            a_o, a_b = fmt(a_o, a_b)

            home_prob = m["home_prob"]
            draw_prob = m["draw_prob"]
            away_prob = m["away_prob"]

            # Betfair prob pills
            pills = ""
            if home_prob:
                pills += f'<span class="stat-pill stat-pill-green">{m["home"][:16]} {home_prob*100:.0f}%</span>'
            if draw_prob > 0.01:
                pills += f'<span class="stat-pill">Draw {draw_prob*100:.0f}%</span>'
            if away_prob:
                pills += f'<span class="stat-pill stat-pill-green">{m["away"][:16]} {away_prob*100:.0f}%</span>'
            if not pills:
                pills = '<span class="stat-pill">No Betfair prices available</span>'

            # EV opps for this match
            match_evs = [o for o in all_opportunities if o["match"] == selected_match]
            ev_rows = ""
            for o in match_evs[:5]:
                ev_rows += f"""
                <div class="match-ev-row">
                    <span class="outcome-label">{o["outcome"]}</span>
                    <span class="bookie-tag">{o["bookmaker"]}</span>
                    <span class="odds-value">{o["odds"]:.2f}</span>
                    <span class="ev-badge">+{o["ev"]*100:.1f}%</span>
                </div>"""

            st.markdown(f"""
            <div class="explorer-card">
                <div class="explorer-match-header">{m['match']}</div>
                <div class="explorer-meta">{m['start']} &nbsp;·&nbsp; {m['bookmakers']} bookmakers</div>
                <div class="odds-grid">
                    <div class="odds-cell">
                        <div class="odds-cell-label">Home</div>
                        <div class="odds-cell-value">{h_o}</div>
                        <div class="odds-cell-bookie">{h_b}</div>
                    </div>
                    <div class="odds-cell">
                        <div class="odds-cell-label">Draw</div>
                        <div class="odds-cell-value">{d_o}</div>
                        <div class="odds-cell-bookie">{d_b}</div>
                    </div>
                    <div class="odds-cell">
                        <div class="odds-cell-label">Away</div>
                        <div class="odds-cell-value">{a_o}</div>
                        <div class="odds-cell-bookie">{d_b}</div>
                    </div>
                </div>
                <div style="margin:0.5rem 0">{pills}</div>
                {f'<div style="margin-top:0.75rem"><div class="section-label" style="margin-bottom:0.4rem">EV Opportunities</div>{ev_rows}</div>' if ev_rows else ""}
            </div>
            """, unsafe_allow_html=True)