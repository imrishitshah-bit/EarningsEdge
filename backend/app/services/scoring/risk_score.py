def risk_score(market):
    """
    Scores risk (0-100)

    Higher score = more favorable risk profile.
    Volatility reduces the score but doesn't dominate it.
    """

    if market is None:
        return {
            "score": 50,
            "reasons": [],
        }

    volatility = market.get("volatility")

    if volatility is None:
        return {
            "score": 50,
            "reasons": [],
        }

    reasons = []

    if volatility < 0.20:

        score = 95
        reasons.append("Very stable")

    elif volatility < 0.35:

        score = 85
        reasons.append("Low volatility")

    elif volatility < 0.50:

        score = 70
        reasons.append("Moderate volatility")

    elif volatility < 0.70:

        score = 55
        reasons.append("Elevated volatility")

    elif volatility < 1.00:

        score = 40
        reasons.append("High volatility")

    else:

        score = 25
        reasons.append("Extremely volatile")

    return {
        "score": score,
        "reasons": reasons,
    }