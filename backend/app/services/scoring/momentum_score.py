def momentum_score(market):
    """
    Scores momentum (0-10)

    Rewards improving trends without requiring
    perfect technical conditions.
    """

    if market is None:
        return {
            "score": 0,
            "reasons": ["No momentum data"],
        }

    score = 0
    reasons = []

    close = market.get("close")
    sma20 = market.get("sma20")
    sma50 = market.get("sma50")
    macd = market.get("macd")
    rsi = market.get("rsi")

    # ---------------------------------
    # Price vs SMA20 (0-4)
    # ---------------------------------

    if close is not None and sma20 is not None:

        pct = (close - sma20) / sma20

        if pct > 0.05:
            score += 4
            reasons.append("Strong short-term momentum")

        elif pct > 0:
            score += 3
            reasons.append("Healthy short-term momentum")

        elif pct > -0.03:
            score += 2

        elif pct > -0.08:
            score += 1

    # ---------------------------------
    # Price vs SMA50 (0-2)
    # ---------------------------------

    if close is not None and sma50 is not None:

        pct = (close - sma50) / sma50

        if pct > 0.05:
            score += 2

        elif pct > -0.03:
            score += 1

    # ---------------------------------
    # MACD (0-2)
    # ---------------------------------

    if macd is not None:

        if macd > 2:
            score += 2

        elif macd > 0:
            score += 2

        elif macd > -1:
            score += 1

    # ---------------------------------
    # RSI (0-2)
    # ---------------------------------

    if rsi is not None:

        if 45 <= rsi <= 65:
            score += 2

        elif 35 <= rsi < 45:
            score += 1

        elif 65 < rsi <= 75:
            score += 1

        elif rsi > 85:
            score -= 1
            reasons.append("Momentum overheated")

    score = max(0, min(score, 10))

    return {
        "score": score,
        "reasons": reasons,
    }