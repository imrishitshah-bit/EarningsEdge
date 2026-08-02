def expectation_score(company, earnings):
    """
    Business Quality Score (0-100)

    Measures how fundamentally strong and established
    the company appears based on currently available data.
    """

    score = 0
    reasons = []

    market_cap = company.get("market_cap")
    eps = earnings.get("eps_estimate")
    revenue = earnings.get("revenue_estimate")

    # ---------------------------------
    # Market Cap (0-30)
    # ---------------------------------

    if market_cap is not None:

        if market_cap >= 500_000_000_000:
            score += 30
            reasons.append("Mega-cap stability")

        elif market_cap >= 100_000_000_000:
            score += 27
            reasons.append("Large-cap company")

        elif market_cap >= 25_000_000_000:
            score += 23
            reasons.append("Established large company")

        elif market_cap >= 10_000_000_000:
            score += 18
            reasons.append("Strong mid-cap")

        elif market_cap >= 2_000_000_000:
            score += 12
            reasons.append("Growing business")

        else:
            score += 6
            reasons.append("Small-cap company")

    # ---------------------------------
    # EPS Estimate (0-20)
    # ---------------------------------

    if eps is not None:

        if eps > 5:
            score += 20
            reasons.append("Very strong expected earnings")

        elif eps > 2:
            score += 18
            reasons.append("Strong expected earnings")

        elif eps > 0:
            score += 15
            reasons.append("Expected to remain profitable")

        else:
            score += 5
            reasons.append("Expected quarterly loss")

    # ---------------------------------
    # Revenue Estimate (0-20)
    # ---------------------------------

    if revenue is not None:

        if revenue >= 100_000_000_000:
            score += 20

        elif revenue >= 25_000_000_000:
            score += 18

        elif revenue >= 10_000_000_000:
            score += 16

        elif revenue >= 2_000_000_000:
            score += 12

        elif revenue >= 500_000_000:
            score += 8

        else:
            score += 5

    # ---------------------------------
    # Company Metadata (0-30)
    # ---------------------------------

    metadata_fields = [
        "sector",
        "industry",
        "website",
        "description",
        "exchange",
        "country",
    ]

    metadata_score = 0

    for field in metadata_fields:

        if company.get(field):
            metadata_score += 5

    metadata_score = min(metadata_score, 30)

    score += metadata_score

    if metadata_score >= 25:
        reasons.append("Complete company profile")

    elif metadata_score >= 15:
        reasons.append("Well-documented business")

    # ---------------------------------

    score = min(score, 100)

    return {
        "score": score,
        "reasons": reasons,
    }