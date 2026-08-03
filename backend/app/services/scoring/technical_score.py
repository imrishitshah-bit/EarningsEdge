def technical_score(market):
    """
    Scores technical setup (0-100)

    Considers:
    - RSI
    - MACD
    - Trend vs moving averages

    Goal:
    Reward healthy technical setups without
    destroying companies that are temporarily
    pulling back.
    """

    if market is None:
        return {
            "score": 50,
            "reasons": [],
        }

    score = 50
    reasons = []

    rsi = market.get("rsi")
    macd = market.get("macd")
    sma20 = market.get("sma20")
    sma50 = market.get("sma50")
    close = market.get("close")

    # ---------------------------------
    # RSI
    # ---------------------------------

    if rsi is not None:

        if 50 <= rsi <= 65:
            score += 20
            reasons.append("Healthy RSI")

        elif 40 <= rsi < 50:
            score += 10

        elif 65 < rsi <= 75:
            score += 8
            reasons.append("Strong RSI")

        elif 30 <= rsi < 40:
            score -= 5

        elif rsi < 30:
            score -= 15
            reasons.append("Oversold")

        elif rsi > 80:
            score -= 15
            reasons.append("Extremely overbought")

    # ---------------------------------
    # MACD
    # ---------------------------------

    if macd is not None:

        if macd > 2:
            score += 15
            reasons.append("Strong bullish MACD")

        elif macd > 0:
            score += 8
            reasons.append("Bullish MACD")

        elif macd < -5:
            score -= 10
            reasons.append("Bearish MACD")

        elif macd < 0:
            score -= 5

    # ---------------------------------
    # Moving Averages
    # ---------------------------------

    if (
        close is not None
        and sma20 is not None
        and sma50 is not None
    ):

        if close > sma20:
            score += 8
        else:
            score -= 5

        if close > sma50:
            score += 8
        else:
            score -= 5

        if close > sma20 and close > sma50:
            reasons.append("Trading above key moving averages")

    score = max(0, min(score, 100))

    return {
        "score": score,
        "reasons": reasons,
    }