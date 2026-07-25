from backend.app.services.scoring.fundamental_score import fundamental_score
from backend.app.services.scoring.technical_score import technical_score
from backend.app.services.scoring.risk_score import risk_score
from backend.app.services.scoring.momentum_score import momentum_score
from backend.app.services.scoring.trend_score import trend_score
from backend.app.services.scoring.relative_strength import relative_strength_score


def calculate_score(company, earnings, market):
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

    # ----------------------------
    # Individual Scores
    # ----------------------------

    fundamental, f_reasons = fundamental_score(earnings)
    technical, t_reasons = technical_score(market)
    risk, r_reasons = risk_score(market)
    momentum, m_reasons = momentum_score(market)
    trend, trend_reasons = trend_score(market)
    relative_strength, rs_reasons = relative_strength_score(market)

    reasons.extend(f_reasons)
    reasons.extend(t_reasons)
    reasons.extend(r_reasons)
    reasons.extend(m_reasons)
    reasons.extend(trend_reasons)
    reasons.extend(rs_reasons)

    # ----------------------------
    # Normalize
    # ----------------------------

    fundamental_pct = (fundamental / 30) * 100
    technical_pct = (technical / 30) * 100
    risk_pct = (risk / 15) * 100
    momentum_pct = (momentum / 22) * 100
    trend_pct = (trend / 20) * 100
    relative_pct = (relative_strength / 10) * 100

    historical_pct = 50
    sentiment_pct = 50

    final_score = (
        fundamental_pct * 0.30 +
        technical_pct * 0.20 +
        momentum_pct * 0.15 +
        trend_pct * 0.10 +
        relative_pct * 0.05 +
        risk_pct * 0.10 +
        historical_pct * 0.05 +
        sentiment_pct * 0.05
    )

    final_score = round(max(0, min(100, final_score)))

    # ----------------------------
    # Confidence
    # ----------------------------

    if final_score >= 90:
        confidence = "Very High"
    elif final_score >= 80:
        confidence = "High"
    elif final_score >= 65:
        confidence = "Medium"
    elif final_score >= 50:
        confidence = "Low"
    else:
        confidence = "Very Low"

    # ----------------------------
    # Remove duplicate reasons
    # ----------------------------

    unique_reasons = []

    for reason in reasons:
        if reason not in unique_reasons:
            unique_reasons.append(reason)

    breakdown = {
        "fundamental": round(fundamental, 2),
        "technical": round(technical, 2),
        "momentum": round(momentum, 2),
        "trend": round(trend, 2),
        "relative_strength": round(relative_strength, 2),
        "risk": round(risk, 2),
        "historical": historical_pct,
        "sentiment": sentiment_pct,
    }

    return {
        "score": final_score,
        "confidence": confidence,
        "reasons": unique_reasons,
        "breakdown": breakdown,
    }