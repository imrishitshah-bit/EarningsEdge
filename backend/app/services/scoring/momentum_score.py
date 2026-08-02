def momentum_score(market):
    """
    Momentum Score (0-100)

    Measures how strong the current trend is,
    independent of technical health.
    """

    if market is None:
        return {
            "score": 50,
            "reasons": ["No momentum data"],
        }

    score = 0
    reasons = []

    close = market.get("close")
    sma20 = market.get("sma20")
    sma50 = market.get("sma50")
    macd = market.get("macd")

    # ---------------------------------
    # Distance Above SMA20 (0-40)
    # ---------------------------------

    if close and sma20:

        pct = (close - sma20) / sma20

        if pct >= 0.10:

            score += 40
            reasons.append("Strong short-term trend")

        elif pct >= 0.05:

            score += 32

        elif pct >= 0:

            score += 24

        elif pct >= -0.05:

            score += 14

        else:

            score += 5
            reasons.append("Weak short-term trend")

    # ---------------------------------
    # Distance Above SMA50 (0-30)
    # ---------------------------------

    if close and sma50:

        pct = (close - sma50) / sma50

        if pct >= 0.20:

            score += 30
            reasons.append("Strong long-term trend")

        elif pct >= 0.10:

            score += 24

        elif pct >= 0:

            score += 18

        elif pct >= -0.05:

            score += 10

        else:

            score += 4
            reasons.append("Weak long-term trend")

    # ---------------------------------
    # MACD Strength (0-20)
    # ---------------------------------

    if macd is not None:

        if macd >= 5:

            score += 20

        elif macd >= 2:

            score += 16

        elif macd > 0:

            score += 12

        elif macd > -1:

            score += 8

        else:

            score += 3
            reasons.append("Negative momentum")

    # ---------------------------------
    # Trend Bonus (0-10)
    # ---------------------------------

    if (
        close
        and sma20
        and sma50
        and close > sma20 > sma50
    ):

        score += 10
        reasons.append("Trend fully aligned")

    score = max(0, min(score, 100))

    return {
        "score": score,
        "reasons": reasons,
    }