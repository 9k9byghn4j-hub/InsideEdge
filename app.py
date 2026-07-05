import streamlit as st
from datetime import datetime
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

# ── Session state ──────────────────────────────────────────────────────────────
if "expanded" not in st.session_state:
    st.session_state.expanded = None

# ── Top bar ────────────────────────────────────────────────────────────────────
from datetime import timezone, timedelta
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

# ── Filters ────────────────────────────────────────────────────────────────────
STICKMAN_HTML = """
<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;
     padding:2rem;font-family:'JetBrains Mono',monospace;">
<style>
@keyframes head-nod {
    0%,100% { transform: translateY(0px) rotate(0deg); }
    20%     { transform: translateY(-14px) rotate(-8deg); }
    40%     { transform: translateY(-18px) rotate(0deg); }
    60%     { transform: translateY(-10px) rotate(6deg); }
    80%     { transform: translateY(-2px) rotate(0deg); }
}
@keyframes ball-arc {
    0%      { transform: translate(0px, 0px); opacity:1; }
    25%     { transform: translate(10px, -40px); opacity:1; }
    50%     { transform: translate(20px, -10px); opacity:1; }
    75%     { transform: translate(10px, -40px); opacity:1; }
    100%    { transform: translate(0px, 0px); opacity:1; }
}
@keyframes arm-l {
    0%,100% { transform: rotate(0deg); }
    40%     { transform: rotate(20deg); }
}
@keyframes arm-r {
    0%,100% { transform: rotate(0deg); }
    40%     { transform: rotate(-20deg); }
}
@keyframes body-sway {
    0%,100% { transform: rotate(0deg); }
    30%     { transform: rotate(-3deg); }
    70%     { transform: rotate(3deg); }
}
.sm-head  { animation: head-nod 1.2s ease-in-out infinite; transform-origin: 50px 105px; }
.sm-body  { animation: body-sway 1.2s ease-in-out infinite; transform-origin: 50px 115px; }
.sm-arml  { animation: arm-l 1.2s ease-in-out infinite; transform-origin: 50px 125px; }
.sm-armr  { animation: arm-r 1.2s ease-in-out infinite; transform-origin: 50px 125px; }
.sm-ball  { animation: ball-arc 1.2s ease-in-out infinite; }
</style>
<svg width="100" height="185" viewBox="0 0 100 185">
  <!-- ball arc -->
  <g class="sm-ball">
    <circle cx="50" cy="95" r="7" stroke="#00e5a0" stroke-width="2" fill="rgba(0,229,160,0.08)"/>
    <line x1="43" y1="91" x2="50" y2="88" stroke="#00e5a0" stroke-width="1" opacity="0.5"/>
    <line x1="57" y1="91" x2="50" y2="88" stroke="#00e5a0" stroke-width="1" opacity="0.5"/>
    <line x1="50" y1="95" x2="50" y2="102" stroke="#00e5a0" stroke-width="1" opacity="0.5"/>
  </g>
  <!-- head (nods up to meet ball) -->
  <g class="sm-head">
    <circle cx="50" cy="107" r="9" stroke="#00e5a0" stroke-width="2" fill="none"/>
    <!-- face dots -->
    <circle cx="47" cy="106" r="1" fill="#00e5a0"/>
    <circle cx="53" cy="106" r="1" fill="#00e5a0"/>
    <path d="M47 110 Q50 112 53 110" stroke="#00e5a0" stroke-width="1" fill="none"/>
  </g>
  <!-- body -->
  <g class="sm-body">
    <line x1="50" y1="116" x2="50" y2="148" stroke="#00e5a0" stroke-width="2"/>
    <!-- left arm -->
    <g class="sm-arml">
      <line x1="50" y1="125" x2="30" y2="140" stroke="#00e5a0" stroke-width="2"/>
    </g>
    <!-- right arm -->
    <g class="sm-armr">
      <line x1="50" y1="125" x2="70" y2="140" stroke="#00e5a0" stroke-width="2"/>
    </g>
    <!-- left leg -->
    <line x1="50" y1="148" x2="38" y2="170" stroke="#00e5a0" stroke-width="2"/>
    <line x1="38" y1="170" x2="33" y2="183" stroke="#00e5a0" stroke-width="2"/>
    <!-- right leg -->
    <line x1="50" y1="148" x2="62" y2="170" stroke="#00e5a0" stroke-width="2"/>
    <line x1="62" y1="170" x2="67" y2="183" stroke="#00e5a0" stroke-width="2"/>
  </g>
</svg>
<div style="margin-top:0.25rem;font-size:0.7rem;letter-spacing:0.15em;color:#5a5a7a">LOADING MARKETS...</div>
</div>
"""

