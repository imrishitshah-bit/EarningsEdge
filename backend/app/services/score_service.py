from backend.app.database import supabase
from backend.app.services.scoring.final_score import calculate_score
from backend.app.services.report_builder import build_report


def get_score(ticker: str):
    # -----------------------------------
    # Company
    # -----------------------------------

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

    # -----------------------------------
    # Upcoming Earnings
    # -----------------------------------

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
            "confidence": "Very Low",
            "reasons": [
                "No upcoming earnings found."
            ],
        }

    earnings = earnings_result.data[0]

    # -----------------------------------
    # Latest Market Data
    # -----------------------------------

    market_rows = (
        supabase.table("market_data")
        .select("*")
        .eq("company_id", company["id"])
        .order("trading_date", desc=True)
        .limit(100)
        .execute()
        .data
    )

    market = None

    for row in market_rows:
        if (
            row["rsi"] is not None
            and row["macd"] is not None
            and row["sma20"] is not None
            and row["sma50"] is not None
            and row["volatility"] is not None
        ):
            market = row
            break

    if market is None:
        return {
            "ticker": company["ticker"],
            "company_name": company["company_name"],
            "ai_score": 50,
            "confidence": "Low",
            "reasons": [
                "Technical indicators have not been calculated yet."
            ],
            "technical": None,
            "earnings_date": earnings["earnings_date"],
            "eps_estimate": earnings["eps_estimate"],
            "revenue_estimate": earnings["revenue_estimate"],
        }

    # -----------------------------------
    # Calculate Score
    # -----------------------------------

    score_data = calculate_score(
        company,
        earnings,
        market,
    )

    technical = {
        "close": market["close"],
        "rsi": market["rsi"],
        "macd": market["macd"],
        "sma20": market["sma20"],
        "sma50": market["sma50"],
        "volatility": market["volatility"],
        "trading_date": market["trading_date"],
    }

    # -----------------------------------
    # Build Report
    # -----------------------------------

    report = build_report(
        company=company,
        earnings=earnings,
        technical=technical,
        ai_score=score_data["score"],
        confidence=score_data["confidence"],
        reasons=score_data["reasons"],
        breakdown=score_data["breakdown"],
    )

    return report