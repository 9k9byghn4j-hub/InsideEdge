import streamlit as st
import data as D
import watchlist as W
import theme

theme.setup_page()
STICKMAN_HTML = theme.STICKMAN_HTML

# ── Session state ──────────────────────────────────────────────────────────────
if "expanded" not in st.session_state:
    st.session_state.expanded = None

# ── Top bar ────────────────────────────────────────────────────────────────────
theme.render_topbar()
theme.require_api_key()

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
# ── Top controls ──────────────────────────────────────────────────────────────
c1, c2, c3 = st.columns([3, 1, 1])
with c1:
    sport_label = st.selectbox("Sport", list(D.SPORTS.keys()),
                               label_visibility="collapsed")
with c2:
    st.write("")
    refresh_clicked = st.button("↻ Refresh Odds", use_container_width=True)
with c3:
    st.write("")
    apply_clicked = st.button("✓ Apply Filters", use_container_width=True)

sport_id = D.SPORTS[sport_label]

if refresh_clicked:
    st.cache_data.clear()
    st.session_state.expanded = None
    st.session_state.pop("filtered_opps", None)
    st.rerun()

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
            outcome = D.substitute_team_names(outcome, fx['home'], fx['away'])

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

# ── Filters — applied only on button click ─────────────────────────────────────
st.markdown('<div class="section-label">Filters</div>', unsafe_allow_html=True)
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
    line_opts = ["All Lines", "Over 0.5", "Over 1.5", "Over 2.5", "Over 3.5", "Over 4.5"]
    sel_line = st.selectbox("Line", line_opts, label_visibility="collapsed")
with f4:
    odds_opts = [1, 1.5, 2, 2.5, 3, 4, 5, 7.5, 10, 15, 20, 30, 50, "∞"]
    odds_raw = st.select_slider("Odds", options=odds_opts, value=(1, "∞"),
                                label_visibility="collapsed")
    lo = float(odds_raw[0])
    hi = float("inf") if odds_raw[1] == "∞" else float(odds_raw[1])

# Only filter when Apply Filters clicked — store in session state
if apply_clicked:
    def _filter(opps):
        return [
            o for o in opps
            if (sel_market == "All Markets" or o["market"] == sel_market)
            and (not sel_bm or o["best_bm"] in sel_bm)
            and lo <= o["best_price"] <= hi
            and (sel_line == "All Lines"
                 or sel_line in o["outcome"]
                 or o["outcome"].startswith(sel_line))
        ]
    st.session_state["filtered_opps"] = _filter(all_opportunities)
    st.session_state["filter_desc"] = (
        f"Market: {sel_market}  ·  "
        f"Bookmakers: {', '.join(D.bm_label(b) for b in sel_bm) if sel_bm else 'All'}  ·  "
        f"Line: {sel_line}  ·  "
        f"Odds: {lo}–{'∞' if hi == float('inf') else hi}"
    )

# Use filtered results if available, else show all
if "filtered_opps" in st.session_state:
    opportunities = st.session_state["filtered_opps"]
    if "filter_desc" in st.session_state:
        st.markdown(
            f'<div style="font-family:JetBrains Mono,monospace;font-size:0.65rem;'
            f'color:#5a5a7a;margin-bottom:0.75rem">Filtered: {st.session_state["filter_desc"]}</div>',
            unsafe_allow_html=True)
else:
    opportunities = all_opportunities

match_opps_f  = [o for o in opportunities if not o.get("is_player")]
player_opps_f = [o for o in opportunities if o.get("is_player")]

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

    bc1, bc2 = st.columns([4, 1])
    with bc1:
        btn = "▲ Hide prices" if is_exp else "▼ All bookmaker prices"
        if st.button(btn, key=f"btn_{card_id}"):
            st.session_state.expanded = None if is_exp else card_id
            st.rerun()
    with bc2:
        pinned = W.is_pinned(opp["fixtureId"])
        if st.button("📌 Pinned" if pinned else "📌 Pin", key=f"pin_{card_id}"):
            if pinned:
                W.unpin(opp["fixtureId"])
            else:
                W.pin(opp["fixtureId"], {"match": opp["match"], "start": opp["start"]})
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