f1, f2, f3, f4, f5 = st.columns([2, 2, 1.8, 1.5, 0.8])
with f1:
    sport_label = st.selectbox("Sport", list(D.SPORTS.keys()), label_visibility="collapsed")
with f2:
    all_bm = [b for b in D.ALL_BOOKMAKERS if b not in D.EXCLUDED_FROM_EV]
    sel_bm = st.multiselect("Bookmakers", options=all_bm, format_func=D.bm_label,
                             default=[], placeholder="All bookmakers",
                             label_visibility="collapsed")
with f3:
    market_options = ["All Markets"] + list(D.MARKETS.keys()) + list(D.PLAYER_MARKETS.keys())
    sel_market = st.selectbox("Market", market_options, label_visibility="collapsed")
with f4:
    odds_options = [1, 1.5, 2, 2.5, 3, 4, 5, 7.5, 10, 15, 20, 30, 50, "∞"]
    odds_raw = st.select_slider(
        "Odds",
        options=odds_options,
        value=(1, "∞"),
        label_visibility="collapsed",
    )
    lo_val = float(odds_raw[0])
    hi_val = float("inf") if odds_raw[1] == "∞" else float(odds_raw[1])
    odds_range = (lo_val, hi_val)
with f5:
    st.write("")
    if st.button("↻ Refresh"):
        st.cache_data.clear()
        st.session_state.expanded = None
        st.rerun()

sport_cfg = D.SPORTS[sport_label]

# ── Fetch fixtures ─────────────────────────────────────────────────────────────
@st.cache_data(ttl=120)
def get_fixtures(tid):
    return D.fetch_fixtures(tid)

fixtures_placeholder = st.empty()
fixtures_placeholder.markdown(STICKMAN_HTML, unsafe_allow_html=True)
fixtures = get_fixtures(sport_cfg["id"])
fixtures_placeholder.empty()

if not fixtures:
    st.markdown('<div class="no-data">No upcoming fixtures found.</div>', unsafe_allow_html=True)
    st.stop()

# ── Fetch odds per fixture (cached individually) ───────────────────────────────
@st.cache_data(ttl=60)
def get_odds(fid):
    return D.fetch_fixture_odds(fid)

