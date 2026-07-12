import streamlit as st
import pandas as pd
import data as D
import watchlist as W
import theme

theme.setup_page("InsideEdge — Terminal")
theme.render_topbar("TERMINAL")
theme.require_api_key()

MATCH_MARKETS = ["Full Time Result", "Both Teams to Score", "Over/Under Goals",
                  "Double Chance", "Draw No Bet", "Half Time Result"]


@st.cache_data(ttl=120)
def get_odds(fid):
    return D.fetch_fixture_odds(fid)


@st.cache_data(ttl=3600)
def get_player_names(pids_tuple):
    return D.fetch_player_names(list(pids_tuple))


def _price_matrix(groups, row_label_fn):
    """Build a styled price grid: rows=outcome, columns=bookmaker.
    Streamlit's dataframe grid renders from the Styler's raw (unformatted)
    values, so NaN cells show as literal "None" if left to Styler.format —
    text and highlighting are computed separately here instead."""
    all_bms = sorted({bm for g in groups for bm in g["bookmakers"]}, key=D.bm_label)
    if not all_bms:
        return None
    rows = {}
    for g in groups:
        rows[row_label_fn(g)] = {D.bm_label(bm): price for bm, price in g["bookmakers"].items()}
    columns = [D.bm_label(bm) for bm in all_bms]
    numeric = pd.DataFrame.from_dict(rows, orient="index").reindex(columns=columns)
    display = numeric.map(lambda v: f"{v:.2f}" if pd.notna(v) else "—")
    row_max = numeric.max(axis=1)

    def _highlight(_):
        styles = pd.DataFrame("", index=numeric.index, columns=numeric.columns)
        for col in numeric.columns:
            styles.loc[numeric[col] == row_max, col] = "background-color: #0f3d2e"
        return styles

    return display.style.apply(_highlight, axis=None)


top = st.columns([5, 1])
with top[0]:
    st.markdown('<div class="section-label">Watchlist — Price Matrix</div>', unsafe_allow_html=True)
with top[1]:
    if st.button("↻ Refresh", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

pins = W.load_pins()

if not pins:
    st.markdown(
        '<div class="no-data">No fixtures pinned yet. Pin fixtures from the '
        'Scanner page to build your watchlist.</div>',
        unsafe_allow_html=True)
    st.stop()

loading = st.empty()
loading.markdown(theme.STICKMAN_HTML, unsafe_allow_html=True)

for fid, meta in sorted(pins.items(), key=lambda kv: kv[1].get("start", "")):

    hc1, hc2 = st.columns([5, 1])
    with hc1:
        st.markdown(
            f'<div class="pc-match">{meta.get("match", fid)}</div>'
            f'<div class="pc-meta">{meta.get("start", "")}</div>',
            unsafe_allow_html=True)
    with hc2:
        if st.button("✕ Unpin", key=f"unpin_{fid}"):
            W.unpin(fid)
            st.rerun()

    all_odds = get_odds(fid)
    if not all_odds:
        st.markdown('<div class="no-data">No odds available for this fixture.</div>',
                     unsafe_allow_html=True)
        st.write("")
        continue

    groups = D.scan_all_markets(all_odds, min_edge_pct=0)
    match_groups  = [g for g in groups if not g.get("is_player") and g["marketName"] in MATCH_MARKETS]
    player_groups = [g for g in groups if g.get("is_player")]

    if match_groups:
        styled = _price_matrix(match_groups, lambda g: f'{g["marketName"]}: {g["outcome_label"]}')
        if styled is not None:
            st.dataframe(styled, use_container_width=True)
    else:
        st.markdown('<div class="no-data">No match-market prices yet.</div>', unsafe_allow_html=True)

    if player_groups:
        pids  = {g["playerId"] for g in player_groups if g.get("playerId")}
        names = get_player_names(tuple(sorted(pids))) if pids else {}

        def _player_label(g):
            pname = names.get(g["playerId"], f'Player {g["playerId"]}')
            return f'{pname} — {g["marketName"]}: {g["outcome_label"]}'

        with st.expander(f"Player props ({len(player_groups)})", expanded=False):
            pstyled = _price_matrix(player_groups, _player_label)
            if pstyled is not None:
                st.dataframe(pstyled, use_container_width=True)

    st.write("")

loading.empty()
