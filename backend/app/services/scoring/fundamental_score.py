def fundamental_score(earnings):
    score = 0
    reasons = []

    if earnings["eps_estimate"] is not None:
        if earnings["eps_estimate"] > 0:
            score += 15
            reasons.append("Positive EPS estimate")

    revenue = earnings["revenue_estimate"]

    if revenue is not None:
        if revenue > 100_000_000_000:
            score += 15
            reasons.append("Massive revenue estimate")
        elif revenue > 10_000_000_000:
            score += 10
            reasons.append("Strong revenue estimate")

    return score, reasons