# ── Build EV opportunities ─────────────────────────────────────────────────────
def build_opportunities(fixtures, sel_bm, sel_market):
    opps = []
    seen = set()

    # Limit to next 6 fixtures to keep load time fast
    for fx in fixtures[:6]:
        all_odds = get_odds(fx["fixtureId"])
        if not all_odds:
            continue
        home, away = fx["home"], fx["away"]

        # ── Match markets ──────────────────────────────────────────────────────
        for market_name, mdef in D.MARKETS.items():
            if sel_market not in ("All Markets", market_name):
                continue

            bm_odds, bf_probs = D.parse_market(all_odds, mdef, home, away)
            if not bf_probs:
                continue

            for outcome, bm_prices in bm_odds.items():
                true_prob = bf_probs.get(outcome)
                if not true_prob or not bm_prices:
                    continue

                dedup_key = (fx["fixtureId"], market_name, outcome)
                if dedup_key in seen:
                    continue
                seen.add(dedup_key)

                best_ev, best_bm, best_price = -999, None, None
                for bm, price in bm_prices.items():
                    if sel_bm and bm not in sel_bm:
                        continue
                    ev = D.calc_ev(true_prob, price)
                    if ev > best_ev:
                        best_ev, best_bm, best_price = ev, bm, price

                if best_bm is None:
                    continue
                if not sel_bm and best_ev <= 0:
                    continue

                opps.append({
                    "fixtureId":  fx["fixtureId"],
                    "match":      f"{home} v {away}",
                    "start":      fx["start"],
                    "market":     market_name,
                    "outcome":    outcome,
                    "best_bm":    best_bm,
                    "best_price": best_price,
                    "true_prob":  true_prob,
                    "ev":         best_ev,
                    "all_prices": bm_prices,
                    "benchmark":  "Betfair Exchange",
                })

        # ── Player prop markets ────────────────────────────────────────────────
        for market_name in D.PLAYER_MARKETS:
            if sel_market not in ("All Markets", market_name):
                continue

            props, _ = D.parse_player_props(all_odds, market_name)
            if not props:
                continue

            for prop in props:
                bm_prices = prop["bookmakers"]
                if len(bm_prices) < 2:
                    continue

                # Market average as true probability
                prices     = list(bm_prices.values())
                true_prob  = 1 / (sum(prices) / len(prices))

                pid        = prop["playerId"]
                line_str   = f" Over {prop['line']}" if prop.get("line") else ""
                outcome    = f"Player {pid}{line_str}"

                dedup_key  = (fx["fixtureId"], market_name, pid, prop["outcomeId"])
                if dedup_key in seen:
                    continue
                seen.add(dedup_key)

                best_ev, best_bm, best_price = -999, None, None
                for bm, price in bm_prices.items():
                    if sel_bm and bm not in sel_bm:
                        continue
                    ev = D.calc_ev(true_prob, price)
                    if ev > best_ev:
                        best_ev, best_bm, best_price = ev, bm, price

                if best_bm is None:
                    continue
                if not sel_bm and best_ev <= 0:
                    continue

                opps.append({
                    "fixtureId":  fx["fixtureId"],
                    "match":      f"{home} v {away}",
                    "start":      fx["start"],
                    "market":     market_name,
                    "outcome":    outcome,
                    "best_bm":    best_bm,
                    "best_price": best_price,
                    "true_prob":  true_prob,
                    "ev":         best_ev,
                    "all_prices": bm_prices,
                    "benchmark":  "Market Avg",
                })

    return sorted(opps, key=lambda x: x["ev"], reverse=True)

opps_placeholder = st.empty()
opps_placeholder.markdown(STICKMAN_HTML, unsafe_allow_html=True)
opportunities = build_opportunities(fixtures, set(sel_bm), sel_market)
opps_placeholder.empty()

# ── Metrics ────────────────────────────────────────────────────────────────────
pos_opps = [o for o in opportunities if o["ev"] > 0]
m1, m2, m3, m4 = st.columns(4)
with m1: st.metric("Fixtures Scanned", min(len(fixtures), 6))
with m2: st.metric("EV Opportunities", len(pos_opps))
with m3: st.metric("Best EV", f"+{pos_opps[0]['ev']*100:.1f}%" if pos_opps else "—")
with m4: st.metric("Markets Scanned", len(D.MARKETS) + len(D.PLAYER_MARKETS))

st.write("")

# ── EV Feed ────────────────────────────────────────────────────────────────────
label = (f"{D.bm_label(sel_bm[0])} Markets" if len(sel_bm) == 1
         else "Selected Bookmakers" if sel_bm
         else "Best Bets Right Now")
st.markdown(f'<div class="section-label">{label}</div>', unsafe_allow_html=True)

display_opps = [
    o for o in opportunities
    if odds_range[0] <= o["best_price"] <= odds_range[1]
][:20]

if not display_opps:
    st.markdown(
        '<div class="no-data">No opportunities found.<br>'
        '<span style="font-size:0.65rem">Try selecting a bookmaker or refreshing.</span></div>',
        unsafe_allow_html=True)
