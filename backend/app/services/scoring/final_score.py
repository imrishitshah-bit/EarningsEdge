from backend.app.services.scoring.expectation_score import expectation_score
from backend.app.services.scoring.expectation_risk import expectation_risk
from backend.app.services.scoring.technical_score import technical_score
from backend.app.services.scoring.risk_score import risk_score
from backend.app.services.scoring.momentum_score import momentum_score
from backend.app.services.scoring.relative_strength_score import relative_strength_score
from backend.app.services.scoring.historical_score import historical_score


def calculate_score(company, earnings, market, history=None):
    """
    Returns:
    {
        score,
        confidence,
        reasons,
        breakdown
    }
    """

    reasons = []

    # ------------------------------------
    # Individual Scores
    # ------------------------------------

    expectation = expectation_score(company, earnings)
    expectation_risk_data = expectation_risk(
        company,
        market,
        earnings,
    )

    technical = technical_score(market)
    risk = risk_score(market)
    momentum = momentum_score(market)
    relative = relative_strength_score(market)
    historical = historical_score(history)

    expectation_score_value = expectation["score"]
    expectation_risk_value = expectation_risk_data["score"]
    technical_score_value = technical["score"]
    risk_score_value = risk["score"]
    momentum_score_value = momentum["score"]
    relative_score_value = relative["score"]
    historical_score_value = historical["score"]

    reasons.extend(expectation["reasons"])
    reasons.extend(expectation_risk_data["reasons"])
    reasons.extend(technical["reasons"])
    reasons.extend(risk["reasons"])
    reasons.extend(momentum["reasons"])
    reasons.extend(relative["reasons"])
    reasons.extend(historical["reasons"])

    # ------------------------------------
    # Sentiment
    # ------------------------------------

    sentiment_score = 5

    # ------------------------------------
    # Business Quality
    # ------------------------------------

    business_quality = (
        expectation_score_value
        + technical_score_value
        + historical_score_value
        + momentum_score_value
        + risk_score_value
        + relative_score_value
    )

    business_quality = min(95, business_quality)

    # ------------------------------------
    # Final Upside Score
    # ------------------------------------

    final_score = (
        business_quality
        - expectation_risk_value
        + sentiment_score
    )

    final_score = max(
        0,
        min(100, round(final_score))
    )

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
        "business_quality": business_quality,
        "expectation_risk": expectation_risk_value,
        "technical": technical_score_value,
        "historical": historical_score_value,
        "momentum": momentum_score_value,
        "risk": risk_score_value,
        "relative_strength": relative_score_value,
        "sentiment": sentiment_score,
    }

    # ------------------------------------
    # Return
    # ------------------------------------
    print("\n============================")
    print(company["ticker"])
    print("============================")
    print(f"Expectation      : {expectation_score_value}")
    print(f"Expectation Risk : {expectation_risk_value}")
    print(f"Technical        : {technical_score_value}")
    print(f"Historical       : {historical_score_value}")
    print(f"Momentum         : {momentum_score_value}")
    print(f"Risk             : {risk_score_value}")
    print(f"Relative Strength: {relative_score_value}")
    print(f"Sentiment        : {sentiment_score}")
    print(f"Business Quality : {business_quality}")
    print(f"Final Score      : {final_score}")
    print("============================")
    return {
        "score": final_score,
        "business_quality": business_quality,
        "expectation_risk": expectation_risk_value,
        "confidence": confidence,
        "reasons": unique_reasons,
        "breakdown": breakdown,
    }