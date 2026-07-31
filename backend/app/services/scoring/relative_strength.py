def relative_strength_score(market):
    """
    Scores relative strength (0-5)

    Uses RSI as a proxy until true relative
    performance vs SPY is implemented.
    """

    if market is None:
        return {
            "score": 0,
            "reasons": ["No relative strength data"],
        }

    rsi = market.get("rsi")

    if rsi is None:
        return {
            "score": 0,
            "reasons": ["Missing RSI"],
        }

    reasons = []

    if 55 <= rsi <= 65:

        score = 5
        reasons.append("Excellent relative strength")

    elif 48 <= rsi < 55:

        score = 4
        reasons.append("Healthy relative strength")

    elif 65 < rsi <= 75:

        score = 3
        reasons.append("Strong but extended")

    elif rsi > 75:

        score = 1
        reasons.append("Overextended")

    else:

        score = 2
        reasons.append("Weak relative strength")

    return {
        "score": score,
        "reasons": reasons,
    }