else:
    for opp in display_opps:
        card_id    = f"{opp['fixtureId']}_{opp['market']}_{opp['outcome']}"
        is_expanded = st.session_state.expanded == card_id
        ev_pct     = opp["ev"] * 100
        bar_width  = min(ev_pct * 5, 100)
        bm_imp     = 1 / opp["best_price"]
        edge       = opp["true_prob"] - bm_imp

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
                    ev_str = f"+{ev*100:.1f}%"
                    ev_cls = "bm-ev-pos"
                else:
                    ev_str = f"{ev*100:.1f}%"
                    ev_cls = "bm-ev-neg"
                rows_html += (
                    f'<div class="bm-row">'
                    f'<span class="bm-name">{D.bm_label(bm)}</span>'
                    f'<span class="{od_cls}">{price:.2f}</span>'
                    f'<span class="{ev_cls}">{ev_str}</span>'
                    f'</div>'
                )

            st.markdown(f"""
            <div class="expanded-card">
                <div class="expanded-title">{opp['outcome']} — {opp['market']} — {opp['match']}</div>
                <div style="margin-bottom:0.5rem;font-family:'JetBrains Mono',monospace;
                     font-size:0.65rem;color:#5a5a7a">
                    True prob ({opp['benchmark']}): {true_prob*100:.1f}%
                </div>
                {rows_html}
            </div>
            """, unsafe_allow_html=True)

st.write("")

# ── Match search ───────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Match Search</div>', unsafe_allow_html=True)
query = st.text_input("Search", placeholder="Type a team name — e.g. England, Brazil...",
                      label_visibility="collapsed")

if query.strip():
    matches = [fx for fx in fixtures
               if query.lower() in fx["home"].lower()
               or query.lower() in fx["away"].lower()]

    if not matches:
        st.markdown(f'<div style="color:#5a5a7a;font-family:JetBrains Mono,monospace;'
                    f'font-size:0.75rem;padding:0.5rem 0">No matches found for "{query}"</div>',
                    unsafe_allow_html=True)
    else:
        if len(matches) > 1:
            sel = st.selectbox("Select", [f"{m['home']} v {m['away']}" for m in matches],
                               label_visibility="collapsed")
            fx = next(m for m in matches if f"{m['home']} v {m['away']}" == sel)
        else:
            fx = matches[0]

        fx_opps = [o for o in opportunities
                   if o["fixtureId"] == fx["fixtureId"]
                   and o["ev"] > 0
                   and odds_range[0] <= o["best_price"] <= odds_range[1]]

        if not fx_opps:
            st.markdown('<div class="no-data">No positive EV opportunities for this fixture yet.</div>',
                        unsafe_allow_html=True)
        else:
            for opp in fx_opps[:10]:
                ev_pct    = opp["ev"] * 100
                bar_width = min(ev_pct * 5, 100)
                bm_imp    = 1 / opp["best_price"]
                st.markdown(f"""
                <div class="ev-card" style="margin-bottom:0.4rem;">
                    <div class="ev-card-accent"></div>
                    <div class="ev-card-top">
                        <div>
                            <div class="ev-card-match">{opp['outcome']}</div>
                            <div class="ev-card-meta">
                                <span class="market-tag">{opp['market']}</span>
                            </div>
                        </div>
                        <div style="text-align:right;flex-shrink:0;margin-left:1rem">
                            <div class="ev-badge">+{ev_pct:.1f}%</div>
                        </div>
                    </div>
                    <div class="ev-card-bottom">
                        <span class="bookie-tag">{D.bm_label(opp['best_bm'])}</span>
                        <span class="odds-tag">{opp['best_price']:.2f}</span>
                        <span class="prob-tag">True: {opp['true_prob']*100:.1f}%
                            &nbsp;·&nbsp; Implied: {bm_imp*100:.1f}%</span>
                    </div>
                    <div class="ev-bar-wrap">
                        <div class="ev-bar-fill" style="width:{bar_width}%"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)