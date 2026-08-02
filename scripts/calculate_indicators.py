def calculate_score(company, earnings, market, history=None):
    """
    Calculates the final EarningsEdge Score (0-100)
    using weighted category scores.
    """
    from backend.app.services.scoring.expectation_score import expectation_score
    from backend.app.services.scoring.technical_score import technical_score
    from backend.app.services.scoring.momentum_score import momentum_score
    from backend.app.services.scoring.risk_score import risk_score
    from backend.app.services.scoring.historical_score import historical_score
    from backend.app.services.scoring.relative_strength_score import relative_strength_score
    reasons = []

    # ------------------------------------
    # Individual Modules
    # ------------------------------------

    business = expectation_score(company, earnings)
    historical = historical_score(history)
    technical = technical_score(market)
    momentum = momentum_score(market)
    risk = risk_score(market)
    relative = relative_strength_score(market)

    reasons.extend(business["reasons"])
    reasons.extend(historical["reasons"])
    reasons.extend(technical["reasons"])
    reasons.extend(momentum["reasons"])
    reasons.extend(risk["reasons"])
    reasons.extend(relative["reasons"])

    # ------------------------------------
    # Weighted Final Score
    # ------------------------------------

    weights = {
        "business": 0.25,
        "historical": 0.25,
        "technical": 0.20,
        "momentum": 0.15,
        "risk": 0.10,
        "relative": 0.05,
    }

    final_score = (
        business["score"] * weights["business"]
        + historical["score"] * weights["historical"]
        + technical["score"] * weights["technical"]
        + momentum["score"] * weights["momentum"]
        + risk["score"] * weights["risk"]
        + relative["score"] * weights["relative"]
    )

    final_score = round(final_score)

    # ------------------------------------
    # Confidence
    # ------------------------------------

    confidence_points = 100

    if history is None or len(history) < 4:
        confidence_points -= 20

    if market is None:
        confidence_points -= 20

    if earnings is None:
        confidence_points -= 20

    if confidence_points >= 90:
        confidence = "Very High"
    elif confidence_points >= 75:
        confidence = "High"
    elif confidence_points >= 60:
        confidence = "Medium"
    elif confidence_points >= 40:
        confidence = "Low"
    else:
        confidence = "Very Low"

    # ------------------------------------
    # Remove Duplicate Reasons
    # ------------------------------------

    unique_reasons = []

    for reason in reasons:
        if reason not in unique_reasons:
            unique_reasons.append(reason)

    # ------------------------------------
    # Breakdown
    # ------------------------------------

    breakdown = {
        "business_quality": business["score"],
        "historical": historical["score"],
        "technical": technical["score"],
        "momentum": momentum["score"],
        "risk": risk["score"],
        "relative_strength": relative["score"],
    }

    return {
        "score": final_score,
        "confidence": confidence,
        "reasons": unique_reasons,
        "breakdown": breakdown,
    }