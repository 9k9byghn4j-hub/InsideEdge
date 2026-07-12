import streamlit as st
from datetime import datetime, timezone, timedelta
import data as D

st.set_page_config(page_title="InsideEdge", page_icon="⚡", layout="wide",
                   initial_sidebar_state="collapsed")

D.API_KEY = st.secrets.get("ODDSPAPI_KEY", "")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500;700&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;background:#0a0a0f;color:#e8e8f0}
.stApp{background:#0a0a0f}
#MainMenu,footer,header{visibility:hidden}
.block-container{padding:1rem 1.5rem 2rem 1.5rem;max-width:100%}

.topbar{display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid #1e1e2e;padding-bottom:.75rem;margin-bottom:1.25rem}
.logo{font-family:'JetBrains Mono',monospace;font-size:1.25rem;font-weight:700;letter-spacing:.12em;color:#00e5a0}
.logo span{color:#5a5a7a}
.ts{font-family:'JetBrains Mono',monospace;font-size:.7rem;color:#5a5a7a}

.section-label{font-family:'JetBrains Mono',monospace;font-size:.65rem;font-weight:500;letter-spacing:.2em;color:#5a5a7a;text-transform:uppercase;margin-bottom:.75rem;border-left:2px solid #00e5a0;padding-left:.5rem}

.ev-card{background:#12121a;border:1px solid #1e1e2e;border-radius:6px;padding:.85rem 1rem;margin-bottom:.5rem;position:relative;overflow:hidden}
.ev-card:hover{border-color:#2e2e4e}
.ev-card-accent{position:absolute;top:0;left:0;height:100%;background:linear-gradient(90deg,rgba(0,229,160,.07),transparent);border-left:3px solid #00e5a0;pointer-events:none}
.ev-card-top{display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:.4rem}
.ev-match{font-size:.82rem;font-weight:600;color:#e8e8f0}
.ev-meta{font-family:'JetBrains Mono',monospace;font-size:.62rem;color:#5a5a7a;margin-top:.1rem}
.ev-badge{font-family:'JetBrains Mono',monospace;font-size:.9rem;font-weight:700;color:#00e5a0}
.ev-bottom{display:flex;align-items:center;gap:.6rem;margin-top:.5rem;flex-wrap:wrap}
.outcome-tag{font-size:.78rem;color:#c8c8e0;flex:1;min-width:8rem}
.bookie-tag{font-family:'JetBrains Mono',monospace;font-size:.63rem;background:#1e1e2e;color:#9a9ab0;padding:.15rem .4rem;border-radius:3px;white-space:nowrap}
.odds-tag{font-family:'JetBrains Mono',monospace;font-size:.82rem;font-weight:600;color:#e8e8f0}
.prob-tag{font-family:'JetBrains Mono',monospace;font-size:.63rem;color:#5a5a7a}
.mkt-tag{font-family:'JetBrains Mono',monospace;font-size:.6rem;color:#5a5a7a;background:#0a0a0f;border:1px solid #1e1e2e;padding:.1rem .35rem;border-radius:3px}
.ev-bar-wrap{height:3px;background:#1e1e2e;border-radius:2px;margin-top:.55rem;overflow:hidden}
.ev-bar-fill{height:100%;border-radius:2px;background:linear-gradient(90deg,#00e5a0,#00ffb3)}

.xp-card{background:#0f0f1a;border:1px solid #00e5a0;border-radius:6px;padding:.85rem 1rem;margin-bottom:.5rem}
.xp-title{font-family:'JetBrains Mono',monospace;font-size:.65rem;color:#5a5a7a;letter-spacing:.15em;text-transform:uppercase;margin-bottom:.6rem}
.bm-row{display:flex;align-items:center;justify-content:space-between;padding:.3rem 0;border-bottom:1px solid #1e1e2e;gap:1rem}
.bm-row:last-child{border-bottom:none}
.bm-name{font-family:'JetBrains Mono',monospace;font-size:.72rem;color:#9a9ab0;flex:1}
.bm-odds-best{font-family:'JetBrains Mono',monospace;font-size:.8rem;font-weight:600;color:#00e5a0}
.bm-odds{font-family:'JetBrains Mono',monospace;font-size:.8rem;font-weight:600;color:#e8e8f0}
.bm-ev-pos{font-family:'JetBrains Mono',monospace;font-size:.65rem;color:#00e5a0;min-width:3rem;text-align:right}
.bm-ev-neg{font-family:'JetBrains Mono',monospace;font-size:.65rem;color:#ff4d6d;min-width:3rem;text-align:right}
.no-data{padding:2rem;text-align:center;color:#5a5a7a;font-family:'JetBrains Mono',monospace;font-size:.75rem;border:1px dashed #1e1e2e;border-radius:6px}

div[data-testid="stSelectbox"]>div>div{background:#12121a!important;border:1px solid #1e1e2e!important;color:#e8e8f0!important;font-family:'JetBrains Mono',monospace!important}
div[data-testid="stMultiSelect"]>div>div{background:#12121a!important;border:1px solid #1e1e2e!important}
.stButton>button{background:#12121a!important;border:1px solid #1e1e2e!important;color:#9a9ab0!important;font-family:'JetBrains Mono',monospace!important;font-size:.7rem!important;border-radius:4px!important}
.stButton>button:hover{border-color:#00e5a0!important;color:#00e5a0!important}
div[data-testid="stMetric"]{background:#12121a;border:1px solid #1e1e2e;border-radius:6px;padding:.75rem 1rem}
div[data-testid="stMetric"] label{font-family:'JetBrains Mono',monospace!important;font-size:.65rem!important;color:#5a5a7a!important;text-transform:uppercase!important;letter-spacing:.1em!important}
div[data-testid="stMetric"] div[data-testid="stMetricValue"]{font-family:'JetBrains Mono',monospace!important;font-size:1.3rem!important;color:#e8e8f0!important}
</style>
""", unsafe_allow_html=True)

STICKMAN_HTML = """
<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;
     padding:2rem;font-family:'JetBrains Mono',monospace;">
<style>
@keyframes ku-ball{0%{transform:translate(0,0) rotate(0deg)}50%{transform:translate(2px,-52px) rotate(180deg)}100%{transform:translate(0,0) rotate(360deg)}}
@keyframes ku-thigh{0%,100%{transform:rotate(-38deg)}12%{transform:rotate(-52deg)}45%{transform:rotate(-15deg)}80%{transform:rotate(-30deg)}}
@keyframes ku-shin{0%,100%{transform:rotate(50deg)}12%{transform:rotate(75deg)}45%{transform:rotate(30deg)}80%{transform:rotate(40deg)}}
@keyframes ku-body{0%,100%{transform:translateY(0) rotate(-2deg)}12%{transform:translateY(-3px) rotate(-4deg)}55%{transform:translateY(1px) rotate(0)}}
@keyframes ku-arml{0%,100%{transform:rotate(-8deg)}12%{transform:rotate(-22deg)}55%{transform:rotate(5deg)}}
@keyframes ku-armr{0%,100%{transform:rotate(8deg)}12%{transform:rotate(25deg)}55%{transform:rotate(-5deg)}}
@keyframes ku-stand{0%,100%{transform:rotate(2deg)}12%{transform:rotate(4deg)}55%{transform:rotate(0)}}
.ku-ball{animation:ku-ball .85s cubic-bezier(.35,0,.65,1) infinite;transform-origin:66px 128px}
.ku-body{animation:ku-body .85s ease-in-out infinite;transform-origin:44px 148px}
.ku-thigh{animation:ku-thigh .85s ease-in-out infinite;transform-origin:44px 100px}
.ku-shin{animation:ku-shin .85s ease-in-out infinite;transform-origin:62px 112px}
.ku-arml{animation:ku-arml .85s ease-in-out infinite;transform-origin:44px 72px}
.ku-armr{animation:ku-armr .85s ease-in-out infinite;transform-origin:44px 72px}
.ku-stand{animation:ku-stand .85s ease-in-out infinite;transform-origin:44px 100px}
</style>
<svg width="120" height="165" viewBox="0 0 120 165">
  <ellipse cx="50" cy="160" rx="26" ry="3" fill="rgba(0,229,160,.08)"/>
  <g class="ku-ball"><circle cx="66" cy="128" r="8" stroke="#00e5a0" stroke-width="2" fill="rgba(0,229,160,.06)"/><path d="M60 124 L66 128 L72 124 M66 128 L66 136" stroke="#00e5a0" stroke-width="1" fill="none" opacity=".55"/></g>
  <g class="ku-body">
    <circle cx="44" cy="52" r="9" stroke="#00e5a0" stroke-width="2" fill="none"/>
    <circle cx="47" cy="50" r="1.1" fill="#00e5a0"/>
    <path d="M44 56 Q47 57.5 49 55.5" stroke="#00e5a0" stroke-width="1" fill="none"/>
    <path d="M44 61 Q42 80 44 100" stroke="#00e5a0" stroke-width="2" fill="none"/>
    <g class="ku-arml"><path d="M44 72 Q28 76 20 88" stroke="#00e5a0" stroke-width="2" fill="none"/></g>
    <g class="ku-armr"><path d="M44 72 Q60 74 70 66" stroke="#00e5a0" stroke-width="2" fill="none"/></g>
  </g>
  <g class="ku-stand"><path d="M44 100 Q40 122 38 142" stroke="#00e5a0" stroke-width="2" fill="none"/><line x1="38" y1="142" x2="30" y2="158" stroke="#00e5a0" stroke-width="2"/><line x1="30" y1="158" x2="40" y2="159" stroke="#00e5a0" stroke-width="2"/></g>
  <g class="ku-thigh"><line x1="44" y1="100" x2="62" y2="112" stroke="#00e5a0" stroke-width="2"/><g class="ku-shin"><line x1="62" y1="112" x2="66" y2="128" stroke="#00e5a0" stroke-width="2"/><line x1="66" y1="128" x2="76" y2="126" stroke="#00e5a0" stroke-width="2"/></g></g>
</svg>
<div style="margin-top:.4rem;font-size:.7rem;letter-spacing:.15em;color:#5a5a7a">LOADING MARKETS...</div>
</div>
"""

# ── Session state ──────────────────────────────────────────────────────────────
if "expanded" not in st.session_state:
    st.session_state.expanded = None

# ── Top bar ────────────────────────────────────────────────────────────────────
bst = timezone(timedelta(hours=1))
now = datetime.now(bst).strftime("%d %b %Y  %H:%M BST")
st.markdown(f'<div class="topbar"><div class="logo">INSIDE<span>EDGE</span></div><div class="ts">{now}</div></div>',
            unsafe_allow_html=True)

if not D.API_KEY:
    st.error("Add ODDSPAPI_KEY to Streamlit secrets.")
    st.stop()

# ── Cached fetchers ────────────────────────────────────────────────────────────
@st.cache_data(ttl=3600)
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

# ── Sport + Fixture filters ────────────────────────────────────────────────────
s1, s2 = st.columns([3, 0.7])
with s1:
    sport_label = st.selectbox("Sport", list(D.SPORTS.keys()), label_visibility="collapsed")
with s2:
    st.write("")
    if st.button("↻ Refresh"):
        st.cache_data.clear()
        st.session_state.expanded = None
        st.rerun()

sport_id = D.SPORTS[sport_label]

# Load fixtures — pin World Cup/EPL/UCL first
loading = st.empty()
loading.markdown(STICKMAN_HTML, unsafe_allow_html=True)

tournaments = get_tournaments(sport_id)
def t_score(t):
    return ((t.get("upcomingFixtures") or 0) +
            (t.get("futureFixtures")   or 0) +
            (t.get("liveFixtures")     or 0))
pinned = [t for t in tournaments if t.get("tournamentId") in D.PINNED_TOURNAMENT_IDS]
others = sorted([t for t in tournaments if t.get("tournamentId") not in D.PINNED_TOURNAMENT_IDS],
                key=t_score, reverse=True)
ranked = pinned + others

fixtures = []
seen_ids = set()
for t in ranked[:8]:
    tid = t.get("tournamentId")
    if tid:
        for fx in get_fixtures(tid):
            if fx["fixtureId"] not in seen_ids:
                fixtures.append(fx)
                seen_ids.add(fx["fixtureId"])

fixtures = sorted(fixtures, key=lambda f: f.get("start_ts", 0))
loading.empty()

if not fixtures:
    st.markdown('<div class="no-data">No upcoming fixtures found.</div>', unsafe_allow_html=True)
    st.stop()

# Fixture selector
fixture_labels = ["All fixtures"] + [
    f"{fx['home']} v {fx['away']}  ·  {fx['start']}" for fx in fixtures
]
sel_fixture = st.selectbox("Fixture", fixture_labels, label_visibility="collapsed")

if sel_fixture != "All fixtures":
    idx = fixture_labels.index(sel_fixture) - 1
    scan_fixtures = [fixtures[idx]]
else:
    scan_fixtures = fixtures[:10]  # scan next 10 for speed

# ── Scan ──────────────────────────────────────────────────────────────────────
market_names = get_market_names(sport_id)

def build_opportunities(scan_fixtures):
    opps = []
    seen = set()

    for fx in scan_fixtures:
        all_odds = get_odds(fx["fixtureId"])
        if not all_odds:
            continue

        groups = D.scan_all_markets(all_odds, market_names)

        # Collect player names
        pids = {g["playerId"] for g in groups if g.get("playerId")}
        names = get_player_names(tuple(sorted(pids))) if pids else {}

        for g in groups:
            tp = g.get("true_prob")
            bm_prices = g.get("bookmakers", {})
            if not tp or not bm_prices:
                continue

            best_price, best_bm = D.best_odds(bm_prices)
            if not best_price:
                continue

            ev = D.calc_ev(tp, best_price)
            if ev <= 0:
                continue

            dedup = (fx["fixtureId"], g["marketId"], g["outcomeId"],
                     g.get("playerId", 0), g.get("handicap"))
            if dedup in seen:
                continue
            seen.add(dedup)

            # Build outcome label
            label = g["marketName"]
            if g.get("playerId"):
                pname = names.get(g["playerId"], f"Player {g['playerId']}")
                label = f"{pname} — {label}"
            if g.get("handicap") is not None:
                label += f" {g['handicap']}"

            opps.append({
                "fixtureId":  fx["fixtureId"],
                "match":      f"{fx['home']} v {fx['away']}",
                "start":      fx["start"],
                "market":     g["marketName"],
                "outcome":    label,
                "best_bm":    best_bm,
                "best_price": best_price,
                "true_prob":  tp,
                "ev":         ev,
                "all_prices": bm_prices,
                "benchmark":  g.get("benchmark", "—"),
            })

    return sorted(opps, key=lambda x: x["ev"], reverse=True)

scan_ph = st.empty()
scan_ph.markdown(STICKMAN_HTML, unsafe_allow_html=True)
all_opportunities = build_opportunities(scan_fixtures)
scan_ph.empty()

# ── Secondary filters ──────────────────────────────────────────────────────────
f1, f2, f3 = st.columns([2, 2.5, 1.8])
with f1:
    mkt_options = ["All Markets"] + sorted({o["market"] for o in all_opportunities})
    sel_market = st.selectbox("Market", mkt_options, label_visibility="collapsed")
with f2:
    bm_options = sorted({o["best_bm"] for o in all_opportunities})
    sel_bm = st.multiselect("Bookmakers", bm_options, format_func=D.bm_label,
                            default=[], placeholder="All bookmakers",
                            label_visibility="collapsed")
with f3:
    odds_opts = [1, 1.5, 2, 2.5, 3, 4, 5, 7.5, 10, 15, 20, 30, 50, "∞"]
    odds_raw = st.select_slider("Odds", options=odds_opts, value=(1, "∞"),
                                label_visibility="collapsed")
    lo = float(odds_raw[0])
    hi = float("inf") if odds_raw[1] == "∞" else float(odds_raw[1])

opportunities = [
    o for o in all_opportunities
    if (sel_market == "All Markets" or o["market"] == sel_market)
    and (not sel_bm or o["best_bm"] in sel_bm)
    and lo <= o["best_price"] <= hi
]

# ── Metrics ────────────────────────────────────────────────────────────────────
m1, m2, m3, m4 = st.columns(4)
with m1: st.metric("Fixtures Scanned", len(scan_fixtures))
with m2: st.metric("EV Opportunities", len(opportunities))
with m3: st.metric("Best EV", f"+{opportunities[0]['ev']*100:.1f}%" if opportunities else "—")
with m4: st.metric("Markets Found", len({o["market"] for o in all_opportunities}))

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
        st.markdown(f'<span style="font-family:JetBrains Mono,monospace;font-size:.72rem;color:#9a9ab0">'
                    f'{D.bm_label(bm)}: {c["odds"]} odds · {c["props"]} player props</span>',
                    unsafe_allow_html=True)
    if missing:
        st.markdown(f'<span style="font-family:JetBrains Mono,monospace;font-size:.72rem;color:#ff4d6d">'
                    f'No data: {", ".join(D.bm_label(b) for b in missing)}</span>',
                    unsafe_allow_html=True)

# ── EV Feed ────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Best Bets Right Now</div>', unsafe_allow_html=True)

if not opportunities:
    st.markdown('<div class="no-data">No opportunities match your filters.</div>',
                unsafe_allow_html=True)
else:
    for idx, opp in enumerate(opportunities[:20]):
        card_id    = f"card_{idx}"
        is_exp     = st.session_state.expanded == card_id
        ev_pct     = opp["ev"] * 100
        bar_width  = min(ev_pct * 5, 100)
        bm_imp     = 1 / opp["best_price"]
        edge       = opp["true_prob"] - bm_imp

        st.markdown(f"""
        <div class="ev-card">
            <div class="ev-card-accent"></div>
            <div class="ev-card-top">
                <div>
                    <div class="ev-match">{opp['match']}</div>
                    <div class="ev-meta">{opp['start']} &nbsp;·&nbsp;
                        <span class="mkt-tag">{opp['market']}</span></div>
                </div>
                <div style="text-align:right;flex-shrink:0;margin-left:1rem">
                    <div class="ev-badge">+{ev_pct:.1f}%</div>
                </div>
            </div>
            <div class="ev-bottom">
                <span class="outcome-tag">{opp['outcome']}</span>
                <span class="bookie-tag">{D.bm_label(opp['best_bm'])}</span>
                <span class="odds-tag">{opp['best_price']:.2f}</span>
                <span class="prob-tag">True: {opp['true_prob']*100:.1f}%
                    &nbsp;·&nbsp; Implied: {bm_imp*100:.1f}%
                    &nbsp;·&nbsp; Edge: +{edge*100:.1f}pp
                    &nbsp;·&nbsp; {opp['benchmark']}</span>
            </div>
            <div class="ev-bar-wrap">
                <div class="ev-bar-fill" style="width:{bar_width}%"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        btn = "▲ Hide prices" if is_exp else "▼ All bookmaker prices"
        if st.button(btn, key=f"btn_{card_id}"):
            st.session_state.expanded = None if is_exp else card_id
            st.rerun()

        if is_exp:
            tp     = opp["true_prob"]
            ranked = sorted(opp["all_prices"].items(), key=lambda x: x[1], reverse=True)
            best_p = ranked[0][1] if ranked else 0

            rows = ""
            for bm, price in ranked:
                ev     = D.calc_ev(tp, price)
                od_cls = "bm-odds-best" if price == best_p else "bm-odds"
                ev_cls = "bm-ev-pos" if ev > 0 else "bm-ev-neg"
                ev_str = f"+{ev*100:.1f}%" if ev > 0 else f"{ev*100:.1f}%"
                rows  += (f'<div class="bm-row"><span class="bm-name">{D.bm_label(bm)}</span>'
                          f'<span class="{od_cls}">{price:.2f}</span>'
                          f'<span class="{ev_cls}">{ev_str}</span></div>')

            st.markdown(f"""
            <div class="xp-card">
                <div class="xp-title">{opp['outcome']} — {opp['match']}</div>
                <div style="margin-bottom:.5rem;font-family:'JetBrains Mono',monospace;
                     font-size:.65rem;color:#5a5a7a">
                    True prob ({opp['benchmark']}): {tp*100:.1f}%
                </div>{rows}
            </div>
            """, unsafe_allow_html=True)