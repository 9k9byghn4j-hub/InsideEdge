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

/* ── Price card ── */
.pc{background:#12121a;border:1px solid #1e1e2e;border-radius:6px;padding:.85rem 1rem;margin-bottom:.5rem;position:relative;overflow:hidden}
.pc:hover{border-color:#2e2e4e}
.pc-accent{position:absolute;top:0;left:0;height:100%;background:linear-gradient(90deg,rgba(0,229,160,.07),transparent);border-left:3px solid #00e5a0;pointer-events:none}
.pc-top{display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:.4rem}
.pc-match{font-size:.82rem;font-weight:600;color:#e8e8f0}
.pc-meta{font-family:'JetBrains Mono',monospace;font-size:.62rem;color:#5a5a7a;margin-top:.1rem}
.pc-edge{font-family:'JetBrains Mono',monospace;font-size:.9rem;font-weight:700;color:#00e5a0;text-align:right}
.pc-edge-sub{font-family:'JetBrains Mono',monospace;font-size:.62rem;color:#5a5a7a;text-align:right}
.pc-bottom{display:flex;align-items:center;gap:.6rem;margin-top:.5rem;flex-wrap:wrap}
.outcome-tag{font-size:.78rem;color:#c8c8e0;flex:1;min-width:8rem}
.bookie-tag{font-family:'JetBrains Mono',monospace;font-size:.63rem;background:#1e1e2e;color:#9a9ab0;padding:.15rem .4rem;border-radius:3px;white-space:nowrap}
.odds-tag{font-family:'JetBrains Mono',monospace;font-size:.88rem;font-weight:700;color:#00e5a0}
.avg-tag{font-family:'JetBrains Mono',monospace;font-size:.72rem;color:#5a5a7a}
.mkt-tag{font-family:'JetBrains Mono',monospace;font-size:.6rem;color:#5a5a7a;background:#0a0a0f;border:1px solid #1e1e2e;padding:.1rem .35rem;border-radius:3px}
.ev-bar-wrap{height:3px;background:#1e1e2e;border-radius:2px;margin-top:.55rem;overflow:hidden}
.ev-bar-fill{height:100%;border-radius:2px;background:linear-gradient(90deg,#00e5a0,#00ffb3)}

/* ── Expanded ── */
.xp-card{background:#0f0f1a;border:1px solid #00e5a0;border-radius:6px;padding:.85rem 1rem;margin-bottom:.5rem}
.xp-title{font-family:'JetBrains Mono',monospace;font-size:.65rem;color:#5a5a7a;letter-spacing:.15em;text-transform:uppercase;margin-bottom:.6rem}
.bm-row{display:flex;align-items:center;justify-content:space-between;padding:.3rem 0;border-bottom:1px solid #1e1e2e;gap:1rem}
.bm-row:last-child{border-bottom:none}
.bm-name{font-family:'JetBrains Mono',monospace;font-size:.72rem;color:#9a9ab0;flex:1}
.bm-odds-best{font-family:'JetBrains Mono',monospace;font-size:.8rem;font-weight:700;color:#00e5a0}
.bm-odds{font-family:'JetBrains Mono',monospace;font-size:.8rem;color:#e8e8f0}
.bm-above{font-family:'JetBrains Mono',monospace;font-size:.65rem;color:#00e5a0;min-width:3.5rem;text-align:right}
.bm-below{font-family:'JetBrains Mono',monospace;font-size:.65rem;color:#ff4d6d;min-width:3.5rem;text-align:right}
.bm-avg{font-family:'JetBrains Mono',monospace;font-size:.65rem;color:#5a5a7a;min-width:3.5rem;text-align:right}

/* ── Misc ── */
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
<g class="ku-ball"><circle cx="66" cy="128" r="8" stroke="#00e5a0" stroke-width="2" fill="rgba(0,229,160,.06)"/><path d="M60 124L66 128L72 124M66 128L66 136" stroke="#00e5a0" stroke-width="1" fill="none" opacity=".55"/></g>
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
st.markdown(f'<div class="topbar"><div class="logo">INSIDE<span>EDGE</span></div>'
            f'<div class="ts">{now}</div></div>', unsafe_allow_html=True)

if not D.API_KEY:
    st.error("Add ODDSPAPI_KEY to Streamlit secrets.")
    st.stop()

# ── Cached fetchers ────────────────────────────────────────────────────────────
@st.cache_data(ttl=3600)
def get_tournaments(sport_id):
    return D.fetch_tournaments(sport_id)

@st.cache_data(ttl=120)
def get_fixtures(tid):
    return D.fetch_fixtures(tid)

@st.cache_data(ttl=120)
def get_odds(fid):
    return D.fetch_fixture_odds(fid)

@st.cache_data(ttl=3600)
def get_player_names(pids_tuple):
    return D.fetch_player_names(list(pids_tuple))

# ── Sport filter ───────────────────────────────────────────────────────────────
s1, s2 = st.columns([3, 0.7])
with s1:
    sport_label = st.selectbox("Sport", list(D.SPORTS.keys()),
                               label_visibility="collapsed")
with s2:
    st.write("")
    if st.button("↻ Refresh"):
        st.cache_data.clear()
        st.session_state.expanded = None
        st.rerun()

sport_id = D.SPORTS[sport_label]

# ── Load fixtures ──────────────────────────────────────────────────────────────
loading = st.empty()
loading.markdown(STICKMAN_HTML, unsafe_allow_html=True)

tournaments = get_tournaments(sport_id)
def t_score(t):
    return ((t.get("upcomingFixtures") or 0) +
            (t.get("futureFixtures")   or 0) +
            (t.get("liveFixtures")     or 0))
# Try pinned tournaments first, then fall back to top tournaments by fixture count
pinned_ids = D.PINNED_TOURNAMENT_IDS
pinned = [t for t in tournaments if t.get("tournamentId") in pinned_ids]
others = sorted(
    [t for t in tournaments if t.get("tournamentId") not in pinned_ids],
    key=lambda t: (t.get("upcomingFixtures") or 0) + (t.get("futureFixtures") or 0),
    reverse=True
)

fixtures, seen_ids = [], set()
# Try pinned first, then top others until we have at least 5 fixtures
for t in pinned + others[:10]:
    tid = t.get("tournamentId")
    if tid:
        for fx in get_fixtures(tid):
            if fx["fixtureId"] not in seen_ids:
                fixtures.append(fx)
                seen_ids.add(fx["fixtureId"])
    if len(fixtures) >= 20:
        break

fixtures = sorted(fixtures, key=lambda f: f.get("start_ts", 0))
loading.empty()

if not fixtures:
    st.markdown('<div class="no-data">No upcoming fixtures found.</div>',
                unsafe_allow_html=True)
    st.stop()

# ── Fixture filter ─────────────────────────────────────────────────────────────
fixture_labels = ["All fixtures"] + [
    f"{fx['home']} v {fx['away']}  ·  {fx['start']}" for fx in fixtures
]
sel_fixture = st.selectbox("Fixture", fixture_labels, label_visibility="collapsed")

if sel_fixture != "All fixtures":
    idx = fixture_labels.index(sel_fixture) - 1
    scan_fixtures = [fixtures[idx]]
else:
    scan_fixtures = fixtures[:10]

# ── Scan ──────────────────────────────────────────────────────────────────────
def build_opportunities(scan_fixtures):
    opps = []
    seen = set()

    for fx in scan_fixtures:
        all_odds = get_odds(fx["fixtureId"])
        if not all_odds:
            continue

        groups = D.scan_all_markets(all_odds)

        # Batch fetch player names
        pids = {g["playerId"] for g in groups if g.get("playerId")}
        names = get_player_names(tuple(sorted(pids))) if pids else {}

        for g in groups:
            dedup = (fx["fixtureId"], g["marketId"],
                     g["outcomeId"], g.get("playerId", 0), g.get("handicap"))
            if dedup in seen:
                continue
            seen.add(dedup)

            # Build full outcome label
            outcome = g["outcome_label"]
            mid = g["marketId"]

            if g.get("playerId"):
                pname = names.get(g["playerId"], f"Player {g['playerId']}")
                outcome = f"{pname} — {outcome}"

            # For correct score, prefix with home team - away team context
            if mid == 10336:
                outcome = f"{fx['home']} {outcome} {fx['away']}"

            # Substitute real team names into generic labels
            h, a = fx['home'], fx['away']
            outcome = (outcome
                .replace("Home (DNB)",  f"{h} (DNB)")
                .replace("Away (DNB)",  f"{a} (DNB)")
                .replace("Home or Draw",f"{h} or Draw")
                .replace("Draw or Away",f"Draw or {a}")
                .replace("Home or Away",f"{h} or {a}")
                .replace("HT Home",     f"HT {h}")
                .replace("HT Away",     f"HT {a}")
                .replace("Home/Home",   f"{h}/{h}")
                .replace("Home/Draw",   f"{h}/Draw")
                .replace("Home/Away",   f"{h}/{a}")
                .replace("Draw/Home",   f"Draw/{h}")
                .replace("Draw/Away",   f"Draw/{a}")
                .replace("Away/Home",   f"{a}/{h}")
                .replace("Away/Draw",   f"{a}/Draw")
                .replace("Away/Away",   f"{a}/{a}")
            )

            opps.append({
                "fixtureId":  fx["fixtureId"],
                "match":      f"{fx['home']} v {fx['away']}",
                "start":      fx["start"],
                "market":     g["marketName"],
                "outcome":    outcome,
                "best_bm":    g["best_bm"],
                "best_price": g["best_price"],
                "avg_odds":   g["avg_odds"],
                "pct_above":  g["pct_above"],
                "bookmakers": g["bookmakers"],
                "is_player":  g.get("is_player", False),
            })

    return sorted(opps, key=lambda x: x["pct_above"], reverse=True)

scan_ph = st.empty()
scan_ph.markdown(STICKMAN_HTML, unsafe_allow_html=True)
all_opportunities = build_opportunities(scan_fixtures)
scan_ph.empty()

# ── Secondary filters ──────────────────────────────────────────────────────────
# Separate player props from match markets
player_opps = [o for o in all_opportunities if o.get("is_player")]
match_opps  = [o for o in all_opportunities if not o.get("is_player")]

f1, f2, f3, f4 = st.columns([2, 2, 1.5, 1.5])
with f1:
    mkt_opts = ["All Markets"] + sorted({o["market"] for o in all_opportunities})
    sel_market = st.selectbox("Market", mkt_opts, label_visibility="collapsed")
with f2:
    bm_opts = sorted({o["best_bm"] for o in all_opportunities})
    sel_bm = st.multiselect("Bookmakers", bm_opts, format_func=D.bm_label,
                            default=[], placeholder="All bookmakers",
                            label_visibility="collapsed")
with f3:
    # Line filter — relevant for player props
    line_opts = ["All Lines", "Over 0.5", "Over 1.5", "Over 2.5", "Over 3.5", "Over 4.5"]
    sel_line = st.selectbox("Line", line_opts, label_visibility="collapsed")
with f4:
    odds_opts = [1, 1.5, 2, 2.5, 3, 4, 5, 7.5, 10, 15, 20, 30, 50, "∞"]
    odds_raw = st.select_slider("Odds", options=odds_opts, value=(1, "∞"),
                                label_visibility="collapsed")
    lo = float(odds_raw[0])
    hi = float("inf") if odds_raw[1] == "∞" else float(odds_raw[1])

def apply_filters(opps):
    return [
        o for o in opps
        if (sel_market == "All Markets" or o["market"] == sel_market)
        and (not sel_bm or o["best_bm"] in sel_bm)
        and lo <= o["best_price"] <= hi
        and (sel_line == "All Lines" or o["outcome"].startswith(sel_line)
             or sel_line in o["outcome"])
    ]

opportunities      = apply_filters(all_opportunities)
match_opps_f       = apply_filters(match_opps)
player_opps_f      = apply_filters(player_opps)

# ── Metrics ────────────────────────────────────────────────────────────────────
m1, m2, m3, m4 = st.columns(4)
with m1: st.metric("Fixtures Scanned", len(scan_fixtures))
with m2: st.metric("Match Edges", len(match_opps_f))
with m3: st.metric("Player Props", len(player_opps_f))
with m4: st.metric("Best Edge", f"+{opportunities[0]['pct_above']:.1f}%" if opportunities else "—")

st.write("")

# ── Card render function ──────────────────────────────────────────────────────
def _render_card(opp, card_id):
    is_exp    = st.session_state.expanded == card_id
    bar_width = min(opp["pct_above"] * 4, 100)

    st.markdown(f"""
    <div class="pc">
        <div class="pc-accent"></div>
        <div class="pc-top">
            <div>
                <div class="pc-match">{opp['match']}</div>
                <div class="pc-meta">{opp['start']} &nbsp;·&nbsp;
                    <span class="mkt-tag">{opp['market']}</span></div>
            </div>
            <div>
                <div class="pc-edge">{f"+{opp['pct_above']:.1f}%" if opp['pct_above'] >= 1 else "—"}</div>
                <div class="pc-edge-sub">vs market avg</div>
            </div>
        </div>
        <div class="pc-bottom">
            <span class="outcome-tag">{opp['outcome']}</span>
            <span class="bookie-tag">{D.bm_label(opp['best_bm'])}</span>
            <span class="odds-tag">{opp['best_price']:.2f}</span>
            <span class="avg-tag">avg {opp['avg_odds']:.2f}</span>
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
        avg    = opp["avg_odds"]
        ranked = D.all_odds_ranked(opp["bookmakers"])
        best_p = ranked[0][1] if ranked else 0
        rows   = ""
        for bm, price in ranked:
            od_cls = "bm-odds-best" if price == best_p else "bm-odds"
            pct    = D.pct_above_avg(price, avg)
            if pct >= 0:
                diff_str, diff_cls = f"+{pct:.1f}%", "bm-above"
            else:
                diff_str, diff_cls = f"{pct:.1f}%", "bm-below"
            rows += (f'<div class="bm-row"><span class="bm-name">{D.bm_label(bm)}</span>'
                     f'<span class="{od_cls}">{price:.2f}</span>'
                     f'<span class="{diff_cls}">{diff_str}</span></div>')
        st.markdown(f"""
        <div class="xp-card">
            <div class="xp-title">{opp['outcome']} — {opp['match']}</div>
            <div style="margin-bottom:.5rem;font-family:'JetBrains Mono',monospace;
                 font-size:.65rem;color:#5a5a7a">Market average: {avg:.2f}</div>
            {rows}
        </div>
        """, unsafe_allow_html=True)

# ── Coverage expander ──────────────────────────────────────────────────────────
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
    missing = [b for b in D.ALL_BOOKMAKERS
               if b not in coverage and b not in D.EXCLUDED_FROM_BM]
    for bm in sorted(coverage, key=lambda b: -coverage[b]["odds"]):
        c = coverage[bm]
        st.markdown(
            f'<span style="font-family:JetBrains Mono,monospace;font-size:.72rem;color:#9a9ab0">'
            f'{D.bm_label(bm)}: {c["odds"]} odds · {c["props"]} player props</span>',
            unsafe_allow_html=True)
    if missing:
        st.markdown(
            f'<span style="font-family:JetBrains Mono,monospace;font-size:.72rem;color:#ff4d6d">'
            f'No data: {", ".join(D.bm_label(b) for b in missing)}</span>',
            unsafe_allow_html=True)

# ── Price feed ─────────────────────────────────────────────────────────────────
# ── Match market feed ─────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Best Prices — Match Markets</div>',
            unsafe_allow_html=True)

if not match_opps_f:
    st.markdown('<div class="no-data">No match market edges found.</div>',
                unsafe_allow_html=True)
else:
    for idx, opp in enumerate(match_opps_f[:10]):
        _render_card(opp, f"m_{idx}")

st.write("")

# ── Player props feed ──────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Player Props</div>',
            unsafe_allow_html=True)

if not player_opps_f:
    st.markdown('<div class="no-data">No player props found for these filters.</div>',
                unsafe_allow_html=True)
else:
    for idx, opp in enumerate(player_opps_f[:30]):
        _render_card(opp, f"p_{idx}")

# ── Dummy loop anchor (replaced above) ────────────────────────────────────────
if False:
    for idx, opp in enumerate(opportunities[:20]):
        card_id   = f"card_{idx}"
        is_exp    = st.session_state.expanded == card_id
        bar_width = min(opp["pct_above"] * 4, 100)

        st.markdown(f"""
        <div class="pc">
            <div class="pc-accent"></div>
            <div class="pc-top">
                <div>
                    <div class="pc-match">{opp['match']}</div>
                    <div class="pc-meta">{opp['start']} &nbsp;·&nbsp;
                        <span class="mkt-tag">{opp['market']}</span></div>
                </div>
                <div>
                    <div class="pc-edge">+{opp['pct_above']:.1f}%</div>
                    <div class="pc-edge-sub">above market avg</div>
                </div>
            </div>
            <div class="pc-bottom">
                <span class="outcome-tag">{opp['outcome']}</span>
                <span class="bookie-tag">{D.bm_label(opp['best_bm'])}</span>
                <span class="odds-tag">{opp['best_price']:.2f}</span>
                <span class="avg-tag">avg {opp['avg_odds']:.2f}</span>
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
            avg   = opp["avg_odds"]
            ranked = D.all_odds_ranked(opp["bookmakers"])
            best_p = ranked[0][1] if ranked else 0

            rows = ""
            for bm, price in ranked:
                od_cls = "bm-odds-best" if price == best_p else "bm-odds"
                pct    = D.pct_above_avg(price, avg)
                if price == best_p:
                    diff_str = f"+{pct:.1f}%"
                    diff_cls = "bm-above"
                elif pct >= 0:
                    diff_str = f"+{pct:.1f}%"
                    diff_cls = "bm-above"
                else:
                    diff_str = f"{pct:.1f}%"
                    diff_cls = "bm-below"
                rows += (f'<div class="bm-row">'
                         f'<span class="bm-name">{D.bm_label(bm)}</span>'
                         f'<span class="{od_cls}">{price:.2f}</span>'
                         f'<span class="{diff_cls}">{diff_str}</span>'
                         f'</div>')

            st.markdown(f"""
            <div class="xp-card">
                <div class="xp-title">{opp['outcome']} — {opp['match']}</div>
                <div style="margin-bottom:.5rem;font-family:'JetBrains Mono',monospace;
                     font-size:.65rem;color:#5a5a7a">
                    Market average: {avg:.2f}
                </div>{rows}
            </div>
            """, unsafe_allow_html=True)