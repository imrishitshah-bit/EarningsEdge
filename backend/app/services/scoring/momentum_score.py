def momentum_score(technical):
    if technical is None:
        return 0, ["No momentum data"]

    score = 0
    reasons = []

    close = technical.get("close")
    sma20 = technical.get("sma20")
    sma50 = technical.get("sma50")
    macd = technical.get("macd")
    rsi = technical.get("rsi")

    if close is not None and sma20 is not None:
        distance20 = (close - sma20) / sma20

        if distance20 > 0.05:
            score += 8
            reasons.append("Strong momentum above SMA20")
        elif distance20 > 0:
            score += 5
            reasons.append("Above SMA20")

    if close is not None and sma50 is not None:
        distance50 = (close - sma50) / sma50

        if distance50 > 0.10:
            score += 8
            reasons.append("Strong long-term trend")
        elif distance50 > 0:
            score += 5
            reasons.append("Above SMA50")

    if macd is not None and macd > 0:
        score += 6
        reasons.append("Bullish MACD")

    if rsi is not None:
        if 50 <= rsi <= 65:
            score += 8
            reasons.append("Healthy RSI")
        elif 40 <= rsi < 50:
            score += 5
            reasons.append("Recovering RSI")
        elif rsi > 75:
            score -= 5
            reasons.append("Overbought")

    return max(score, 0), reasons