from backend.app.database import supabase
from backend.app.services.scoring.final_score import calculate_score


def get_score(ticker: str):
    # Get company
    company_result = (
        supabase.table("companies")
        .select("*")
        .eq("ticker", ticker.upper())
        .single()
        .execute()
    )

    if not company_result.data:
        return None

    company = company_result.data

    # Get the next earnings event
    earnings_result = (
        supabase.table("earnings")
        .select("*")
        .eq("company_id", company["id"])
        .order("earnings_date")
        .limit(1)
        .execute()
    )

    if not earnings_result.data:
        return {
            "ticker": company["ticker"],
            "company_name": company["company_name"],
            "ai_score": 0,
            "confidence": "Low",
            "reasons": [
                "No upcoming earnings found."
            ]
        }

    earnings = earnings_result.data[0]

    # Calculate AI score
    ai_score, confidence, reasons = calculate_score(earnings)

    return {
        "ticker": company["ticker"],
        "company_name": company["company_name"],
        "ai_score": ai_score,
        "confidence": confidence,
        "reasons": reasons,
        "earnings_date": earnings["earnings_date"],
        "eps_estimate": earnings["eps_estimate"],
        "revenue_estimate": earnings["revenue_estimate"],
    }