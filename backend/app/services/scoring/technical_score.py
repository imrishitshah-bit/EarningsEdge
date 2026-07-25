def technical_score(technical):
    score = 0
    reasons = []

    if technical is None:
        return 0, ["No technical data"]

    rsi = technical["rsi"]
    macd = technical["macd"]
    close = technical["close"]
    sma20 = technical["sma20"]
    sma50 = technical["sma50"]
    volatility = technical["volatility"]

    if rsi is not None:
        if 45 <= rsi <= 65:
            score += 8
            reasons.append("Healthy RSI")
        elif rsi < 30:
            score += 6
            reasons.append("Oversold")
        elif rsi > 75:
            score -= 4
            reasons.append("Overbought")

    if macd is not None and macd > 0:
        score += 8
        reasons.append("Bullish MACD")

    if sma20 is not None and close > sma20:
        score += 6
        reasons.append("Above SMA20")

    if sma50 is not None and close > sma50:
        score += 5
        reasons.append("Above SMA50")

    if volatility is not None:
        if volatility < 0.35:
            score += 3
            reasons.append("Stable price action")

    return max(score, 0), reasons