def build_report(
    company,
    earnings,
    technical,
    ai_score,
    confidence,
    reasons,
    breakdown,
):
    # -------------------------
    # Grade
    # -------------------------

    if ai_score >= 95:
        grade = "A+"
    elif ai_score >= 90:
        grade = "A"
    elif ai_score >= 85:
        grade = "A-"
    elif ai_score >= 80:
        grade = "B+"
    elif ai_score >= 75:
        grade = "B"
    elif ai_score >= 70:
        grade = "B-"
    elif ai_score >= 65:
        grade = "C+"
    elif ai_score >= 60:
        grade = "C"
    else:
        grade = "D"

    # -------------------------
    # Recommendation
    # -------------------------

    if ai_score >= 90:
        recommendation = "Strong Buy Before Earnings"
    elif ai_score >= 80:
        recommendation = "Buy Before Earnings"
    elif ai_score >= 70:
        recommendation = "Watch Closely"
    elif ai_score >= 60:
        recommendation = "Neutral"
    else:
        recommendation = "Avoid"

    # -------------------------
    # Risk
    # -------------------------

    risk_level = "Medium"

    if technical:
        volatility = technical.get("volatility")

        if volatility is not None:
            if volatility < 0.30:
                risk_level = "Low"
            elif volatility > 0.60:
                risk_level = "High"

    # -------------------------
    # Strengths / Weaknesses
    # -------------------------

    strengths = []
    weaknesses = []

    positive_words = [
        "bullish",
        "positive",
        "strong",
        "above",
        "healthy",
        "stable",
        "low volatility",
    ]

    for reason in reasons:
        if any(word in reason.lower() for word in positive_words):
            strengths.append(reason)
        else:
            weaknesses.append(reason)

    # -------------------------
    # Summary
    # -------------------------

    summary = (
        f"{company['ticker']} has an AI Score of {ai_score}/100 with "
        f"{confidence.lower()} confidence. "
        f"The stock currently shows {len(strengths)} positive signals "
        f"and {len(weaknesses)} cautionary signals heading into earnings. "
        f"Recommendation: {recommendation}."
    )

    return {
        "ticker": company["ticker"],
        "company_name": company["company_name"],

        "ai_score": ai_score,
        "grade": grade,
        "confidence": confidence,

        "recommendation": recommendation,
        "risk_level": risk_level,

        "summary": summary,

        "strengths": strengths,
        "weaknesses": weaknesses,

        "reasons": reasons,

        "breakdown": breakdown,

        "earnings_date": earnings["earnings_date"] if earnings else None,
        "eps_estimate": earnings["eps_estimate"] if earnings else None,
        "revenue_estimate": earnings["revenue_estimate"] if earnings else None,

        "technical": technical,
    }