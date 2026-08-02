def relative_strength_score(market):
    """
    Relative Strength Score (0-100)

    Uses RSI as a temporary proxy until true
    relative performance vs SPY is implemented.
    """

    if market is None:
        return {
            "score": 50,
            "reasons": ["No relative strength data"],
        }

    rsi = market.get("rsi")

    if rsi is None:
        return {
            "score": 50,
            "reasons": ["Missing RSI"],
        }

    reasons = []

    if 55 <= rsi <= 65:

        score = 100
        reasons.append("Excellent relative strength")

    elif 50 <= rsi < 55:

        score = 85
        reasons.append("Healthy relative strength")

    elif 65 < rsi <= 70:

        score = 80
        reasons.append("Strong momentum")

    elif 45 <= rsi < 50:

        score = 70

    elif 70 < rsi <= 80:

        score = 55
        reasons.append("Momentum becoming extended")

    elif 35 <= rsi < 45:

        score = 45
        reasons.append("Below-average relative strength")

    elif rsi < 35:

        score = 25
        reasons.append("Weak relative strength")

    else:

        score = 15
        reasons.append("Extremely overextended")

    return {
        "score": score,
        "reasons": reasons,
    }