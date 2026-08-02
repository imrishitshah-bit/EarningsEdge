def risk_score(market):
    """
    Risk Score (0-100)

    Scores volatility for earnings trading.

    Moderate volatility is preferred.
    Extremely low or extremely high
    volatility receives lower scores.
    """

    if market is None:
        return {
            "score": 50,
            "reasons": ["No volatility data"],
        }

    volatility = market.get("volatility")

    if volatility is None:

        return {
            "score": 50,
            "reasons": ["Missing volatility"],
        }

    reasons = []

    # ---------------------------------
    # Volatility
    # ---------------------------------

    if 0.30 <= volatility <= 0.50:

        score = 100
        reasons.append("Ideal earnings volatility")

    elif 0.20 <= volatility < 0.30:

        score = 90
        reasons.append("Low volatility")

    elif 0.50 < volatility <= 0.65:

        score = 80
        reasons.append("Higher volatility with good upside")

    elif 0.10 <= volatility < 0.20:

        score = 65
        reasons.append("Very stable")

    elif 0.65 < volatility <= 0.80:

        score = 55
        reasons.append("Elevated volatility")

    elif volatility > 0.80:

        score = 25
        reasons.append("Extremely volatile")

    else:

        score = 40
        reasons.append("Unusually low volatility")

    return {
        "score": score,
        "reasons": reasons,
    }