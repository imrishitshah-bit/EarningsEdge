def risk_score(market):
    """
    Scores risk (0-10)

    Moderate volatility is preferred for earnings trades.
    Extremely high volatility is penalized.
    Extremely low volatility gets a small penalty because
    expected moves are often limited.
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

        score = 5
        reasons.append("Very low volatility")

    elif volatility < 0.35:

        score = 8
        reasons.append("Stable volatility")

    elif volatility < 0.55:

        score = 10
        reasons.append("Ideal earnings volatility")

    elif volatility < 0.75:

        score = 8
        reasons.append("Elevated volatility")

    elif volatility < 1.00:

        score = 5
        reasons.append("High volatility")

    else:

        score = 2
        reasons.append("Extremely volatile")

    return {
        "score": score,
        "reasons": reasons,
    }