from backend.app.services.scoring import (
    company_size,
    eps,
    revenue,
    timing,
    upcoming,
)


def calculate_score(earnings):
    modules = [
        eps,
        revenue,
        timing,
        company_size,
        upcoming,
    ]

    total = 0
    reasons = []

    for module in modules:
        points, reason = module.score(earnings)

        total += points

        if points > 0:
            reasons.append(reason)

    if total >= 80:
        confidence = "High"
    elif total >= 60:
        confidence = "Medium"
    else:
        confidence = "Low"

    return total, confidence, reasons