def technical_score(market):
    """
    Technical Setup Score (0-100)

    Measures whether the stock has a healthy
    technical setup heading into earnings.
    """

    if market is None:
        return {
            "score": 50,
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
    # RSI (0-30)
    # ---------------------------------

    if rsi is not None:

        if 45 <= rsi <= 60:

            score += 30
            reasons.append("Healthy RSI")

        elif 60 < rsi <= 70:

            score += 24
            reasons.append("Strong momentum")

        elif 35 <= rsi < 45:

            score += 20

        elif 70 < rsi <= 80:

            score += 12
            reasons.append("Overbought")

        elif 25 <= rsi < 35:

            score += 10
            reasons.append("Oversold")

        else:

            score += 5
            reasons.append("Extreme RSI")

    # ---------------------------------
    # MACD (0-25)
    # ---------------------------------

    if macd is not None:

        if macd > 2:

            score += 25
            reasons.append("Strong bullish MACD")

        elif macd > 0:

            score += 20
            reasons.append("Bullish MACD")

        elif macd > -1:

            score += 12

        else:

            score += 5
            reasons.append("Bearish MACD")

    # ---------------------------------
    # Price vs SMA20 (0-20)
    # ---------------------------------

    if close and sma20:

        if close > sma20:

            score += 20

        else:

            score += 8
            reasons.append("Below 20-day average")

    # ---------------------------------
    # Price vs SMA50 (0-15)
    # ---------------------------------

    if close and sma50:

        if close > sma50:

            score += 15

        else:

            score += 5
            reasons.append("Below 50-day average")

    # ---------------------------------
    # Trend Alignment Bonus (0-10)
    # ---------------------------------

    if (
        close
        and sma20
        and sma50
    ):

        if close > sma20 > sma50:

            score += 10
            reasons.append("Strong uptrend")

        elif close > sma50:

            score += 5

    score = max(0, min(score, 100))

    return {
        "score": score,
        "reasons": reasons,
    }