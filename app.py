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

.ev-card { background:#12121a; border:1px solid #1e1e2e; border-radius:6px; padding:0.85rem 1rem; margin-bottom:0.5rem; position:relative; overflow:hidden; cursor:pointer; transition:border-color 0.15s; }
.ev-card:hover { border-color:#2e2e4e; }
.ev-card-accent { position:absolute; top:0; left:0; height:100%; background:linear-gradient(90deg,rgba(0,229,160,0.07),transparent); border-left:3px solid #00e5a0; pointer-events:none; }
.ev-card-top { display:flex; align-items:flex-start; justify-content:space-between; margin-bottom:0.4rem; }
.ev-card-match { font-size:0.82rem; font-weight:600; color:#e8e8f0; }
.ev-card-meta { font-family:'JetBrains Mono',monospace; font-size:0.62rem; color:#5a5a7a; margin-top:0.1rem; }
.ev-card-right { text-align:right; flex-shrink:0; margin-left:1rem; }
.ev-badge { font-family:'JetBrains Mono',monospace; font-size:0.9rem; font-weight:700; color:#00e5a0; }
.ev-card-bottom { display:flex; align-items:center; gap:0.6rem; margin-top:0.5rem; }
.outcome-tag { font-size:0.78rem; color:#c8c8e0; flex:1; }
.bookie-tag { font-family:'JetBrains Mono',monospace; font-size:0.63rem; background:#1e1e2e; color:#9a9ab0; padding:0.15rem 0.4rem; border-radius:3px; }
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
.bm-odds { font-family:'JetBrains Mono',monospace; font-size:0.8rem; font-weight:600; color:#e8e8f0; }
.bm-odds-best { color:#00e5a0; }
.bm-ev-pos { font-family:'JetBrains Mono',monospace; font-size:0.65rem; color:#00e5a0; min-width:3rem; text-align:right; }
.bm-ev-neg { font-family:'JetBrains Mono',monospace; font-size:0.65rem; color:#5a5a7a; min-width:3rem; text-align:right; }

.no-data { padding:2rem; text-align:center; color:#5a5a7a; font-family:'JetBrains Mono',monospace; font-size:0.75rem; border:1px dashed #1e1e2e; border-radius:6px; }

div[data-testid="stSelectbox"] > div > div { background:#12121a !important; border:1px solid #1e1e2e !important; color:#e8e8f0 !important; font-family:'JetBrains Mono',monospace !important; }
div[data-testid="stMultiSelect"] > div > div { background:#12121a !important; border:1px solid #1e1e2e !important; }
div[data-testid="stSlider"] > div { padding-top:0.25rem; }
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
now = datetime.utcnow().strftime("%d %b %Y  %H:%M UTC")
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
f1, f2, f3, f4 = st.columns([2, 2.5, 2, 0.8])
with f1:
    sport_label = st.selectbox("Sport", list(D.SPORTS.keys()), label_visibility="collapsed")
with f2:
    all_bm = [b for b in D.ALL_BOOKMAKERS if b not in D.EXCLUDED_FROM_EV]
    sel_bm = st.multiselect("Bookmakers", options=all_bm,
                             format_func=D.bm_label, default=[],
                             placeholder="All bookmakers",
                             label_visibility="collapsed")
with f3:
    market_options = ["All Markets"] + list(D.MARKETS.keys())
    sel_market = st.selectbox("Market", market_options, label_visibility="collapsed")
with f4:
    st.write("")
    if st.button("↻ Refresh"):
        st.cache_data.clear()
        st.session_state.expanded = None
        st.rerun()

min_ev = 0  # show all markets regardless of EV

sport_cfg = D.SPORTS[sport_label]

# ── Fetch fixtures ─────────────────────────────────────────────────────────────
@st.cache_data(ttl=120)
def get_fixtures(tid):
    return D.fetch_fixtures(tid)

with st.spinner(""):
    fixtures = get_fixtures(sport_cfg["id"])

if not fixtures:
    st.markdown('<div class="no-data">No upcoming fixtures found.</div>',
                unsafe_allow_html=True)
    st.stop()

# ── Fetch all odds and build EV opportunity list ───────────────────────────────
@st.cache_data(ttl=60)
def get_all_odds(fid):
    return D.fetch_fixture_odds(fid)

@st.cache_data(ttl=60)
def build_opportunities(fixtures_json):
    """Scan every fixture and every market for positive EV.
    Returns list of opportunity dicts, deduplicated by (fixture, market, outcome)."""
    import json
    fixtures = json.loads(fixtures_json)
    opps = []
    seen = set()  # (fixtureId, market_name, outcome)

    for fx in fixtures:
        all_odds = get_all_odds(fx["fixtureId"])
        if not all_odds:
            continue
        home, away = fx["home"], fx["away"]

        for market_name, mdef in D.MARKETS.items():
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

                # Find best EV across bookmakers
                best_ev, best_bm, best_price = -999, None, None
                for bm, price in bm_prices.items():
                    if sel_bm and bm not in sel_bm:
                        continue
                    ev = D.calc_ev(true_prob, price)
                    if ev > best_ev:
                        best_ev, best_bm, best_price = ev, bm, price

                if best_bm is None:
                    continue
                # When specific bookmakers selected, show all their markets
                # When no bookmaker filter, only show positive EV
                if not sel_bm and best_ev <= 0:
                    continue
                if sel_market != "All Markets" and market_name != sel_market:
                    continue

                opps.append({
                    "fixtureId":   fx["fixtureId"],
                    "match":       f"{home} v {away}",
                    "start":       fx["start"],
                    "market":      market_name,
                    "outcome":     outcome,
                    "best_bm":     best_bm,
                    "best_price":  best_price,
                    "true_prob":   true_prob,
                    "ev":          best_ev,
                    "all_prices":  bm_prices,
                })

    return sorted(opps, key=lambda x: x["ev"], reverse=True)

import json
with st.spinner("Scanning markets..."):
    opportunities = build_opportunities(json.dumps(fixtures))

# ── Metrics ────────────────────────────────────────────────────────────────────
pos_opps = [o for o in opportunities if o["ev"] > 0]
m1, m2, m3, m4 = st.columns(4)
with m1: st.metric("Fixtures", len(fixtures))
with m2: st.metric("Opportunities", len(opportunities))
with m3: st.metric("Best EV", f"+{pos_opps[0]['ev']*100:.1f}%" if pos_opps else "—")
with m4: st.metric("Markets Scanned", len(D.MARKETS))

st.write("")

# ── EV Feed ────────────────────────────────────────────────────────────────────
label_text = f"{D.bm_label(sel_bm[0])} Markets" if len(sel_bm) == 1 else ("Selected Bookmakers" if sel_bm else "Best Bets Right Now")
st.markdown(f'<div class="section-label">{label_text}</div>', unsafe_allow_html=True)

display_opps = opportunities[:20]

if not display_opps:
    st.markdown(
        '<div class="no-data">No positive EV opportunities found.<br>'
        '<span style="font-size:0.65rem">Try lowering the min EV filter or refreshing.</span></div>',
        unsafe_allow_html=True,
    )
else:
    for i, opp in enumerate(display_opps):
        card_id = f"{opp['fixtureId']}_{opp['market']}_{opp['outcome']}"
        is_expanded = st.session_state.expanded == card_id
        ev_pct     = opp["ev"] * 100
        bar_width  = min(ev_pct * 5, 100)
        bm_imp     = 1 / opp["best_price"]
        edge       = opp["true_prob"] - bm_imp

        # ── Card ──
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
                <div class="ev-card-right">
                    <div class="ev-badge">+{ev_pct:.1f}%</div>
                </div>
            </div>
            <div class="ev-card-bottom">
                <span class="outcome-tag">{opp['outcome']}</span>
                <span class="bookie-tag">{D.bm_label(opp['best_bm'])}</span>
                <span class="odds-tag">{opp['best_price']:.2f}</span>
                <span class="prob-tag">True: {opp['true_prob']*100:.1f}%
                    &nbsp;·&nbsp; Implied: {bm_imp*100:.1f}%
                    &nbsp;·&nbsp; Edge: +{edge*100:.1f}pp</span>
            </div>
            <div class="ev-bar-wrap">
                <div class="ev-bar-fill" style="width:{bar_width}%"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Expand button ──
        btn_label = "▲ Hide prices" if is_expanded else "▼ All bookmaker prices"
        if st.button(btn_label, key=f"exp_{card_id}"):
            st.session_state.expanded = None if is_expanded else card_id
            st.rerun()

        # ── Expanded view ──
        if is_expanded:
            true_prob   = opp["true_prob"]
            all_prices  = opp["all_prices"]
            ranked      = sorted(all_prices.items(), key=lambda x: x[1], reverse=True)
            best_price  = ranked[0][1] if ranked else 0

            rows_html = ""
            for bm, price in ranked:
                ev   = D.calc_ev(true_prob, price)
                sign = "+" if ev > 0 else ""
                ev_cls = "bm-ev-pos" if ev > 0 else "bm-ev-neg"
                odds_cls = "bm-odds-best" if price == best_price else "bm-odds"
                rows_html += (
                    f'<div class="bm-row">'
                    f'<span class="bm-name">{D.bm_label(bm)}</span>'
                    f'<span class="{odds_cls}">{price:.2f}</span>'
                    f'<span class="{ev_cls}">{sign}{ev*100:.1f}%</span>'
                    f'</div>'
                )

            st.markdown(f"""
            <div class="expanded-card">
                <div class="expanded-title">{opp['outcome']} — {opp['market']} — {opp['match']}</div>
                <div style="margin-bottom:0.4rem">
                    <span style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:#5a5a7a">
                        True prob (Betfair Exchange): {true_prob*100:.1f}%
                    </span>
                </div>
                {rows_html}
            </div>
            """, unsafe_allow_html=True)

st.write("")

# ── Match search ───────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Match Search</div>', unsafe_allow_html=True)
query = st.text_input("Search", placeholder="Type a team name — e.g. France, England, Brazil...",
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
        match_names = [f"{m['home']} v {m['away']}" for m in matches]
        if len(match_names) > 1:
            sel = st.selectbox("Select match", match_names, label_visibility="collapsed")
            fx = next(m for m in matches if f"{m['home']} v {m['away']}" == sel)
        else:
            fx = matches[0]
            st.markdown(f'<div style="font-family:JetBrains Mono,monospace;font-size:0.72rem;'
                        f'color:#5a5a7a;margin-bottom:0.5rem">'
                        f'{fx["home"]} v {fx["away"]} · {fx["start"]}</div>',
                        unsafe_allow_html=True)

        # Show EV opportunities for this fixture
        fx_opps = [o for o in opportunities if o["fixtureId"] == fx["fixtureId"] and o["ev"] > 0]

        if not fx_opps:
            st.markdown('<div class="no-data">No positive EV opportunities for this fixture.</div>',
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
                        <div class="ev-card-right">
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
