import streamlit as st
from datetime import datetime
import random

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="InsideEdge",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Styling ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #0a0a0f; color: #e8e8f0; }
.stApp { background-color: #0a0a0f; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1rem 1.5rem 2rem 1.5rem; max-width: 100%; }

.topbar { display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #1e1e2e; padding-bottom: 0.75rem; margin-bottom: 1.25rem; }
.logo { font-family: 'JetBrains Mono', monospace; font-size: 1.25rem; font-weight: 700; letter-spacing: 0.12em; color: #00e5a0; }
.logo span { color: #5a5a7a; }
.timestamp { font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: #5a5a7a; }
.demo-badge { font-family: 'JetBrains Mono', monospace; font-size: 0.6rem; background: rgba(255,200,0,0.1); color: #ffc800; border: 1px solid rgba(255,200,0,0.3); padding: 0.2rem 0.5rem; border-radius: 3px; letter-spacing: 0.1em; }

.section-label { font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; font-weight: 500; letter-spacing: 0.2em; color: #5a5a7a; text-transform: uppercase; margin-bottom: 0.75rem; border-left: 2px solid #00e5a0; padding-left: 0.5rem; }

.ev-card { background: #12121a; border: 1px solid #1e1e2e; border-radius: 6px; padding: 0.85rem 1rem; margin-bottom: 0.6rem; position: relative; overflow: hidden; }
.ev-card:hover { border-color: #2e2e4e; }
.ev-card-accent { position: absolute; top: 0; left: 0; height: 100%; background: linear-gradient(90deg, rgba(0,229,160,0.07), transparent); border-left: 3px solid #00e5a0; pointer-events: none; }
.match-name { font-size: 0.82rem; font-weight: 600; color: #e8e8f0; margin-bottom: 0.15rem; }
.match-meta { font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; color: #5a5a7a; margin-bottom: 0.55rem; }
.card-row { display: flex; align-items: center; justify-content: space-between; gap: 0.5rem; }
.outcome-label { font-size: 0.75rem; color: #9a9ab0; flex: 1; }
.bookie-tag { font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; background: #1e1e2e; color: #9a9ab0; padding: 0.15rem 0.4rem; border-radius: 3px; white-space: nowrap; }
.odds-value { font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; font-weight: 500; color: #e8e8f0; min-width: 2.5rem; text-align: right; }
.ev-badge { font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; font-weight: 700; color: #00e5a0; min-width: 3.5rem; text-align: right; }
.ev-bar-wrap { height: 3px; background: #1e1e2e; border-radius: 2px; margin-top: 0.55rem; overflow: hidden; }
.ev-bar-fill { height: 100%; border-radius: 2px; background: linear-gradient(90deg, #00e5a0, #00ffb3); }

.prob-row { display: flex; align-items: center; gap: 1rem; margin-top: 0.6rem; padding-top: 0.6rem; border-top: 1px solid #1e1e2e; }
.prob-item { display: flex; flex-direction: column; }
.prob-label { font-family: 'JetBrains Mono', monospace; font-size: 0.58rem; color: #5a5a7a; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.15rem; }
.prob-value-dim { font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; font-weight: 600; color: #5a5a7a; }
.prob-value-green { font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; font-weight: 700; color: #00e5a0; }
.prob-arrow { color: #2e2e4e; font-size: 1rem; margin-top: 0.75rem; }

.explorer-card { background: #12121a; border: 1px solid #1e1e2e; border-radius: 6px; padding: 1rem; margin-bottom: 0.6rem; }
.explorer-match-header { font-size: 0.9rem; font-weight: 600; color: #e8e8f0; margin-bottom: 0.2rem; }
.explorer-meta { font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; color: #5a5a7a; margin-bottom: 0.75rem; }
.odds-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 0.5rem; margin-bottom: 0.65rem; }
.odds-cell { background: #0a0a0f; border: 1px solid #1e1e2e; border-radius: 4px; padding: 0.5rem; text-align: center; }
.odds-cell-label { font-size: 0.6rem; color: #5a5a7a; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.2rem; }
.odds-cell-value { font-family: 'JetBrains Mono', monospace; font-size: 0.95rem; font-weight: 700; color: #00e5a0; }
.odds-cell-bookie { font-family: 'JetBrains Mono', monospace; font-size: 0.6rem; color: #5a5a7a; margin-top: 0.15rem; }

.stat-pill { display: inline-block; font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; background: #1e1e2e; color: #9a9ab0; padding: 0.2rem 0.5rem; border-radius: 3px; margin-right: 0.3rem; margin-bottom: 0.3rem; }
.stat-pill-green { background: rgba(0,229,160,0.12); color: #00e5a0; }

.match-ev-row { display: flex; align-items: center; gap: 0.5rem; padding: 0.35rem 0; border-bottom: 1px solid #1e1e2e; }
.match-ev-row:last-child { border-bottom: none; }

.player-card { background: #12121a; border: 1px solid #1e1e2e; border-radius: 6px; padding: 0.85rem 1rem; margin-bottom: 0.6rem; position: relative; overflow: hidden; }
.player-card-accent { position: absolute; top: 0; left: 0; height: 100%; background: linear-gradient(90deg, rgba(120,80,255,0.07), transparent); border-left: 3px solid #7850ff; pointer-events: none; }
.player-name { font-size: 0.85rem; font-weight: 600; color: #e8e8f0; margin-bottom: 0.05rem; }
.player-match { font-family: 'JetBrains Mono', monospace; font-size: 0.63rem; color: #5a5a7a; margin-bottom: 0.5rem; }
.player-market { font-size: 0.72rem; color: #9a9ab0; }
.player-line { font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #c8c8e0; font-weight: 500; }
.ev-badge-purple { font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; font-weight: 700; color: #7850ff; min-width: 3.5rem; text-align: right; }
.ev-bar-fill-purple { height: 100%; border-radius: 2px; background: linear-gradient(90deg, #7850ff, #a080ff); }

div[data-testid="stSelectbox"] > div > div { background: #12121a !important; border: 1px solid #1e1e2e !important; color: #e8e8f0 !important; font-family: 'JetBrains Mono', monospace !important; font-size: 0.8rem !important; }
div[data-testid="stSlider"] label { color: #5a5a7a !important; font-size: 0.75rem !important; }
div[data-testid="stMultiSelect"] > div > div { background: #12121a !important; border: 1px solid #1e1e2e !important; }
.stButton > button { background: #12121a !important; border: 1px solid #1e1e2e !important; color: #9a9ab0 !important; font-family: 'JetBrains Mono', monospace !important; font-size: 0.7rem !important; letter-spacing: 0.1em !important; border-radius: 4px !important; }
.stButton > button:hover { border-color: #00e5a0 !important; color: #00e5a0 !important; }
div[data-testid="stTextInput"] input { background: #12121a !important; border: 1px solid #1e1e2e !important; color: #e8e8f0 !important; font-family: 'JetBrains Mono', monospace !important; font-size: 0.8rem !important; }
div[data-testid="stMetric"] { background: #12121a; border: 1px solid #1e1e2e; border-radius: 6px; padding: 0.75rem 1rem; }
div[data-testid="stMetric"] label { font-family: 'JetBrains Mono', monospace !important; font-size: 0.65rem !important; color: #5a5a7a !important; text-transform: uppercase !important; letter-spacing: 0.1em !important; }
div[data-testid="stMetric"] div[data-testid="stMetricValue"] { font-family: 'JetBrains Mono', monospace !important; font-size: 1.4rem !important; color: #e8e8f0 !important; }
div[data-testid="stTabs"] button { font-family: 'JetBrains Mono', monospace !important; font-size: 0.72rem !important; color: #5a5a7a !important; }
div[data-testid="stTabs"] button[aria-selected="true"] { color: #00e5a0 !important; }
</style>
""", unsafe_allow_html=True)

# ── Dummy Data ─────────────────────────────────────────────────────────────────
BOOKMAKERS = ["bet365", "william hill", "betfair", "unibet", "paddy power",
              "draftkings", "fanduel", "betmgm", "bwin", "1xbet",
              "pinnacle", "betway", "ladbrokes", "coral", "888sport"]

MATCHES = [
    {"match": "Netherlands v Morocco",     "home": "Netherlands", "away": "Morocco",     "start": "30 Jun 02:00"},
    {"match": "Portugal v Uruguay",        "home": "Portugal",    "away": "Uruguay",     "start": "30 Jun 17:00"},
    {"match": "France v Argentina",        "home": "France",      "away": "Argentina",   "start": "30 Jun 21:00"},
    {"match": "England v USA",             "home": "England",     "away": "USA",         "start": "01 Jul 16:00"},
    {"match": "Spain v Germany",           "home": "Spain",       "away": "Germany",     "start": "01 Jul 20:00"},
    {"match": "Brazil v Japan",            "home": "Brazil",      "away": "Japan",       "start": "02 Jul 00:00"},
    {"match": "Belgium v Croatia",         "home": "Belgium",     "away": "Croatia",     "start": "02 Jul 19:00"},
    {"match": "Italy v Switzerland",       "home": "Italy",       "away": "Switzerland", "start": "02 Jul 23:00"},
    {"match": "Australia v South Korea",   "home": "Australia",   "away": "South Korea", "start": "03 Jul 03:00"},
    {"match": "Denmark v Mexico",          "home": "Denmark",     "away": "Mexico",      "start": "03 Jul 18:00"},
]

BASE_PROBS = {
    "Netherlands v Morocco":   (0.52, 0.26, 0.22),
    "Portugal v Uruguay":      (0.48, 0.27, 0.25),
    "France v Argentina":      (0.38, 0.28, 0.34),
    "England v USA":           (0.44, 0.29, 0.27),
    "Spain v Germany":         (0.41, 0.27, 0.32),
    "Brazil v Japan":          (0.61, 0.22, 0.17),
    "Belgium v Croatia":       (0.43, 0.28, 0.29),
    "Italy v Switzerland":     (0.45, 0.28, 0.27),
    "Australia v South Korea": (0.36, 0.30, 0.34),
    "Denmark v Mexico":        (0.40, 0.29, 0.31),
}

# Player pool per match with realistic per-90 stats
PLAYER_POOL = {
    "Netherlands v Morocco": [
        {"name": "V. van Dijk",      "team": "Netherlands", "shots_p90": 1.1, "sot_p90": 0.5, "fouls_p90": 0.8},
        {"name": "C. Gakpo",         "team": "Netherlands", "shots_p90": 2.8, "sot_p90": 1.2, "fouls_p90": 0.6},
        {"name": "X. Simons",        "team": "Netherlands", "shots_p90": 1.9, "sot_p90": 0.9, "fouls_p90": 1.1},
        {"name": "H. Ziyech",        "team": "Morocco",     "shots_p90": 2.1, "sot_p90": 0.8, "fouls_p90": 1.3},
        {"name": "A. Hakimi",        "team": "Morocco",     "shots_p90": 1.4, "sot_p90": 0.6, "fouls_p90": 1.8},
    ],
    "Portugal v Uruguay": [
        {"name": "C. Ronaldo",       "team": "Portugal",    "shots_p90": 4.2, "sot_p90": 1.8, "fouls_p90": 0.9},
        {"name": "B. Fernandes",     "team": "Portugal",    "shots_p90": 2.6, "sot_p90": 1.1, "fouls_p90": 1.4},
        {"name": "R. Leão",          "team": "Portugal",    "shots_p90": 2.9, "sot_p90": 1.3, "fouls_p90": 0.7},
        {"name": "D. Núñez",         "team": "Uruguay",     "shots_p90": 3.1, "sot_p90": 1.4, "fouls_p90": 1.1},
        {"name": "F. Valverde",      "team": "Uruguay",     "shots_p90": 1.8, "sot_p90": 0.7, "fouls_p90": 2.1},
    ],
    "France v Argentina": [
        {"name": "K. Mbappé",        "team": "France",      "shots_p90": 4.8, "sot_p90": 2.1, "fouls_p90": 0.8},
        {"name": "A. Griezmann",     "team": "France",      "shots_p90": 2.4, "sot_p90": 1.0, "fouls_p90": 1.2},
        {"name": "O. Giroud",        "team": "France",      "shots_p90": 2.9, "sot_p90": 1.3, "fouls_p90": 1.5},
        {"name": "L. Messi",         "team": "Argentina",   "shots_p90": 3.6, "sot_p90": 1.6, "fouls_p90": 2.2},
        {"name": "J. Álvarez",       "team": "Argentina",   "shots_p90": 2.7, "sot_p90": 1.2, "fouls_p90": 1.0},
        {"name": "Á. Di María",      "team": "Argentina",   "shots_p90": 2.2, "sot_p90": 0.9, "fouls_p90": 1.6},
    ],
    "England v USA": [
        {"name": "H. Kane",          "team": "England",     "shots_p90": 4.1, "sot_p90": 1.9, "fouls_p90": 1.1},
        {"name": "J. Bellingham",    "team": "England",     "shots_p90": 2.3, "sot_p90": 1.0, "fouls_p90": 1.4},
        {"name": "B. Saka",          "team": "England",     "shots_p90": 2.8, "sot_p90": 1.2, "fouls_p90": 0.9},
        {"name": "C. Pulisic",       "team": "USA",         "shots_p90": 2.5, "sot_p90": 1.1, "fouls_p90": 1.3},
        {"name": "T. Weah",          "team": "USA",         "shots_p90": 1.9, "sot_p90": 0.8, "fouls_p90": 1.7},
    ],
    "Spain v Germany": [
        {"name": "A. Morata",        "team": "Spain",       "shots_p90": 3.0, "sot_p90": 1.3, "fouls_p90": 1.2},
        {"name": "P. Gavi",          "team": "Spain",       "shots_p90": 1.2, "sot_p90": 0.5, "fouls_p90": 2.8},
        {"name": "R. Yamal",         "team": "Spain",       "shots_p90": 2.6, "sot_p90": 1.1, "fouls_p90": 0.8},
        {"name": "K. Havertz",       "team": "Germany",     "shots_p90": 2.4, "sot_p90": 1.0, "fouls_p90": 1.1},
        {"name": "J. Musiala",       "team": "Germany",     "shots_p90": 2.9, "sot_p90": 1.3, "fouls_p90": 0.9},
        {"name": "T. Müller",        "team": "Germany",     "shots_p90": 1.8, "sot_p90": 0.8, "fouls_p90": 1.0},
    ],
    "Brazil v Japan": [
        {"name": "Vinicius Jr.",      "team": "Brazil",      "shots_p90": 4.3, "sot_p90": 1.9, "fouls_p90": 2.4},
        {"name": "Neymar",           "team": "Brazil",      "shots_p90": 3.8, "sot_p90": 1.7, "fouls_p90": 3.1},
        {"name": "Rodrygo",          "team": "Brazil",      "shots_p90": 2.6, "sot_p90": 1.1, "fouls_p90": 1.3},
        {"name": "D. Kamada",        "team": "Japan",       "shots_p90": 1.7, "sot_p90": 0.7, "fouls_p90": 1.4},
        {"name": "H. Ito",           "team": "Japan",       "shots_p90": 1.4, "sot_p90": 0.6, "fouls_p90": 1.9},
    ],
    "Belgium v Croatia": [
        {"name": "R. Lukaku",        "team": "Belgium",     "shots_p90": 3.5, "sot_p90": 1.6, "fouls_p90": 1.3},
        {"name": "K. De Bruyne",     "team": "Belgium",     "shots_p90": 2.1, "sot_p90": 0.9, "fouls_p90": 1.0},
        {"name": "L. Trossard",      "team": "Belgium",     "shots_p90": 2.4, "sot_p90": 1.0, "fouls_p90": 0.8},
        {"name": "L. Modrić",        "team": "Croatia",     "shots_p90": 1.6, "sot_p90": 0.7, "fouls_p90": 1.5},
        {"name": "A. Kramarić",      "team": "Croatia",     "shots_p90": 2.8, "sot_p90": 1.2, "fouls_p90": 1.1},
    ],
    "Italy v Switzerland": [
        {"name": "G. Scamacca",      "team": "Italy",       "shots_p90": 3.1, "sot_p90": 1.4, "fouls_p90": 1.2},
        {"name": "F. Chiesa",        "team": "Italy",       "shots_p90": 2.7, "sot_p90": 1.2, "fouls_p90": 1.6},
        {"name": "N. Barella",       "team": "Italy",       "shots_p90": 1.5, "sot_p90": 0.6, "fouls_p90": 2.1},
        {"name": "X. Shaqiri",       "team": "Switzerland", "shots_p90": 2.3, "sot_p90": 1.0, "fouls_p90": 1.4},
        {"name": "B. Embolo",        "team": "Switzerland", "shots_p90": 2.6, "sot_p90": 1.1, "fouls_p90": 1.3},
    ],
    "Australia v South Korea": [
        {"name": "M. Leckie",        "team": "Australia",   "shots_p90": 1.8, "sot_p90": 0.8, "fouls_p90": 1.4},
        {"name": "M. Duke",          "team": "Australia",   "shots_p90": 2.2, "sot_p90": 1.0, "fouls_p90": 1.6},
        {"name": "Son Heung-min",    "team": "South Korea", "shots_p90": 3.4, "sot_p90": 1.5, "fouls_p90": 1.1},
        {"name": "H. Lee",           "team": "South Korea", "shots_p90": 1.9, "sot_p90": 0.8, "fouls_p90": 2.0},
    ],
    "Denmark v Mexico": [
        {"name": "E. Haaland",       "team": "Denmark",     "shots_p90": 4.6, "sot_p90": 2.0, "fouls_p90": 1.0},
        {"name": "C. Eriksen",       "team": "Denmark",     "shots_p90": 1.7, "sot_p90": 0.7, "fouls_p90": 0.9},
        {"name": "H. Lozano",        "team": "Mexico",      "shots_p90": 2.4, "sot_p90": 1.0, "fouls_p90": 1.8},
        {"name": "R. Jiménez",       "team": "Mexico",      "shots_p90": 2.9, "sot_p90": 1.3, "fouls_p90": 1.4},
    ],
}

PROP_MARKETS = [
    {"key": "shots",   "label": "Shots",           "lines": [1.5, 2.5, 3.5], "stat": "shots_p90"},
    {"key": "sot",     "label": "Shots on Target",  "lines": [0.5, 1.5, 2.5], "stat": "sot_p90"},
    {"key": "fouls",   "label": "Fouls Committed",  "lines": [0.5, 1.5, 2.5], "stat": "fouls_p90"},
]

def poisson_over(lam, line):
    """P(X > line) using Poisson with mean lam."""
    import math
    k = int(line + 0.5)
    prob_under = sum(
        (lam**i * math.exp(-lam)) / math.factorial(i) for i in range(k + 1)
    )
    return max(0.01, min(0.99, 1 - prob_under))

def make_match_opportunities():
    random.seed(42)
    opps = []
    for m in MATCHES:
        hp, dp, ap = BASE_PROBS[m["match"]]
        outcomes = [(m["home"], hp), ("Draw", dp), (m["away"], ap)]
        for outcome_label, true_prob in outcomes:
            for bm in random.sample(BOOKMAKERS, 6):
                noise = random.uniform(-0.04, 0.07)
                implied = max(true_prob + noise, 0.05)
                odds = round(1 / implied * random.uniform(0.96, 1.0), 2)
                ev = (true_prob * odds) - 1
                if ev > 0.005:
                    opps.append({
                        "match": m["match"], "start": m["start"],
                        "home": m["home"], "away": m["away"],
                        "outcome": outcome_label, "bookmaker": bm,
                        "odds": odds, "true_prob": true_prob, "ev": ev,
                        "type": "match",
                    })
    return sorted(opps, key=lambda x: x["ev"], reverse=True)

def make_player_opportunities():
    random.seed(99)
    opps = []
    for match_name, players in PLAYER_POOL.items():
        match = next(m for m in MATCHES if m["match"] == match_name)
        for player in players:
            for market in PROP_MARKETS:
                stat_p90 = player[market["stat"]]
                lam = stat_p90  # expected value over 90 mins
                for line in market["lines"]:
                    true_prob = poisson_over(lam, line)
                    for bm in random.sample(BOOKMAKERS, 4):
                        noise = random.uniform(-0.05, 0.08)
                        bm_prob = max(true_prob - noise, 0.05)
                        odds = round(1 / bm_prob * random.uniform(0.93, 0.98), 2)
                        ev = (true_prob * odds) - 1
                        if ev > 0.01:
                            opps.append({
                                "player":    player["name"],
                                "team":      player["team"],
                                "match":     match_name,
                                "start":     match["start"],
                                "market":    market["label"],
                                "line":      line,
                                "direction": "Over",
                                "bookmaker": bm,
                                "odds":      odds,
                                "true_prob": true_prob,
                                "ev":        ev,
                                "type":      "player",
                            })
    return sorted(opps, key=lambda x: x["ev"], reverse=True)

def make_match_summaries():
    random.seed(42)
    summaries = []
    for m in MATCHES:
        hp, dp, ap = BASE_PROBS[m["match"]]
        summaries.append({
            "match": m["match"], "home": m["home"], "away": m["away"], "start": m["start"],
            "best_home": (round(1/hp * random.uniform(0.97, 1.01), 2), random.choice(BOOKMAKERS)),
            "best_draw": (round(1/dp * random.uniform(0.97, 1.01), 2), random.choice(BOOKMAKERS)),
            "best_away": (round(1/ap * random.uniform(0.97, 1.01), 2), random.choice(BOOKMAKERS)),
            "home_prob": hp, "draw_prob": dp, "away_prob": ap,
            "bookmakers": random.randint(80, 146),
        })
    return summaries

match_opps   = make_match_opportunities()
player_opps  = make_player_opportunities()
match_sums   = make_match_summaries()
all_opps     = match_opps + player_opps

# ── Top bar ────────────────────────────────────────────────────────────────────
now = datetime.utcnow().strftime("%d %b %Y  %H:%M UTC")
st.markdown(f"""
<div class="topbar">
    <div style="display:flex; align-items:center; gap:1rem;">
        <div class="logo">INSIDE<span>EDGE</span></div>
        <div class="demo-badge">DEMO MODE</div>
    </div>
    <div class="timestamp">LIVE ● {now}</div>
</div>
""", unsafe_allow_html=True)

# ── Tabs ───────────────────────────────────────────────────────────────────────
tab_match, tab_player = st.tabs(["⚽  Match Markets", "👤  Player Props"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — MATCH MARKETS
# ══════════════════════════════════════════════════════════════════════════════
with tab_match:

    # Filters
    f1, f2, f3 = st.columns([2, 2, 1.5])
    with f1:
        st.selectbox("Sport", ["⚽ World Cup", "⚽ Premier League", "⚽ Champions League"], label_visibility="collapsed")
    with f2:
        all_bm = sorted(set(o["bookmaker"] for o in match_opps))
        sel_bm = st.multiselect("Bookmakers", options=all_bm, default=[], placeholder="All bookmakers", label_visibility="collapsed")
    with f3:
        min_ev_pct = st.slider("Min EV", 0, 20, 0, label_visibility="collapsed", key="match_ev")
        min_ev = min_ev_pct / 100

    filtered = match_opps
    if sel_bm:
        filtered = [o for o in filtered if o["bookmaker"] in sel_bm]
    if min_ev > 0:
        filtered = [o for o in filtered if o["ev"] >= min_ev]

    st.write("")

    # Metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.metric("Fixtures", len(MATCHES))
    with m2: st.metric("EV Opportunities", len(filtered))
    with m3: st.metric("Best EV", f"+{filtered[0]['ev']*100:.1f}%" if filtered else "—")
    with m4: st.metric("Bookmakers", len(set(o["bookmaker"] for o in filtered)) if filtered else 0)

    st.write("")

    # Top 5
    st.markdown('<div class="section-label">Best Bets Right Now</div>', unsafe_allow_html=True)
    if not filtered:
        st.markdown('<div style="padding:2rem;text-align:center;color:#5a5a7a;font-family:JetBrains Mono,monospace;font-size:0.75rem;border:1px dashed #1e1e2e;border-radius:6px;">NO OPPORTUNITIES — try adjusting filters</div>', unsafe_allow_html=True)
    else:
        for opp in filtered[:5]:
            ev_pct    = opp["ev"] * 100
            bar_width = min(ev_pct * 5, 100)
            true_prob = opp["true_prob"]
            bm_imp    = 1 / opp["odds"]
            edge      = true_prob - bm_imp
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
                    <div class="prob-item"><div class="prob-label">Bookie Implied</div><div class="prob-value-dim">{bm_imp*100:.1f}%</div></div>
                    <div class="prob-arrow">→</div>
                    <div class="prob-item"><div class="prob-label">True Prob (Betfair)</div><div class="prob-value-green">{true_prob*100:.1f}%</div></div>
                    <div class="prob-item" style="margin-left:auto"><div class="prob-label">Edge</div><div class="prob-value-green">+{edge*100:.1f}pp</div></div>
                </div>
                <div class="ev-bar-wrap"><div class="ev-bar-fill" style="width:{bar_width}%"></div></div>
            </div>
            """, unsafe_allow_html=True)

    st.write("")

    # Match search
    st.markdown('<div class="section-label">Match Search</div>', unsafe_allow_html=True)
    query = st.text_input("Search", placeholder="Type a team name — e.g. France, Brazil, England...", label_visibility="collapsed", key="match_search")

    if query.strip():
        suggestions = [m["match"] for m in match_sums if query.lower() in m["match"].lower()]
        if not suggestions:
            st.markdown(f'<div style="color:#5a5a7a;font-family:JetBrains Mono,monospace;font-size:0.75rem;padding:0.5rem 0">No matches found for "{query}"</div>', unsafe_allow_html=True)
        else:
            sel = st.selectbox("Select", options=suggestions, label_visibility="collapsed", key="match_select")
            m = next((x for x in match_sums if x["match"] == sel), None)
            if m:
                h_o, h_b = m["best_home"]
                d_o, d_b = m["best_draw"]
                a_o, a_b = m["best_away"]
                pills = (
                    f'<span class="stat-pill stat-pill-green">{m["home"]} {m["home_prob"]*100:.0f}%</span>'
                    f'<span class="stat-pill">Draw {m["draw_prob"]*100:.0f}%</span>'
                    f'<span class="stat-pill stat-pill-green">{m["away"]} {m["away_prob"]*100:.0f}%</span>'
                )
                match_evs = [o for o in match_opps if o["match"] == sel]
                ev_rows = "".join(f'<div class="match-ev-row"><span class="outcome-label">{o["outcome"]}</span><span class="bookie-tag">{o["bookmaker"]}</span><span class="odds-value">{o["odds"]:.2f}</span><span class="ev-badge">+{o["ev"]*100:.1f}%</span></div>' for o in match_evs[:6])
                ev_sec = f'<div style="margin-top:0.75rem"><div class="section-label" style="margin-bottom:0.4rem">EV Opportunities</div>{ev_rows}</div>' if ev_rows else ""
                st.markdown(f"""
                <div class="explorer-card">
                    <div class="explorer-match-header">{m['match']}</div>
                    <div class="explorer-meta">{m['start']} &nbsp;·&nbsp; {m['bookmakers']} bookmakers</div>
                    <div class="odds-grid">
                        <div class="odds-cell"><div class="odds-cell-label">Home</div><div class="odds-cell-value">{h_o:.2f}</div><div class="odds-cell-bookie">{h_b}</div></div>
                        <div class="odds-cell"><div class="odds-cell-label">Draw</div><div class="odds-cell-value">{d_o:.2f}</div><div class="odds-cell-bookie">{d_b}</div></div>
                        <div class="odds-cell"><div class="odds-cell-label">Away</div><div class="odds-cell-value">{a_o:.2f}</div><div class="odds-cell-bookie">{a_b}</div></div>
                    </div>
                    <div>{pills}</div>
                    {ev_sec}
                </div>
                """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — PLAYER PROPS
# ══════════════════════════════════════════════════════════════════════════════
with tab_player:

    # Filters
    p1, p2, p3 = st.columns([2, 2, 1.5])
    with p1:
        market_options = ["All Markets", "Shots", "Shots on Target", "Fouls Committed"]
        sel_market = st.selectbox("Market", market_options, label_visibility="collapsed", key="prop_market")
    with p2:
        prop_bm = sorted(set(o["bookmaker"] for o in player_opps))
        sel_prop_bm = st.multiselect("Bookmakers", options=prop_bm, default=[], placeholder="All bookmakers", label_visibility="collapsed", key="prop_bm")
    with p3:
        min_prop_ev_pct = st.slider("Min EV", 0, 20, 0, label_visibility="collapsed", key="prop_ev")
        min_prop_ev = min_prop_ev_pct / 100

    filtered_props = player_opps
    if sel_market != "All Markets":
        filtered_props = [o for o in filtered_props if o["market"] == sel_market]
    if sel_prop_bm:
        filtered_props = [o for o in filtered_props if o["bookmaker"] in sel_prop_bm]
    if min_prop_ev > 0:
        filtered_props = [o for o in filtered_props if o["ev"] >= min_prop_ev]

    st.write("")

    # Metrics
    p_m1, p_m2, p_m3, p_m4 = st.columns(4)
    with p_m1: st.metric("Players Tracked", sum(len(v) for v in PLAYER_POOL.values()))
    with p_m2: st.metric("EV Opportunities", len(filtered_props))
    with p_m3: st.metric("Best EV", f"+{filtered_props[0]['ev']*100:.1f}%" if filtered_props else "—")
    with p_m4: st.metric("Markets", len(set(o["market"] for o in filtered_props)))

    st.write("")

    # Top 5 player props
    st.markdown('<div class="section-label">Best Player Prop Bets</div>', unsafe_allow_html=True)

    if not filtered_props:
        st.markdown('<div style="padding:2rem;text-align:center;color:#5a5a7a;font-family:JetBrains Mono,monospace;font-size:0.75rem;border:1px dashed #1e1e2e;border-radius:6px;">NO OPPORTUNITIES — try adjusting filters</div>', unsafe_allow_html=True)
    else:
        for opp in filtered_props[:5]:
            ev_pct    = opp["ev"] * 100
            bar_width = min(ev_pct * 5, 100)
            true_prob = opp["true_prob"]
            bm_imp    = 1 / opp["odds"]
            edge      = true_prob - bm_imp
            st.markdown(f"""
            <div class="player-card">
                <div class="player-card-accent"></div>
                <div class="player-name">{opp['player']} <span style="color:#5a5a7a;font-size:0.72rem;font-weight:400">· {opp['team']}</span></div>
                <div class="player-match">{opp['match']} · {opp['start']}</div>
                <div class="card-row">
                    <span class="player-market">{opp['direction']} {opp['line']} {opp['market']}</span>
                    <span class="bookie-tag">{opp['bookmaker']}</span>
                    <span class="odds-value">{opp['odds']:.2f}</span>
                    <span class="ev-badge-purple">+{ev_pct:.1f}%</span>
                </div>
                <div class="prob-row">
                    <div class="prob-item"><div class="prob-label">Bookie Implied</div><div class="prob-value-dim">{bm_imp*100:.1f}%</div></div>
                    <div class="prob-arrow">→</div>
                    <div class="prob-item"><div class="prob-label">True Prob (Poisson)</div><div class="prob-value-green">{true_prob*100:.1f}%</div></div>
                    <div class="prob-item" style="margin-left:auto"><div class="prob-label">Edge</div><div class="prob-value-green">+{edge*100:.1f}pp</div></div>
                </div>
                <div class="ev-bar-wrap"><div class="ev-bar-fill-purple" style="width:{bar_width}%"></div></div>
            </div>
            """, unsafe_allow_html=True)

    st.write("")

    # Player search
    st.markdown('<div class="section-label">Player Search</div>', unsafe_allow_html=True)
    player_query = st.text_input("Search player", placeholder="Type a player name — e.g. Mbappé, Kane, Messi...", label_visibility="collapsed", key="player_search")

    if player_query.strip():
        all_players = [p for players in PLAYER_POOL.values() for p in players]
        matched = [p for p in all_players if player_query.lower() in p["name"].lower()]

        if not matched:
            st.markdown(f'<div style="color:#5a5a7a;font-family:JetBrains Mono,monospace;font-size:0.75rem;padding:0.5rem 0">No players found for "{player_query}"</div>', unsafe_allow_html=True)
        else:
            player_names = list(dict.fromkeys(p["name"] for p in matched))
            sel_player = st.selectbox("Select player", options=player_names, label_visibility="collapsed", key="player_select")

            player = next((p for players in PLAYER_POOL.values() for p in players if p["name"] == sel_player), None)
            match_name = next((mn for mn, players in PLAYER_POOL.items() for p in players if p["name"] == sel_player), None)
            match = next((m for m in MATCHES if m["match"] == match_name), None)

            if player and match:
                player_ev = [o for o in player_opps if o["player"] == sel_player]

                stat_rows = ""
                for market in PROP_MARKETS:
                    lam = player[market["stat"]]
                    for line in market["lines"]:
                        prob = poisson_over(lam, line)
                        fair_odds = round(1 / prob, 2)
                        stat_rows += f"""
                        <div class="match-ev-row">
                            <span class="outcome-label">Over {line} {market['label']}</span>
                            <span class="bookie-tag">Fair odds</span>
                            <span class="odds-value">{fair_odds:.2f}</span>
                            <span style="font-family:JetBrains Mono,monospace;font-size:0.72rem;color:#9a9ab0">{prob*100:.0f}%</span>
                        </div>"""

                ev_rows_p = "".join(
                    f'<div class="match-ev-row"><span class="outcome-label">{o["direction"]} {o["line"]} {o["market"]}</span><span class="bookie-tag">{o["bookmaker"]}</span><span class="odds-value">{o["odds"]:.2f}</span><span class="ev-badge-purple">+{o["ev"]*100:.1f}%</span></div>'
                    for o in player_ev[:8]
                )

                st.markdown(f"""
                <div class="explorer-card">
                    <div class="explorer-match-header">{sel_player} <span style="color:#5a5a7a;font-weight:400;font-size:0.8rem">· {player['team']}</span></div>
                    <div class="explorer-meta">{match['match']} · {match['start']}</div>
                    <div style="margin-bottom:0.75rem">
                        <span class="stat-pill">Shots/90: {player['shots_p90']}</span>
                        <span class="stat-pill">SoT/90: {player['sot_p90']}</span>
                        <span class="stat-pill">Fouls/90: {player['fouls_p90']}</span>
                    </div>
                    <div class="section-label" style="margin-bottom:0.4rem">Fair Odds (Poisson Model)</div>
                    {stat_rows}
                    {f'<div style="margin-top:0.75rem"><div class="section-label" style="margin-bottom:0.4rem">EV Opportunities</div>{ev_rows_p}</div>' if ev_rows_p else ""}
                </div>
                """, unsafe_allow_html=True)