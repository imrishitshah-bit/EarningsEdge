def technical_score(market):
    """
    Scores technical setup (0-15)

    Focuses on:
    - RSI
    - MACD
    - Trend above moving averages

    Penalizes:
    - Extremely overbought conditions
    """

    if market is None:
        return {
            "score": 0,
            "reasons": ["No technical data"],
        }

    score = 0
    reasons = []

    rsi = market.get("rsi")
    macd = market.get("macd")
    sma20 = market.get("sma20")
    sma50 = market.get("sma50")
    close = market.get("close")

    # -----------------------------
    # RSI
    # -----------------------------

    if rsi is not None:

        if 45 <= rsi <= 60:
            score += 6
            reasons.append("Healthy RSI")

        elif 60 < rsi <= 70:
            score += 4
            reasons.append("Strong RSI")

        elif 70 < rsi <= 80:
            score += 1
            reasons.append("Overbought")

        elif rsi > 80:
            score -= 5
            reasons.append("Extremely overbought")

        elif rsi < 30:
            score -= 3
            reasons.append("Oversold")

    # -----------------------------
    # MACD
    # -----------------------------

    if macd is not None:

        if macd > 2:
            score += 5
            reasons.append("Strong Bullish MACD")

        elif macd > 0:
            score += 3
            reasons.append("Bullish MACD")

    # -----------------------------
    # Trend
    # -----------------------------

    if (
        close is not None
        and sma20 is not None
        and sma50 is not None
    ):

        if close > sma20:
            score += 2

        if close > sma50:
            score += 3

        if close > sma20 and close > sma50:
            reasons.append("Trading above key moving averages")

    score = max(0, min(score, 15))

    return {
        "score": score,
        "reasons": reasons,
    }