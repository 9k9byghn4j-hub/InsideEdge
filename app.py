import streamlit as st
from datetime import datetime
import random
import math

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

/* ── Topbar ── */
.topbar { display:flex; align-items:center; justify-content:space-between; border-bottom:1px solid #1e1e2e; padding-bottom:0.75rem; margin-bottom:1.25rem; }
.logo { font-family:'JetBrains Mono',monospace; font-size:1.25rem; font-weight:700; letter-spacing:0.12em; color:#00e5a0; }
.logo span { color:#5a5a7a; }
.timestamp { font-family:'JetBrains Mono',monospace; font-size:0.7rem; color:#5a5a7a; }
.demo-badge { font-family:'JetBrains Mono',monospace; font-size:0.6rem; background:rgba(255,200,0,0.1); color:#ffc800; border:1px solid rgba(255,200,0,0.3); padding:0.2rem 0.5rem; border-radius:3px; }

/* ── Fixture list ── */
.fixture-row {
    display:flex; align-items:center; justify-content:space-between;
    background:#12121a; border:1px solid #1e1e2e; border-radius:6px;
    padding:0.75rem 1rem; margin-bottom:0.5rem; cursor:pointer;
    transition: border-color 0.15s;
}
.fixture-row:hover { border-color:#00e5a0; }
.fixture-time { font-family:'JetBrains Mono',monospace; font-size:0.65rem; color:#5a5a7a; min-width:4.5rem; }
.fixture-teams { font-size:0.85rem; font-weight:600; color:#e8e8f0; flex:1; padding:0 1rem; }
.fixture-comp { font-family:'JetBrains Mono',monospace; font-size:0.62rem; color:#5a5a7a; }
.ev-dot { width:8px; height:8px; border-radius:50%; background:#00e5a0; box-shadow:0 0 6px #00e5a0; margin-left:0.75rem; }
.ev-dot-none { width:8px; height:8px; border-radius:50%; background:#1e1e2e; margin-left:0.75rem; }

/* ── Match header ── */
.match-header {
    background:linear-gradient(135deg, #12121a, #0f0f1a);
    border:1px solid #1e1e2e; border-radius:8px;
    padding:1.25rem 1.5rem; margin-bottom:1.25rem;
}
.match-header-comp { font-family:'JetBrains Mono',monospace; font-size:0.62rem; color:#5a5a7a; letter-spacing:0.15em; text-transform:uppercase; margin-bottom:0.5rem; }
.match-header-teams { font-size:1.4rem; font-weight:700; color:#e8e8f0; margin-bottom:0.35rem; }
.match-header-time { font-family:'JetBrains Mono',monospace; font-size:0.72rem; color:#5a5a7a; }

/* ── Market table ── */
.market-table { background:#12121a; border:1px solid #1e1e2e; border-radius:6px; overflow:hidden; margin-bottom:1rem; }
.market-table-header { padding:0.6rem 1rem; background:#0a0a0f; border-bottom:1px solid #1e1e2e; font-family:'JetBrains Mono',monospace; font-size:0.65rem; color:#5a5a7a; letter-spacing:0.15em; text-transform:uppercase; }
.market-row { display:flex; align-items:center; padding:0.65rem 1rem; border-bottom:1px solid #1e1e2e; gap:0.75rem; }
.market-row:last-child { border-bottom:none; }
.market-row:hover { background:#1a1a26; }
.outcome-name { flex:1; font-size:0.82rem; color:#c8c8e0; }

/* ── Odds cell with hover tooltip ── */
.odds-wrap { position:relative; display:inline-block; }
.odds-btn {
    display:flex; align-items:center; gap:0.4rem;
    background:#1a1a2e; border:1px solid #2e2e4e;
    border-radius:5px; padding:0.4rem 0.65rem;
    cursor:pointer; transition:border-color 0.15s, background 0.15s;
    min-width:5.5rem;
}
.odds-btn:hover { border-color:#00e5a0; background:#1e1e38; }
.odds-btn-price { font-family:'JetBrains Mono',monospace; font-size:0.85rem; font-weight:700; color:#00e5a0; }
.odds-btn-bookie { font-family:'JetBrains Mono',monospace; font-size:0.58rem; color:#5a5a7a; }
.odds-tooltip {
    display:none; position:absolute; top:calc(100% + 6px); left:0;
    background:#0f0f1a; border:1px solid #2e2e4e; border-radius:6px;
    padding:0.5rem; min-width:180px; z-index:999;
    box-shadow:0 8px 24px rgba(0,0,0,0.6);
}
.odds-wrap:hover .odds-tooltip { display:block; }
.tooltip-row { display:flex; align-items:center; justify-content:space-between; gap:0.5rem; padding:0.25rem 0.35rem; border-radius:3px; }
.tooltip-row:hover { background:#1e1e2e; }
.tooltip-bookie { font-family:'JetBrains Mono',monospace; font-size:0.68rem; color:#9a9ab0; flex:1; }
.tooltip-price { font-family:'JetBrains Mono',monospace; font-size:0.75rem; font-weight:600; color:#e8e8f0; }
.tooltip-price-best { color:#00e5a0; }
.tooltip-divider { border:none; border-top:1px solid #1e1e2e; margin:0.3rem 0; }

/* ── EV pill ── */
.ev-pill { font-family:'JetBrains Mono',monospace; font-size:0.65rem; font-weight:700; padding:0.2rem 0.45rem; border-radius:3px; white-space:nowrap; }
.ev-pill-pos { background:rgba(0,229,160,0.12); color:#00e5a0; border:1px solid rgba(0,229,160,0.2); }
.ev-pill-neg { background:rgba(255,77,109,0.08); color:#5a5a7a; border:1px solid #1e1e2e; }

/* ── True prob ── */
.true-prob { font-family:'JetBrains Mono',monospace; font-size:0.72rem; color:#5a5a7a; min-width:3rem; text-align:right; }

/* ── Player card ── */
.player-section { margin-bottom:0.5rem; }
.player-row { display:flex; align-items:center; padding:0.6rem 1rem; border-bottom:1px solid #1e1e2e; gap:0.75rem; }
.player-row:last-child { border-bottom:none; }
.player-info { flex:1.5; }
.player-info-name { font-size:0.82rem; font-weight:600; color:#e8e8f0; }
.player-info-team { font-family:'JetBrains Mono',monospace; font-size:0.62rem; color:#5a5a7a; }
.player-stat { font-family:'JetBrains Mono',monospace; font-size:0.68rem; color:#5a5a7a; min-width:4rem; }

/* ── Section label ── */
.section-label { font-family:'JetBrains Mono',monospace; font-size:0.65rem; font-weight:500; letter-spacing:0.2em; color:#5a5a7a; text-transform:uppercase; margin-bottom:0.75rem; border-left:2px solid #00e5a0; padding-left:0.5rem; }

/* ── Back button ── */
.back-btn { font-family:'JetBrains Mono',monospace; font-size:0.7rem; color:#5a5a7a; cursor:pointer; margin-bottom:1rem; display:inline-block; }
.back-btn:hover { color:#00e5a0; }

/* ── Bookie badge ── */
.bookie-badge { font-family:'JetBrains Mono',monospace; font-size:0.6rem; background:#1e1e2e; color:#9a9ab0; padding:0.1rem 0.35rem; border-radius:3px; }

/* Streamlit overrides */
div[data-testid="stSelectbox"] > div > div { background:#12121a !important; border:1px solid #1e1e2e !important; color:#e8e8f0 !important; font-family:'JetBrains Mono',monospace !important; }
.stButton > button { background:#12121a !important; border:1px solid #1e1e2e !important; color:#9a9ab0 !important; font-family:'JetBrains Mono',monospace !important; font-size:0.7rem !important; border-radius:4px !important; }
.stButton > button:hover { border-color:#00e5a0 !important; color:#00e5a0 !important; }
div[data-testid="stTabs"] button { font-family:'JetBrains Mono',monospace !important; font-size:0.72rem !important; color:#5a5a7a !important; }
div[data-testid="stTabs"] button[aria-selected="true"] { color:#00e5a0 !important; }
</style>
""", unsafe_allow_html=True)

# ── Data ───────────────────────────────────────────────────────────────────────
BOOKMAKERS = [
    "bet365", "william hill", "betfair", "unibet", "paddy power",
    "draftkings", "fanduel", "betmgm", "bwin", "1xbet",
    "pinnacle", "betway", "ladbrokes", "coral", "888sport",
]

MATCHES = [
    {"match": "Netherlands v Morocco",     "home": "Netherlands", "away": "Morocco",     "start": "30 Jun 02:00", "comp": "FIFA WORLD CUP 2026"},
    {"match": "Portugal v Uruguay",        "home": "Portugal",    "away": "Uruguay",     "start": "30 Jun 17:00", "comp": "FIFA WORLD CUP 2026"},
    {"match": "France v Argentina",        "home": "France",      "away": "Argentina",   "start": "30 Jun 21:00", "comp": "FIFA WORLD CUP 2026"},
    {"match": "England v USA",             "home": "England",     "away": "USA",         "start": "01 Jul 16:00", "comp": "FIFA WORLD CUP 2026"},
    {"match": "Spain v Germany",           "home": "Spain",       "away": "Germany",     "start": "01 Jul 20:00", "comp": "FIFA WORLD CUP 2026"},
    {"match": "Brazil v Japan",            "home": "Brazil",      "away": "Japan",       "start": "02 Jul 00:00", "comp": "FIFA WORLD CUP 2026"},
    {"match": "Belgium v Croatia",         "home": "Belgium",     "away": "Croatia",     "start": "02 Jul 19:00", "comp": "FIFA WORLD CUP 2026"},
    {"match": "Italy v Switzerland",       "home": "Italy",       "away": "Switzerland", "start": "02 Jul 23:00", "comp": "FIFA WORLD CUP 2026"},
    {"match": "Australia v South Korea",   "home": "Australia",   "away": "South Korea", "start": "03 Jul 03:00", "comp": "FIFA WORLD CUP 2026"},
    {"match": "Denmark v Mexico",          "home": "Denmark",     "away": "Mexico",      "start": "03 Jul 18:00", "comp": "FIFA WORLD CUP 2026"},
]

BASE_PROBS = {
    "Netherlands v Morocco":   {"Netherlands": 0.52, "Draw": 0.26, "Morocco": 0.22},
    "Portugal v Uruguay":      {"Portugal": 0.48, "Draw": 0.27, "Uruguay": 0.25},
    "France v Argentina":      {"France": 0.38, "Draw": 0.28, "Argentina": 0.34},
    "England v USA":           {"England": 0.44, "Draw": 0.29, "USA": 0.27},
    "Spain v Germany":         {"Spain": 0.41, "Draw": 0.27, "Germany": 0.32},
    "Brazil v Japan":          {"Brazil": 0.61, "Draw": 0.22, "Japan": 0.17},
    "Belgium v Croatia":       {"Belgium": 0.43, "Draw": 0.28, "Croatia": 0.29},
    "Italy v Switzerland":     {"Italy": 0.45, "Draw": 0.28, "Switzerland": 0.27},
    "Australia v South Korea": {"Australia": 0.36, "Draw": 0.30, "South Korea": 0.34},
    "Denmark v Mexico":        {"Denmark": 0.40, "Draw": 0.29, "Mexico": 0.31},
}

BTTS_PROBS = {
    "Netherlands v Morocco": 0.48, "Portugal v Uruguay": 0.52,
    "France v Argentina": 0.61, "England v USA": 0.44,
    "Spain v Germany": 0.58, "Brazil v Japan": 0.38,
    "Belgium v Croatia": 0.55, "Italy v Switzerland": 0.46,
    "Australia v South Korea": 0.50, "Denmark v Mexico": 0.53,
}

OU_LINES = {
    "Netherlands v Morocco": 2.5, "Portugal v Uruguay": 2.5,
    "France v Argentina": 3.5, "England v USA": 2.5,
    "Spain v Germany": 3.5, "Brazil v Japan": 2.5,
    "Belgium v Croatia": 2.5, "Italy v Switzerland": 2.5,
    "Australia v South Korea": 2.5, "Denmark v Mexico": 2.5,
}

OU_OVER_PROBS = {
    "Netherlands v Morocco": 0.44, "Portugal v Uruguay": 0.49,
    "France v Argentina": 0.58, "England v USA": 0.41,
    "Spain v Germany": 0.52, "Brazil v Japan": 0.36,
    "Belgium v Croatia": 0.48, "Italy v Switzerland": 0.43,
    "Australia v South Korea": 0.46, "Denmark v Mexico": 0.51,
}

CARDS_PROBS = {
    "Netherlands v Morocco": {"Over 3.5": 0.52, "Under 3.5": 0.48},
    "Portugal v Uruguay":    {"Over 3.5": 0.48, "Under 3.5": 0.52},
    "France v Argentina":    {"Over 4.5": 0.44, "Under 4.5": 0.56},
    "England v USA":         {"Over 3.5": 0.51, "Under 3.5": 0.49},
    "Spain v Germany":       {"Over 3.5": 0.55, "Under 3.5": 0.45},
    "Brazil v Japan":        {"Over 3.5": 0.47, "Under 3.5": 0.53},
    "Belgium v Croatia":     {"Over 3.5": 0.50, "Under 3.5": 0.50},
    "Italy v Switzerland":   {"Over 3.5": 0.53, "Under 3.5": 0.47},
    "Australia v South Korea": {"Over 3.5": 0.49, "Under 3.5": 0.51},
    "Denmark v Mexico":      {"Over 3.5": 0.46, "Under 3.5": 0.54},
}

PLAYER_POOL = {
    "Netherlands v Morocco": [
        {"name": "C. Gakpo",      "team": "Netherlands", "shots_p90": 2.8, "sot_p90": 1.2, "fouls_p90": 0.6},
        {"name": "X. Simons",     "team": "Netherlands", "shots_p90": 1.9, "sot_p90": 0.9, "fouls_p90": 1.1},
        {"name": "H. Ziyech",     "team": "Morocco",     "shots_p90": 2.1, "sot_p90": 0.8, "fouls_p90": 1.3},
        {"name": "A. Hakimi",     "team": "Morocco",     "shots_p90": 1.4, "sot_p90": 0.6, "fouls_p90": 1.8},
    ],
    "Portugal v Uruguay": [
        {"name": "C. Ronaldo",    "team": "Portugal",    "shots_p90": 4.2, "sot_p90": 1.8, "fouls_p90": 0.9},
        {"name": "B. Fernandes",  "team": "Portugal",    "shots_p90": 2.6, "sot_p90": 1.1, "fouls_p90": 1.4},
        {"name": "D. Núñez",      "team": "Uruguay",     "shots_p90": 3.1, "sot_p90": 1.4, "fouls_p90": 1.1},
        {"name": "F. Valverde",   "team": "Uruguay",     "shots_p90": 1.8, "sot_p90": 0.7, "fouls_p90": 2.1},
    ],
    "France v Argentina": [
        {"name": "K. Mbappé",     "team": "France",      "shots_p90": 4.8, "sot_p90": 2.1, "fouls_p90": 0.8},
        {"name": "A. Griezmann",  "team": "France",      "shots_p90": 2.4, "sot_p90": 1.0, "fouls_p90": 1.2},
        {"name": "L. Messi",      "team": "Argentina",   "shots_p90": 3.6, "sot_p90": 1.6, "fouls_p90": 2.2},
        {"name": "J. Álvarez",    "team": "Argentina",   "shots_p90": 2.7, "sot_p90": 1.2, "fouls_p90": 1.0},
        {"name": "Á. Di María",   "team": "Argentina",   "shots_p90": 2.2, "sot_p90": 0.9, "fouls_p90": 1.6},
    ],
    "England v USA": [
        {"name": "H. Kane",       "team": "England",     "shots_p90": 4.1, "sot_p90": 1.9, "fouls_p90": 1.1},
        {"name": "J. Bellingham", "team": "England",     "shots_p90": 2.3, "sot_p90": 1.0, "fouls_p90": 1.4},
        {"name": "B. Saka",       "team": "England",     "shots_p90": 2.8, "sot_p90": 1.2, "fouls_p90": 0.9},
        {"name": "C. Pulisic",    "team": "USA",         "shots_p90": 2.5, "sot_p90": 1.1, "fouls_p90": 1.3},
    ],
    "Spain v Germany": [
        {"name": "R. Yamal",      "team": "Spain",       "shots_p90": 2.6, "sot_p90": 1.1, "fouls_p90": 0.8},
        {"name": "A. Morata",     "team": "Spain",       "shots_p90": 3.0, "sot_p90": 1.3, "fouls_p90": 1.2},
        {"name": "J. Musiala",    "team": "Germany",     "shots_p90": 2.9, "sot_p90": 1.3, "fouls_p90": 0.9},
        {"name": "K. Havertz",    "team": "Germany",     "shots_p90": 2.4, "sot_p90": 1.0, "fouls_p90": 1.1},
    ],
    "Brazil v Japan": [
        {"name": "Vinicius Jr.",  "team": "Brazil",      "shots_p90": 4.3, "sot_p90": 1.9, "fouls_p90": 2.4},
        {"name": "Rodrygo",       "team": "Brazil",      "shots_p90": 2.6, "sot_p90": 1.1, "fouls_p90": 1.3},
        {"name": "D. Kamada",     "team": "Japan",       "shots_p90": 1.7, "sot_p90": 0.7, "fouls_p90": 1.4},
        {"name": "H. Ito",        "team": "Japan",       "shots_p90": 1.4, "sot_p90": 0.6, "fouls_p90": 1.9},
    ],
    "Belgium v Croatia": [
        {"name": "R. Lukaku",     "team": "Belgium",     "shots_p90": 3.5, "sot_p90": 1.6, "fouls_p90": 1.3},
        {"name": "K. De Bruyne",  "team": "Belgium",     "shots_p90": 2.1, "sot_p90": 0.9, "fouls_p90": 1.0},
        {"name": "L. Modrić",     "team": "Croatia",     "shots_p90": 1.6, "sot_p90": 0.7, "fouls_p90": 1.5},
        {"name": "A. Kramarić",   "team": "Croatia",     "shots_p90": 2.8, "sot_p90": 1.2, "fouls_p90": 1.1},
    ],
    "Italy v Switzerland": [
        {"name": "G. Scamacca",   "team": "Italy",       "shots_p90": 3.1, "sot_p90": 1.4, "fouls_p90": 1.2},
        {"name": "F. Chiesa",     "team": "Italy",       "shots_p90": 2.7, "sot_p90": 1.2, "fouls_p90": 1.6},
        {"name": "X. Shaqiri",    "team": "Switzerland", "shots_p90": 2.3, "sot_p90": 1.0, "fouls_p90": 1.4},
        {"name": "B. Embolo",     "team": "Switzerland", "shots_p90": 2.6, "sot_p90": 1.1, "fouls_p90": 1.3},
    ],
    "Australia v South Korea": [
        {"name": "M. Leckie",     "team": "Australia",   "shots_p90": 1.8, "sot_p90": 0.8, "fouls_p90": 1.4},
        {"name": "M. Duke",       "team": "Australia",   "shots_p90": 2.2, "sot_p90": 1.0, "fouls_p90": 1.6},
        {"name": "Son Heung-min", "team": "South Korea", "shots_p90": 3.4, "sot_p90": 1.5, "fouls_p90": 1.1},
        {"name": "H. Lee",        "team": "South Korea", "shots_p90": 1.9, "sot_p90": 0.8, "fouls_p90": 2.0},
    ],
    "Denmark v Mexico": [
        {"name": "E. Haaland",    "team": "Denmark",     "shots_p90": 4.6, "sot_p90": 2.0, "fouls_p90": 1.0},
        {"name": "C. Eriksen",    "team": "Denmark",     "shots_p90": 1.7, "sot_p90": 0.7, "fouls_p90": 0.9},
        {"name": "H. Lozano",     "team": "Mexico",      "shots_p90": 2.4, "sot_p90": 1.0, "fouls_p90": 1.8},
        {"name": "R. Jiménez",    "team": "Mexico",      "shots_p90": 2.9, "sot_p90": 1.3, "fouls_p90": 1.4},
    ],
}

# ── Helpers ────────────────────────────────────────────────────────────────────
def poisson_over(lam, line):
    k = int(line + 0.5)
    prob_under = sum((lam**i * math.exp(-lam)) / math.factorial(i) for i in range(k + 1))
    return max(0.01, min(0.99, 1 - prob_under))

def gen_bookie_odds(true_prob, seed=0):
    """Generate odds from multiple bookmakers with realistic margin noise."""
    random.seed(seed)
    results = []
    for bm in BOOKMAKERS:
        margin = random.uniform(0.04, 0.12)
        noise  = random.uniform(-0.025, 0.025)
        bm_prob = min(0.97, true_prob * (1 + margin) + noise)
        odds = round(1 / bm_prob, 2)
        results.append({"bookmaker": bm, "odds": odds})
    return sorted(results, key=lambda x: x["odds"], reverse=True)

def best_odds(bookie_list):
    return bookie_list[0] if bookie_list else {"odds": 0, "bookmaker": "—"}

def ev(true_prob, odds):
    return (true_prob * odds) - 1

def has_positive_ev(match_name):
    """Check if any market for this match has positive EV."""
    probs = BASE_PROBS[match_name]
    for outcome, prob in probs.items():
        seed = hash(match_name + outcome) % 10000
        bk = gen_bookie_odds(prob, seed)
        if ev(prob, best_odds(bk)["odds"]) > 0.01:
            return True
    return False

def odds_tooltip_html(bookie_list, true_prob):
    """Render all bookmaker prices as a hover tooltip."""
    rows = ""
    best = bookie_list[0]["odds"]
    for b in bookie_list:
        cls = "tooltip-price-best" if b["odds"] == best else "tooltip-price"
        rows += f'<div class="tooltip-row"><span class="tooltip-bookie">{b["bookmaker"]}</span><span class="{cls}">{b["odds"]:.2f}</span></div>'
    rows += f'<hr class="tooltip-divider"><div class="tooltip-row"><span class="tooltip-bookie" style="color:#5a5a7a">True prob</span><span class="tooltip-price" style="color:#00e5a0">{true_prob*100:.1f}%</span></div>'
    return rows

def render_market_row(outcome_name, true_prob, bookie_list, row_seed):
    bo    = best_odds(bookie_list)
    ev_val = ev(true_prob, bo["odds"])
    ev_cls = "ev-pill-pos" if ev_val > 0 else "ev-pill-neg"
    ev_str = f"+{ev_val*100:.1f}%" if ev_val > 0 else f"{ev_val*100:.1f}%"
    tooltip = odds_tooltip_html(bookie_list, true_prob)
    return f"""
    <div class="market-row">
        <span class="outcome-name">{outcome_name}</span>
        <div class="odds-wrap">
            <div class="odds-btn">
                <div>
                    <div class="odds-btn-price">{bo['odds']:.2f}</div>
                    <div class="odds-btn-bookie">{bo['bookmaker']}</div>
                </div>
            </div>
            <div class="odds-tooltip">{tooltip}</div>
        </div>
        <span class="true-prob">{true_prob*100:.1f}%</span>
        <span class="ev-pill {ev_cls}">{ev_str}</span>
    </div>
    """

# ── Session state ──────────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "home"
if "selected_match" not in st.session_state:
    st.session_state.selected_match = None

# ── Top bar ────────────────────────────────────────────────────────────────────
now = datetime.utcnow().strftime("%d %b %Y  %H:%M UTC")
st.markdown(f"""
<div class="topbar">
    <div style="display:flex;align-items:center;gap:1rem;">
        <div class="logo">INSIDE<span>EDGE</span></div>
        <div class="demo-badge">DEMO</div>
    </div>
    <div class="timestamp">{now}</div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# HOME PAGE — fixture list
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "home":
    st.markdown('<div class="section-label">Upcoming Fixtures</div>', unsafe_allow_html=True)

    for m in MATCHES:
        has_ev = has_positive_ev(m["match"])
        dot    = '<div class="ev-dot"></div>' if has_ev else '<div class="ev-dot-none"></div>'
        ev_tip = '<span style="font-family:JetBrains Mono,monospace;font-size:0.6rem;color:#00e5a0">EV</span>' if has_ev else ""

        col1, col2 = st.columns([10, 1])
        with col1:
            st.markdown(f"""
            <div class="fixture-row">
                <div class="fixture-time">{m['start']}</div>
                <div class="fixture-teams">{m['match']}</div>
                <div class="fixture-comp">{m['comp']}</div>
                {dot}
            </div>
            """, unsafe_allow_html=True)
        with col2:
            if st.button("→", key=f"btn_{m['match']}"):
                st.session_state.selected_match = m["match"]
                st.session_state.page = "match"
                st.rerun()

    st.markdown("""
    <div style="margin-top:1.5rem;padding:0.75rem 1rem;background:#12121a;border:1px solid #1e1e2e;
         border-radius:6px;font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:#5a5a7a;">
        ● Green dot = positive EV opportunity exists in this fixture &nbsp;·&nbsp;
        Hover over any odds to see all bookmaker prices
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# MATCH PAGE
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "match":
    match_name = st.session_state.selected_match
    m = next(x for x in MATCHES if x["match"] == match_name)

    # Back button
    if st.button("← Back to fixtures"):
        st.session_state.page = "home"
        st.rerun()

    # Match header
    st.markdown(f"""
    <div class="match-header">
        <div class="match-header-comp">{m['comp']}</div>
        <div class="match-header-teams">{m['home']} <span style="color:#2e2e4e">v</span> {m['away']}</div>
        <div class="match-header-time">⏱ {m['start']}</div>
    </div>
    """, unsafe_allow_html=True)

    # Column headers
    st.markdown("""
    <div style="display:flex;align-items:center;padding:0 1rem;margin-bottom:0.4rem;gap:0.75rem;">
        <span style="flex:1;font-family:'JetBrains Mono',monospace;font-size:0.6rem;color:#3a3a5a;text-transform:uppercase;letter-spacing:0.1em;">Outcome</span>
        <span style="min-width:5.5rem;font-family:'JetBrains Mono',monospace;font-size:0.6rem;color:#3a3a5a;text-transform:uppercase;letter-spacing:0.1em;">Best Odds ↓hover</span>
        <span style="min-width:3rem;text-align:right;font-family:'JetBrains Mono',monospace;font-size:0.6rem;color:#3a3a5a;text-transform:uppercase;letter-spacing:0.1em;">True %</span>
        <span style="min-width:3.5rem;font-family:'JetBrains Mono',monospace;font-size:0.6rem;color:#3a3a5a;text-transform:uppercase;letter-spacing:0.1em;">EV</span>
    </div>
    """, unsafe_allow_html=True)

    # Market tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Match Result", "Both Teams to Score", "Over / Under", "Cards", "Player Props"
    ])

    # ── Match Result ──
    with tab1:
        probs = BASE_PROBS[match_name]
        outcomes = [m["home"], "Draw", m["away"]]
        rows_html = ""
        for i, outcome in enumerate(outcomes):
            prob = probs[outcome]
            bk   = gen_bookie_odds(prob, seed=hash(match_name + outcome) % 10000)
            rows_html += render_market_row(outcome, prob, bk, i)
        st.markdown(f'<div class="market-table"><div class="market-table-header">Full Time Result</div>{rows_html}</div>', unsafe_allow_html=True)

    # ── BTTS ──
    with tab2:
        btts_yes = BTTS_PROBS[match_name]
        btts_no  = 1 - btts_yes
        rows_html = ""
        for outcome, prob in [("Yes", btts_yes), ("No", btts_no)]:
            bk = gen_bookie_odds(prob, seed=hash(match_name + "btts" + outcome) % 10000)
            rows_html += render_market_row(outcome, prob, bk, 0)
        st.markdown(f'<div class="market-table"><div class="market-table-header">Both Teams to Score</div>{rows_html}</div>', unsafe_allow_html=True)

    # ── Over/Under ──
    with tab3:
        line     = OU_LINES[match_name]
        over_p   = OU_OVER_PROBS[match_name]
        under_p  = 1 - over_p
        rows_html = ""
        for outcome, prob in [(f"Over {line}", over_p), (f"Under {line}", under_p)]:
            bk = gen_bookie_odds(prob, seed=hash(match_name + "ou" + outcome) % 10000)
            rows_html += render_market_row(outcome, prob, bk, 0)
        st.markdown(f'<div class="market-table"><div class="market-table-header">Total Goals — Over/Under {line}</div>{rows_html}</div>', unsafe_allow_html=True)

    # ── Cards ──
    with tab4:
        cards = CARDS_PROBS[match_name]
        rows_html = ""
        for outcome, prob in cards.items():
            bk = gen_bookie_odds(prob, seed=hash(match_name + "cards" + outcome) % 10000)
            rows_html += render_market_row(outcome, prob, bk, 0)
        st.markdown(f'<div class="market-table"><div class="market-table-header">Total Cards</div>{rows_html}</div>', unsafe_allow_html=True)

    # ── Player Props ──
    with tab5:
        players = PLAYER_POOL.get(match_name, [])
        prop_markets = [
            {"label": "Shots",           "stat": "shots_p90", "lines": [1.5, 2.5, 3.5]},
            {"label": "Shots on Target", "stat": "sot_p90",   "lines": [0.5, 1.5, 2.5]},
            {"label": "Fouls Committed", "stat": "fouls_p90", "lines": [0.5, 1.5, 2.5]},
        ]

        sel_market = st.selectbox(
            "Market",
            [pm["label"] for pm in prop_markets],
            label_visibility="collapsed",
            key="prop_market_sel",
        )
        market = next(pm for pm in prop_markets if pm["label"] == sel_market)

        st.markdown(f"""
        <div style="display:flex;align-items:center;padding:0 1rem;margin:0.75rem 0 0.4rem;gap:0.75rem;">
            <span style="flex:1.5;font-family:'JetBrains Mono',monospace;font-size:0.6rem;color:#3a3a5a;text-transform:uppercase;letter-spacing:0.1em;">Player</span>
            <span style="min-width:3rem;font-family:'JetBrains Mono',monospace;font-size:0.6rem;color:#3a3a5a;text-transform:uppercase;letter-spacing:0.1em;">/90</span>
            {"".join(f'<span style="flex:1;text-align:center;font-family:JetBrains Mono,monospace;font-size:0.6rem;color:#3a3a5a;text-transform:uppercase;letter-spacing:0.1em;">O {l}</span>' for l in market['lines'])}
        </div>
        """, unsafe_allow_html=True)

        for player in players:
            lam   = player[market["stat"]]
            cells = ""
            for line in market["lines"]:
                true_prob = poisson_over(lam, line)
                bk        = gen_bookie_odds(true_prob, seed=hash(match_name + player["name"] + str(line)) % 10000)
                bo        = best_odds(bk)
                ev_val    = ev(true_prob, bo["odds"])
                ev_cls    = "ev-pill-pos" if ev_val > 0 else "ev-pill-neg"
                ev_str    = f"+{ev_val*100:.1f}%" if ev_val > 0 else f"{ev_val*100:.1f}%"
                tooltip   = odds_tooltip_html(bk, true_prob)
                cells += f"""
                <div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:0.3rem;">
                    <div class="odds-wrap">
                        <div class="odds-btn" style="min-width:4.5rem;justify-content:center;">
                            <div style="text-align:center">
                                <div class="odds-btn-price">{bo['odds']:.2f}</div>
                                <div class="odds-btn-bookie">{bo['bookmaker']}</div>
                            </div>
                        </div>
                        <div class="odds-tooltip">{tooltip}</div>
                    </div>
                    <span class="ev-pill {ev_cls}" style="font-size:0.58rem">{ev_str}</span>
                </div>
                """

            st.markdown(f"""
            <div class="market-table" style="margin-bottom:0.5rem;">
                <div class="player-row">
                    <div class="player-info" style="flex:1.5">
                        <div class="player-info-name">{player['name']}</div>
                        <div class="player-info-team">{player['team']}</div>
                    </div>
                    <div class="player-stat">{lam:.1f}</div>
                    {cells}
                </div>
            </div>
            """, unsafe_allow_html=True)