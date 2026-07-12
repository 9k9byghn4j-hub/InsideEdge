import streamlit as st
import data as D
import arbitrage as A
import theme

theme.setup_page("InsideEdge — Arbitrage")
theme.render_topbar("ARBITRAGE")
theme.require_api_key()


@st.cache_data(ttl=3600)
def get_tournaments(sport_id):
    return D.fetch_tournaments(sport_id)


@st.cache_data(ttl=120)
def get_fixtures(tid):
    return D.fetch_fixtures(tid)


@st.cache_data(ttl=120)
def get_odds(fid):
    return D.fetch_fixture_odds(fid)


c1, c2, c3 = st.columns([3, 1.5, 1])
with c1:
    sport_label = st.selectbox("Sport", list(D.SPORTS.keys()), label_visibility="collapsed")
with c2:
    stake = st.number_input("Total stake (£)", min_value=10, value=100, step=10,
                             label_visibility="collapsed")
with c3:
    if st.button("↻ Scan", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

sport_id = D.SPORTS[sport_label]

loading = st.empty()
loading.markdown(theme.STICKMAN_HTML, unsafe_allow_html=True)

tournaments = get_tournaments(sport_id)
pinned_ids = D.PINNED_TOURNAMENT_IDS
pinned = [t for t in tournaments if t.get("tournamentId") in pinned_ids]
others = sorted(
    [t for t in tournaments if t.get("tournamentId") not in pinned_ids],
    key=lambda t: (t.get("upcomingFixtures") or 0) + (t.get("futureFixtures") or 0),
    reverse=True
)

fixtures, seen_ids = [], set()
for t in pinned + others[:10]:
    tid = t.get("tournamentId")
    if tid:
        for fx in get_fixtures(tid):
            if fx["fixtureId"] not in seen_ids:
                fixtures.append(fx)
                seen_ids.add(fx["fixtureId"])
    if len(fixtures) >= 20:
        break

fixtures = sorted(fixtures, key=lambda f: f.get("start_ts", 0))[:20]
loading.empty()

if not fixtures:
    st.markdown('<div class="no-data">No upcoming fixtures found.</div>', unsafe_allow_html=True)
    st.stop()

scan_ph = st.empty()
scan_ph.markdown(theme.STICKMAN_HTML, unsafe_allow_html=True)

all_opps = []
for fx in fixtures:
    all_odds = get_odds(fx["fixtureId"])
    if not all_odds:
        continue
    for opp in A.find_arbitrage(all_odds):
        opp["fixture"] = fx
        all_opps.append(opp)

all_opps.sort(key=lambda o: o["margin_pct"], reverse=True)
scan_ph.empty()

m1, m2 = st.columns(2)
with m1:
    st.metric("Fixtures Scanned", len(fixtures))
with m2:
    st.metric("Arb Opportunities", len(all_opps))

st.write("")
st.markdown('<div class="section-label">Arbitrage Opportunities</div>', unsafe_allow_html=True)

if not all_opps:
    st.markdown(
        '<div class="no-data">No arbitrage found across scanned fixtures right now — '
        'margins this tight are rare and close fast.</div>',
        unsafe_allow_html=True)
else:
    for opp in all_opps:
        fx = opp["fixture"]
        mkt_name, _, _ = D.MARKET_CONFIG.get(opp["marketId"], ("Unknown", False, False))
        rows, profit = A.stake_split(opp, stake)

        rows_html = ""
        for r in rows:
            label = D.substitute_team_names(
                D.OUTCOME_LABELS.get(r["outcomeId"], str(r["outcomeId"])),
                fx["home"], fx["away"])
            rows_html += (
                f'<div class="bm-row"><span class="bm-name">{label}</span>'
                f'<span class="bm-odds">{D.bm_label(r["bookmaker"])} @ {r["price"]:.2f}</span>'
                f'<span class="bm-above">£{r["stake"]:.2f} → £{r["payout"]:.2f}</span></div>'
            )

        st.markdown(f"""
        <div class="arb-card">
            <div class="pc-top">
                <div>
                    <div class="pc-match">{fx['home']} v {fx['away']}</div>
                    <div class="pc-meta">{fx['start']} &nbsp;·&nbsp;
                        <span class="mkt-tag">{mkt_name}</span></div>
                </div>
                <div>
                    <div class="arb-margin">+{opp['margin_pct']:.2f}%</div>
                    <div class="pc-edge-sub">profit £{profit:.2f} on £{stake:.0f}</div>
                </div>
            </div>
            {rows_html}
        </div>
        """, unsafe_allow_html=True)
