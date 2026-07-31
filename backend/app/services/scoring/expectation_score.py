def expectation_score(company, earnings):
    """
    Scores business quality (0-25)

    This is NOT trying to predict the stock reaction.

    It only answers:

    "Is this fundamentally a high-quality business?"
    """

    score = 0
    reasons = []

    eps = earnings.get("eps_estimate")
    revenue = earnings.get("revenue_estimate")
    market_cap = company.get("market_cap")

    # -----------------------
    # EPS Quality
    # -----------------------

    if eps is not None:

        if eps >= 5:
            score += 10
            reasons.append("Excellent profitability")

        elif eps >= 2:
            score += 8
            reasons.append("Strong profitability")

        elif eps > 0:
            score += 6
            reasons.append("Profitable business")

        else:
            score += 1
            reasons.append("Expected quarterly loss")

    # -----------------------
    # Revenue Quality
    # -----------------------

    if revenue is not None:

        if revenue >= 50_000_000_000:

            score += 5
            reasons.append("Large, established business")

        elif revenue >= 10_000_000_000:

            score += 4
            reasons.append("Strong revenue base")

        elif revenue >= 2_000_000_000:

            score += 3
            reasons.append("Healthy revenue")

        elif revenue >= 500_000_000:

            score += 2

        else:

            score += 1

    # -----------------------
    # Company Size
    # -----------------------

    if market_cap is not None:

        if market_cap >= 500_000_000_000:

            score += 3
            reasons.append("Mega-cap stability")

        elif market_cap >= 100_000_000_000:

            score += 4
            reasons.append("Large-cap quality")

        elif market_cap >= 20_000_000_000:

            score += 5
            reasons.append("Healthy large business")

        elif market_cap >= 5_000_000_000:

            score += 4
            reasons.append("Growing mid-cap")

        else:

            score += 2
            reasons.append("Small-cap")

    # -----------------------
    # Profitability Bonus
    # -----------------------

    if (
        eps is not None
        and revenue is not None
    ):

        if eps > 0 and revenue > 10_000_000_000:

            score += 3
            reasons.append("Consistently profitable")

    score = min(score, 25)

    return {
        "score": score,
        "reasons": reasons,
    }