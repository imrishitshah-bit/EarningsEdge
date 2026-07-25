def trend_score(technical):
    if technical is None:
        return 0, ["No trend data"]

    score = 0
    reasons = []

    close = technical.get("close")
    sma20 = technical.get("sma20")
    sma50 = technical.get("sma50")

    if None not in (close, sma20, sma50):

        if close > sma20 > sma50:
            score += 20
            reasons.append("Strong bullish trend")

        elif close > sma20:
            score += 12
            reasons.append("Short-term uptrend")

        elif close > sma50:
            score += 8
            reasons.append("Long-term support")

    return score, reasons