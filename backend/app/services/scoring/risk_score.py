def risk_score(market):
    """
    Scores risk (0-15)

    Lower volatility earns a higher score.
    Extremely volatile stocks receive
    significantly lower scores.
    """

    if market is None:
        return {
            "score": 5,
            "reasons": ["Missing market data"],
        }

    volatility = market.get("volatility")

    if volatility is None:

        return {
            "score": 5,
            "reasons": ["Missing volatility"],
        }

    reasons = []

    if volatility < 0.20:

        score = 15
        reasons.append("Extremely stable")

    elif volatility < 0.35:

        score = 12
        reasons.append("Low volatility")

    elif volatility < 0.50:

        score = 8
        reasons.append("Moderate volatility")

    elif volatility < 0.70:

        score = 5
        reasons.append("High volatility")

    else:

        score = 1
        reasons.append("Extremely volatile")

    return {
        "score": score,
        "reasons": reasons,
    }