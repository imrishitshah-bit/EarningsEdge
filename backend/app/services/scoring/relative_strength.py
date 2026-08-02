def relative_strength_score(market):
    """
    Scores relative strength (0-5)

    Temporary implementation using RSI until
    true performance vs SPY is added.
    """

    if market is None:
        return {
            "score": 0,
            "reasons": [],
        }

    rsi = market.get("rsi")

    if rsi is None:
        return {
            "score": 0,
            "reasons": [],
        }

    reasons = []

    if 55 <= rsi <= 65:

        score = 5
        reasons.append("Excellent relative strength")

    elif 45 <= rsi < 55:

        score = 4
        reasons.append("Healthy relative strength")

    elif 65 < rsi <= 75:

        score = 3
        reasons.append("Strong but extended")

    elif 35 <= rsi < 45:

        score = 3
        reasons.append("Average relative strength")

    elif 25 <= rsi < 35:

        score = 2

    else:

        score = 1
        reasons.append("Weak relative strength")

    return {
        "score": score,
        "reasons": reasons,
    }