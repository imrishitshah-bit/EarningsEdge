def risk_score(technical):
    score = 15
    reasons = []

    if technical is None:
        return 5, ["Unknown risk"]

    vol = technical["volatility"]

    if vol is not None:
        if vol > 0.60:
            score -= 8
            reasons.append("Very volatile")
        elif vol > 0.40:
            score -= 4
            reasons.append("Moderate volatility")
        else:
            reasons.append("Low volatility")

    return max(score, 0), reasons