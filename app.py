import streamlit as st
from datetime import datetime, timezone, timedelta
import data as D

st.set_page_config(
    page_title="InsideEdge",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

D.API_KEY = st.secrets.get("ODDSPAPI_KEY", "")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500;700&display=swap');

html, body, [class*="css"] { font-family:'Inter',sans-serif; background:#0a0a0f; color:#e8e8f0; }
.stApp { background:#0a0a0f; }
#MainMenu, footer, header { visibility:hidden; }
.block-container { padding:1rem 1.5rem 2rem 1.5rem; max-width:100%; }

.topbar { display:flex; align-items:center; justify-content:space-between; border-bottom:1px solid #1e1e2e; padding-bottom:0.75rem; margin-bottom:1.25rem; }
.logo { font-family:'JetBrains Mono',monospace; font-size:1.25rem; font-weight:700; letter-spacing:0.12em; color:#00e5a0; }
.logo span { color:#5a5a7a; }
.timestamp { font-family:'JetBrains Mono',monospace; font-size:0.7rem; color:#5a5a7a; }

.section-label { font-family:'JetBrains Mono',monospace; font-size:0.65rem; font-weight:500; letter-spacing:0.2em; color:#5a5a7a; text-transform:uppercase; margin-bottom:0.75rem; border-left:2px solid #00e5a0; padding-left:0.5rem; }

.ev-card { background:#12121a; border:1px solid #1e1e2e; border-radius:6px; padding:0.85rem 1rem; margin-bottom:0.5rem; position:relative; overflow:hidden; }
.ev-card:hover { border-color:#2e2e4e; }
.ev-card-accent { position:absolute; top:0; left:0; height:100%; background:linear-gradient(90deg,rgba(0,229,160,0.07),transparent); border-left:3px solid #00e5a0; pointer-events:none; }
.ev-card-top { display:flex; align-items:flex-start; justify-content:space-between; margin-bottom:0.4rem; }
.ev-card-match { font-size:0.82rem; font-weight:600; color:#e8e8f0; }
.ev-card-meta { font-family:'JetBrains Mono',monospace; font-size:0.62rem; color:#5a5a7a; margin-top:0.1rem; }
.ev-badge { font-family:'JetBrains Mono',monospace; font-size:0.9rem; font-weight:700; color:#00e5a0; }
.ev-card-bottom { display:flex; align-items:center; gap:0.6rem; margin-top:0.5rem; flex-wrap:wrap; }
.outcome-tag { font-size:0.78rem; color:#c8c8e0; flex:1; min-width:8rem; }
.bookie-tag { font-family:'JetBrains Mono',monospace; font-size:0.63rem; background:#1e1e2e; color:#9a9ab0; padding:0.15rem 0.4rem; border-radius:3px; white-space:nowrap; }
.odds-tag { font-family:'JetBrains Mono',monospace; font-size:0.82rem; font-weight:600; color:#e8e8f0; }
.prob-tag { font-family:'JetBrains Mono',monospace; font-size:0.63rem; color:#5a5a7a; }
.market-tag { font-family:'JetBrains Mono',monospace; font-size:0.6rem; color:#5a5a7a; background:#0a0a0f; border:1px solid #1e1e2e; padding:0.1rem 0.35rem; border-radius:3px; }
.ev-bar-wrap { height:3px; background:#1e1e2e; border-radius:2px; margin-top:0.55rem; overflow:hidden; }
.ev-bar-fill { height:100%; border-radius:2px; background:linear-gradient(90deg,#00e5a0,#00ffb3); }

.expanded-card { background:#0f0f1a; border:1px solid #00e5a0; border-radius:6px; padding:0.85rem 1rem; margin-bottom:0.5rem; }
.expanded-title { font-family:'JetBrains Mono',monospace; font-size:0.65rem; color:#5a5a7a; letter-spacing:0.15em; text-transform:uppercase; margin-bottom:0.6rem; }
.bm-row { display:flex; align-items:center; justify-content:space-between; padding:0.3rem 0; border-bottom:1px solid #1e1e2e; gap:1rem; }
.bm-row:last-child { border-bottom:none; }
.bm-name { font-family:'JetBrains Mono',monospace; font-size:0.72rem; color:#9a9ab0; flex:1; }
.bm-odds-best { font-family:'JetBrains Mono',monospace; font-size:0.8rem; font-weight:600; color:#00e5a0; }
.bm-odds { font-family:'JetBrains Mono',monospace; font-size:0.8rem; font-weight:600; color:#e8e8f0; }
.bm-ev-pos { font-family:'JetBrains Mono',monospace; font-size:0.65rem; color:#00e5a0; min-width:3rem; text-align:right; }
.bm-ev-neg { font-family:'JetBrains Mono',monospace; font-size:0.65rem; color:#ff4d6d; min-width:3rem; text-align:right; }

.no-data { padding:2rem; text-align:center; color:#5a5a7a; font-family:'JetBrains Mono',monospace; font-size:0.75rem; border:1px dashed #1e1e2e; border-radius:6px; }

div[data-testid="stSelectbox"] > div > div { background:#12121a !important; border:1px solid #1e1e2e !important; color:#e8e8f0 !important; font-family:'JetBrains Mono',monospace !important; }
div[data-testid="stMultiSelect"] > div > div { background:#12121a !important; border:1px solid #1e1e2e !important; }
.stButton > button { background:#12121a !important; border:1px solid #1e1e2e !important; color:#9a9ab0 !important; font-family:'JetBrains Mono',monospace !important; font-size:0.7rem !important; border-radius:4px !important; }
.stButton > button:hover { border-color:#00e5a0 !important; color:#00e5a0 !important; }
div[data-testid="stTextInput"] input { background:#12121a !important; border:1px solid #1e1e2e !important; color:#e8e8f0 !important; font-family:'JetBrains Mono',monospace !important; font-size:0.8rem !important; }
div[data-testid="stMetric"] { background:#12121a; border:1px solid #1e1e2e; border-radius:6px; padding:0.75rem 1rem; }
div[data-testid="stMetric"] label { font-family:'JetBrains Mono',monospace !important; font-size:0.65rem !important; color:#5a5a7a !important; text-transform:uppercase !important; letter-spacing:0.1em !important; }
div[data-testid="stMetric"] div[data-testid="stMetricValue"] { font-family:'JetBrains Mono',monospace !important; font-size:1.3rem !important; color:#e8e8f0 !important; }
</style>
""", unsafe_allow_html=True)

STICKMAN_HTML = """
<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;
     padding:2rem;font-family:'JetBrains Mono',monospace;">
<style>
@keyframes ku-ball {
    0%   { transform: translate(0px, 0px) rotate(0deg); }
    50%  { transform: translate(2px, -52px) rotate(180deg); }
    100% { transform: translate(0px, 0px) rotate(360deg); }
}
@keyframes ku-thigh {
    0%   { transform: rotate(-38deg); }
    12%  { transform: rotate(-52deg); }
    45%  { transform: rotate(-15deg); }
    80%  { transform: rotate(-30deg); }
    100% { transform: rotate(-38deg); }
}
@keyframes ku-shin {
    0%   { transform: rotate(50deg); }
    12%  { transform: rotate(75deg); }
    45%  { transform: rotate(30deg); }
    80%  { transform: rotate(40deg); }
    100% { transform: rotate(50deg); }
}
@keyframes ku-body {
    0%,100% { transform: translateY(0px) rotate(-2deg); }
    12%     { transform: translateY(-3px) rotate(-4deg); }
    55%     { transform: translateY(1px) rotate(0deg); }
}
@keyframes ku-arml {
    0%,100% { transform: rotate(-8deg); }
    12%     { transform: rotate(-22deg); }
    55%     { transform: rotate(5deg); }
}
@keyframes ku-armr {
    0%,100% { transform: rotate(8deg); }
    12%     { transform: rotate(25deg); }
    55%     { transform: rotate(-5deg); }
}
@keyframes ku-stand {
    0%,100% { transform: rotate(2deg); }
    12%     { transform: rotate(4deg); }
    55%     { transform: rotate(0deg); }
}
.ku-ball  { animation: ku-ball  0.85s cubic-bezier(0.35,0,0.65,1) infinite; transform-origin: 66px 128px; }
.ku-body  { animation: ku-body  0.85s ease-in-out infinite; transform-origin: 44px 148px; }
.ku-thigh { animation: ku-thigh 0.85s ease-in-out infinite; transform-origin: 44px 100px; }
.ku-shin  { animation: ku-shin  0.85s ease-in-out infinite; transform-origin: 62px 112px; }
.ku-arml  { animation: ku-arml  0.85s ease-in-out infinite; transform-origin: 44px 72px; }
.ku-armr  { animation: ku-armr  0.85s ease-in-out infinite; transform-origin: 44px 72px; }
.ku-stand { animation: ku-stand 0.85s ease-in-out infinite; transform-origin: 44px 100px; }
</style>
<svg width="120" height="165" viewBox="0 0 120 165">
  <!-- ground shadow -->
  <ellipse cx="50" cy="160" rx="26" ry="3" fill="rgba(0,229,160,0.08)"/>

  <!-- ball: bounces off the foot, spins as it rises -->
  <g class="ku-ball">
    <circle cx="66" cy="128" r="8" stroke="#00e5a0" stroke-width="2" fill="rgba(0,229,160,0.06)"/>
    <path d="M60 124 L66 128 L72 124 M66 128 L66 136" stroke="#00e5a0" stroke-width="1" fill="none" opacity="0.55"/>
  </g>

  <g class="ku-body">
    <!-- head -->
    <circle cx="44" cy="52" r="9" stroke="#00e5a0" stroke-width="2" fill="none"/>
    <circle cx="47" cy="50" r="1.1" fill="#00e5a0"/>
    <path d="M44 56 Q47 57.5 49 55.5" stroke="#00e5a0" stroke-width="1" fill="none"/>
    <!-- torso, slight lean back -->
    <path d="M44 61 Q42 80 44 100" stroke="#00e5a0" stroke-width="2" fill="none"/>
    <!-- left arm: out for balance -->
    <g class="ku-arml">
      <path d="M44 72 Q28 76 20 88" stroke="#00e5a0" stroke-width="2" fill="none"/>
    </g>
    <!-- right arm: swings opposite -->
    <g class="ku-armr">
      <path d="M44 72 Q60 74 70 66" stroke="#00e5a0" stroke-width="2" fill="none"/>
    </g>
  </g>

  <!-- standing leg: slight flex on each touch -->
  <g class="ku-stand">
    <path d="M44 100 Q40 122 38 142" stroke="#00e5a0" stroke-width="2" fill="none"/>
    <line x1="38" y1="142" x2="30" y2="158" stroke="#00e5a0" stroke-width="2"/>
    <line x1="30" y1="158" x2="40" y2="159" stroke="#00e5a0" stroke-width="2"/>
  </g>

  <!-- juggling leg: thigh + shin chained rotation, foot meets ball -->
  <g class="ku-thigh">
    <line x1="44" y1="100" x2="62" y2="112" stroke="#00e5a0" stroke-width="2"/>
    <g class="ku-shin">
      <line x1="62" y1="112" x2="66" y2="128" stroke="#00e5a0" stroke-width="2"/>
      <line x1="66" y1="128" x2="76" y2="126" stroke="#00e5a0" stroke-width="2"/>
    </g>
  </g>
</svg>
<div style="margin-top:0.4rem;font-size:0.7rem;letter-spacing:0.15em;color:#5a5a7a">LOADING MARKETS...</div>
</div>
"""

# ── Session state ──────────────────────────────────────────────────────────────
if "expanded" not in st.session_state:
    st.session_state.expanded = None

# ── Top bar ────────────────────────────────────────────────────────────────────
bst = timezone(timedelta(hours=1))
now = datetime.now(bst).strftime("%d %b %Y  %H:%M BST")
st.markdown(f"""
<div class="topbar">
    <div class="logo">INSIDE<span>EDGE</span></div>
    <div class="timestamp">{now}</div>
</div>
""", unsafe_allow_html=True)

if not D.API_KEY:
    st.error("Add ODDSPAPI_KEY to your Streamlit secrets.")
    st.stop()

# ── Cached data access ─────────────────────────────────────────────────────────
@st.cache_data(ttl=3600)
def get_sports():
    return D.fetch_sports()

@st.cache_data(ttl=600)
def get_tournaments(sport_id):
    return D.fetch_tournaments(sport_id)

@st.cache_data(ttl=3600)
def get_market_names(sport_id):
    return D.fetch_market_names(sport_id)

@st.cache_data(ttl=120)
def get_fixtures(tid):
    return D.fetch_fixtures(tid)

@st.cache_data(ttl=60)
def get_odds(fid):
    return D.fetch_fixture_odds(fid)

@st.cache_data(ttl=3600)
def get_player_names(pids_tuple):
    return D.fetch_player_names(list(pids_tuple))

# ── Resolve sport IDs dynamically ──────────────────────────────────────────────
WANTED_SPORTS = {"⚽  Football": "soccer", "⛳  Golf": "golf", "🏏  Cricket": "cricket"}

@st.cache_data(ttl=3600)
def resolve_sports():
    sports = get_sports()
    resolved = {}
    for label, keyword in WANTED_SPORTS.items():
        for s in sports:
            name = (s.get("sportName") or "").lower()
            if keyword in name:
                resolved[label] = s.get("sportId")
                break
    # Football fallback — we know it is 10
    if "⚽  Football" not in resolved:
        resolved["⚽  Football"] = 10
    return resolved

sport_map = resolve_sports()

# ══════════════════════════════════════════════════════════════════════════════
# FILTERS — Sport first, then Fixture
# ══════════════════════════════════════════════════════════════════════════════
s1, s2 = st.columns([2, 0.6])
with s1:
    sport_label = st.selectbox("Sport", list(sport_map.keys()), label_visibility="collapsed")
with s2:
    st.write("")
    if st.button("↻ Refresh"):
        st.cache_data.clear()
        st.session_state.expanded = None
        st.rerun()

sport_id = sport_map[sport_label]

# Load fixtures for the sport — top tournaments by upcoming fixtures
loading = st.empty()
loading.markdown(STICKMAN_HTML, unsafe_allow_html=True)

tournaments = get_tournaments(sport_id)
# rank tournaments by upcoming fixture count where available
def t_count(t):
    return (t.get("upcomingFixtures") or 0) + (t.get("futureFixtures") or 0)
tournaments = sorted(tournaments, key=t_count, reverse=True)

fixtures = []
for t in tournaments[:4]:
    tid = t.get("tournamentId")
    if tid:
        fixtures.extend(get_fixtures(tid))
fixtures = sorted(fixtures, key=lambda f: f.get("start_ts", 0))[:10]

loading.empty()

if not fixtures:
    st.markdown('<div class="no-data">No upcoming fixtures found for this sport.</div>',
                unsafe_allow_html=True)
    st.stop()

# Fixture filter — below sport
fixture_names = ["All fixtures"] + [f"{fx['home']} v {fx['away']}  ·  {fx['start']}" for fx in fixtures]
sel_fixture = st.selectbox("Fixture", fixture_names, label_visibility="collapsed")

if sel_fixture != "All fixtures":
    idx = fixture_names.index(sel_fixture) - 1
    scan_fixtures = [fixtures[idx]]
else:
    scan_fixtures = fixtures[:6]

# ══════════════════════════════════════════════════════════════════════════════
# SCAN — generic across every market and bookmaker
# ══════════════════════════════════════════════════════════════════════════════
market_names = get_market_names(sport_id)

def build_opportunities(scan_fixtures):
    opps = []
    seen = set()

    for fx in scan_fixtures:
        all_odds = get_odds(fx["fixtureId"])
        if not all_odds:
            continue

        groups = D.scan_all_markets(all_odds, market_names)

        # Collect playerIds for name merge
        pids = {g["playerId"] for g in groups if g["playerId"]}
        names = get_player_names(tuple(sorted(pids))) if pids else {}

        for g in groups:
            bm_prices = g["bookmakers"]
            if len(g["all_prices"]) < 2 or not bm_prices:
                continue

            true_prob, benchmark = D.market_true_prob(g["all_prices"])
            if not true_prob:
                continue

            dedup = (fx["fixtureId"], g["marketId"], g["outcomeId"],
                     g["playerId"], g["handicap"])
            if dedup in seen:
                continue
            seen.add(dedup)

            # Build outcome label
            label = g["marketName"]
            if g["playerId"]:
                pname = names.get(g["playerId"], f"Player {g['playerId']}")
                label = f"{pname} — {label}"
            if g["handicap"] is not None:
                label += f" {g['handicap']}"

            best_price, best_bm = D.best_odds(bm_prices)
            ev = D.calc_ev(true_prob, best_price)
            if ev <= 0:
                continue

            opps.append({
                "fixtureId":  fx["fixtureId"],
                "match":      f"{fx['home']} v {fx['away']}",
                "start":      fx["start"],
                "market":     g["marketName"],
                "outcome":    label,
                "best_bm":    best_bm,
                "best_price": best_price,
                "true_prob":  true_prob,
                "ev":         ev,
                "all_prices": bm_prices,
                "benchmark":  benchmark,
            })

    return sorted(opps, key=lambda x: x["ev"], reverse=True)

scan_placeholder = st.empty()
scan_placeholder.markdown(STICKMAN_HTML, unsafe_allow_html=True)
all_opportunities = build_opportunities(scan_fixtures)
scan_placeholder.empty()

# ══════════════════════════════════════════════════════════════════════════════
# SECONDARY FILTERS — market, bookmaker, odds (post-scan, options from real data)
# ══════════════════════════════════════════════════════════════════════════════
f1, f2, f3 = st.columns([2, 2, 1.8])
with f1:
    discovered_markets = sorted({o["market"] for o in all_opportunities})
    sel_market = st.selectbox("Market", ["All Markets"] + discovered_markets,
                              label_visibility="collapsed")
with f2:
    discovered_bms = sorted({o["best_bm"] for o in all_opportunities})
    sel_bm = st.multiselect("Bookmakers", options=discovered_bms,
                            format_func=D.bm_label, default=[],
                            placeholder="All bookmakers",
                            label_visibility="collapsed")
with f3:
    odds_options = [1, 1.5, 2, 2.5, 3, 4, 5, 7.5, 10, 15, 20, 30, 50, "∞"]
    odds_raw = st.select_slider("Odds", options=odds_options, value=(1, "∞"),
                                label_visibility="collapsed")
    lo_val = float(odds_raw[0])
    hi_val = float("inf") if odds_raw[1] == "∞" else float(odds_raw[1])

opportunities = [
    o for o in all_opportunities
    if (sel_market == "All Markets" or o["market"] == sel_market)
    and (not sel_bm or o["best_bm"] in sel_bm)
    and lo_val <= o["best_price"] <= hi_val
]

# ── Metrics ────────────────────────────────────────────────────────────────────
m1, m2, m3, m4 = st.columns(4)
with m1: st.metric("Fixtures Scanned", len(scan_fixtures))
with m2: st.metric("EV Opportunities", len(opportunities))
with m3: st.metric("Best EV", f"+{opportunities[0]['ev']*100:.1f}%" if opportunities else "—")
with m4: st.metric("Markets Found", len(discovered_markets))

st.write("")

# ── Coverage debug ─────────────────────────────────────────────────────────────
with st.expander("🔍 Bookmaker coverage", expanded=False):
    coverage = {}
    for fx in scan_fixtures:
        odds = get_odds(fx["fixtureId"])
        for bm, bm_odds in odds.items():
            props = sum(1 for o in bm_odds.values() if o.get("playerId", 0) != 0)
            if bm not in coverage:
                coverage[bm] = {"odds": 0, "props": 0}
            coverage[bm]["odds"]  += len(bm_odds)
            coverage[bm]["props"] += props
    missing = [b for b in D.ALL_BOOKMAKERS if b not in coverage and b not in D.EXCLUDED_FROM_EV]
    for bm in sorted(coverage, key=lambda b: -coverage[b]["odds"]):
        c = coverage[bm]
        st.markdown(
            f'<span style="font-family:JetBrains Mono,monospace;font-size:0.72rem;color:#9a9ab0">'
            f'{D.bm_label(bm)}: {c["odds"]} odds · {c["props"]} player props</span>',
            unsafe_allow_html=True)
    if missing:
        st.markdown(
            f'<span style="font-family:JetBrains Mono,monospace;font-size:0.72rem;color:#ff4d6d">'
            f'No data: {", ".join(D.bm_label(b) for b in missing)}</span>',
            unsafe_allow_html=True)

# ── EV Feed ────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Best Bets Right Now</div>', unsafe_allow_html=True)

display_opps = opportunities[:20]

if not display_opps:
    st.markdown(
        '<div class="no-data">No opportunities match your filters.<br>'
        '<span style="font-size:0.65rem">Try widening the odds range or clearing filters.</span></div>',
        unsafe_allow_html=True)
else:
    for idx, opp in enumerate(display_opps):
        card_id = f"{idx}_{opp['fixtureId']}_{opp['market']}_{opp['outcome']}"
        is_expanded = st.session_state.expanded == card_id
        ev_pct    = opp["ev"] * 100
        bar_width = min(ev_pct * 5, 100)
        bm_imp    = 1 / opp["best_price"]
        edge      = opp["true_prob"] - bm_imp

        st.markdown(f"""
        <div class="ev-card">
            <div class="ev-card-accent"></div>
            <div class="ev-card-top">
                <div>
                    <div class="ev-card-match">{opp['match']}</div>
                    <div class="ev-card-meta">{opp['start']} &nbsp;·&nbsp;
                        <span class="market-tag">{opp['market']}</span>
                    </div>
                </div>
                <div style="text-align:right;flex-shrink:0;margin-left:1rem">
                    <div class="ev-badge">+{ev_pct:.1f}%</div>
                </div>
            </div>
            <div class="ev-card-bottom">
                <span class="outcome-tag">{opp['outcome']}</span>
                <span class="bookie-tag">{D.bm_label(opp['best_bm'])}</span>
                <span class="odds-tag">{opp['best_price']:.2f}</span>
                <span class="prob-tag">
                    True: {opp['true_prob']*100:.1f}%
                    &nbsp;·&nbsp; Implied: {bm_imp*100:.1f}%
                    &nbsp;·&nbsp; Edge: +{edge*100:.1f}pp
                    &nbsp;·&nbsp; via {opp['benchmark']}
                </span>
            </div>
            <div class="ev-bar-wrap">
                <div class="ev-bar-fill" style="width:{bar_width}%"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        btn_label = "▲ Hide prices" if is_expanded else "▼ All bookmaker prices"
        if st.button(btn_label, key=f"exp_{card_id}"):
            st.session_state.expanded = None if is_expanded else card_id
            st.rerun()

        if is_expanded:
            true_prob  = opp["true_prob"]
            ranked     = sorted(opp["all_prices"].items(), key=lambda x: x[1], reverse=True)
            best_price = ranked[0][1] if ranked else 0

            rows_html = ""
            for bm, price in ranked:
                ev     = D.calc_ev(true_prob, price)
                od_cls = "bm-odds-best" if price == best_price else "bm-odds"
                if ev > 0:
                    ev_str, ev_cls = f"+{ev*100:.1f}%", "bm-ev-pos"
                else:
                    ev_str, ev_cls = f"{ev*100:.1f}%", "bm-ev-neg"
                rows_html += (
                    f'<div class="bm-row">'
                    f'<span class="bm-name">{D.bm_label(bm)}</span>'
                    f'<span class="{od_cls}">{price:.2f}</span>'
                    f'<span class="{ev_cls}">{ev_str}</span>'
                    f'</div>'
                )

            st.markdown(f"""
            <div class="expanded-card">
                <div class="expanded-title">{opp['outcome']} — {opp['match']}</div>
                <div style="margin-bottom:0.5rem;font-family:'JetBrains Mono',monospace;
                     font-size:0.65rem;color:#5a5a7a">
                    True prob ({opp['benchmark']}): {true_prob*100:.1f}%
                </div>
                {rows_html}
            </div>
            """, unsafe_allow_html=True)
