def momentum_score(market):
    """
    Scores momentum (0-10)

    Rewards healthy trends but penalizes
    stocks that have become too extended.
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

    # -------------------------
    # Price vs SMA20
    # -------------------------

    if close and sma20:

        pct = (close - sma20) / sma20

        if 0 < pct <= 0.05:
            score += 4
            reasons.append("Healthy short-term momentum")

        elif 0.05 < pct <= 0.10:
            score += 3

        elif pct > 0.15:
            score -= 2
            reasons.append("Momentum extended")

    # -------------------------
    # Price vs SMA50
    # -------------------------

    if close and sma50:

        pct = (close - sma50) / sma50

        if 0 < pct <= 0.10:
            score += 2

        elif pct > 0.20:
            score -= 1

    # -------------------------
    # MACD
    # -------------------------

    if macd is not None:

        if macd > 2:
            score += 2

        elif macd > 0:
            score += 1

    # -------------------------
    # RSI
    # -------------------------

    if rsi is not None:

        if 50 <= rsi <= 60:
            score += 2

        elif 60 < rsi <= 70:
            score += 1

        elif rsi > 75:
            score -= 2
            reasons.append("Overextended momentum")

        elif rsi < 30:
            score -= 1

    score = max(0, min(score, 10))

    return {
        "score": score,
        "reasons": reasons,
    }