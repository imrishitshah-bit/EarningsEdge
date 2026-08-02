def technical_score(market):
    """
    Scores technical setup (0-15)

    Uses:
    - RSI
    - MACD
    - Trend vs moving averages

    Rewards healthy technicals without
    being overly harsh.
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

    # ---------------------------------
    # RSI (0-6)
    # ---------------------------------

    if rsi is not None:

        if 45 <= rsi <= 60:
            score += 6
            reasons.append("Healthy RSI")

        elif 35 <= rsi < 45:
            score += 4
            reasons.append("Recovering RSI")

        elif 60 < rsi <= 70:
            score += 5
            reasons.append("Strong RSI")

        elif 25 <= rsi < 35:
            score += 2
            reasons.append("Oversold")

        elif 70 < rsi <= 80:
            score += 2
            reasons.append("Slightly overbought")

        elif rsi > 80:
            score -= 2
            reasons.append("Extremely overbought")

    # ---------------------------------
    # MACD (0-5)
    # ---------------------------------

    if macd is not None:

        if macd > 2:
            score += 5
            reasons.append("Strong Bullish MACD")

        elif macd > 0:
            score += 4
            reasons.append("Bullish MACD")

        elif macd > -1:
            score += 2

        elif macd > -3:
            score += 1

    # ---------------------------------
    # Trend (0-4)
    # ---------------------------------

    if (
        close is not None
        and sma20 is not None
        and sma50 is not None
    ):

        if close > sma20:
            score += 2

        elif close >= sma20 * 0.98:
            score += 1

        if close > sma50:
            score += 2

        elif close >= sma50 * 0.98:
            score += 1

        if close > sma20 and close > sma50:
            reasons.append("Trading above key moving averages")

    score = max(0, min(score, 15))

    return {
        "score": score,
        "reasons": reasons,
    }