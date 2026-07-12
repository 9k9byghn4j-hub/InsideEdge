import data as D

# marketId -> complete set of outcomeIds that make up that market.
# Only markets where every outcome is confirmed enumerable in data.py's
# OUTCOME_LABELS are included — Correct Score and player markets are too
# sparse across bookmakers for reliable arbitrage math.
ARB_ELIGIBLE_MARKETS = {
    101:    {101, 102, 103},        # Full Time Result
    104:    {104, 105},             # Both Teams to Score
    106:    {106, 107},             # Over/Under 0.5
    108:    {108, 109},             # Over/Under 1.5
    1010:   {1010, 1011},           # Over/Under 2.5
    1012:   {1012, 1013},           # Over/Under 3.5
    1014:   {1014, 1015},           # Over/Under 4.5
    1016:   {1016, 1017},           # Over/Under 5.5
    10214:  {10214, 10215},         # Draw No Bet
    10168:  {10168, 10169, 10170},  # Double Chance
    10799:  {10799, 10800, 10801},  # Half Time Result
}

MIN_MARGIN_PCT = 0.5  # ignore anything smaller — likely stale-price noise


def find_arbitrage(all_odds, min_margin_pct=MIN_MARGIN_PCT):
    """Scan one fixture's odds for arbitrage opportunities.

    Returns a list of dicts (sorted by margin desc), each with:
      marketId, implied_sum, margin_pct, outcomes: [
        {outcomeId, price, bookmaker, stake_pct}, ...
      ]
    stake_pct is each outcome's share of a total stake for equal profit
    regardless of result.
    """
    best_by_market = {}  # marketId -> {outcomeId: (price, bookmaker)}

    for bm, bm_odds in all_odds.items():
        if bm in D.EXCLUDED_FROM_BM:
            continue
        for odd in bm_odds.values():
            if not odd.get("active", True):
                continue
            mid = odd.get("marketId")
            required = ARB_ELIGIBLE_MARKETS.get(mid)
            if not required:
                continue
            oid = odd.get("outcomeId")
            if oid not in required:
                continue
            price = odd.get("price")
            if not price or price <= 1:
                continue
            slot = best_by_market.setdefault(mid, {})
            if oid not in slot or price > slot[oid][0]:
                slot[oid] = (price, bm)

    results = []
    for mid, best in best_by_market.items():
        required = ARB_ELIGIBLE_MARKETS[mid]
        if set(best.keys()) != required:
            continue  # incomplete coverage — can't compute a full-market arb

        implied_sum = sum(1 / price for price, _ in best.values())
        margin_pct = (1 - implied_sum) * 100
        if margin_pct < min_margin_pct:
            continue

        outcomes = [
            {
                "outcomeId": oid,
                "price": price,
                "bookmaker": bm,
                "stake_pct": (1 / price) / implied_sum,
            }
            for oid, (price, bm) in best.items()
        ]
        results.append({
            "marketId":    mid,
            "implied_sum": implied_sum,
            "margin_pct":  margin_pct,
            "outcomes":    outcomes,
        })

    return sorted(results, key=lambda r: r["margin_pct"], reverse=True)


def stake_split(opportunity, total_stake):
    """Given an opportunity from find_arbitrage() and a total stake amount,
    return (rows, profit) where rows adds 'stake'/'payout' to each outcome
    and profit is the guaranteed profit (same for every outcome)."""
    implied_sum = opportunity["implied_sum"]
    rows = []
    for o in opportunity["outcomes"]:
        stake = total_stake * o["stake_pct"]
        rows.append({**o, "stake": stake, "payout": stake * o["price"]})
    profit = total_stake * (1 - implied_sum) / implied_sum
    return rows, profit
