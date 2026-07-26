from datetime import date, timedelta

from backend.app.database import supabase
from backend.app.services.rankings_service import get_rankings


def get_dashboard():

    rankings = get_rankings()

    today = date.today()
    week = today + timedelta(days=7)

    earnings = (
        supabase.table("earnings")
        .select("""
            earnings_date,
            companies(
                ticker,
                company_name
            )
        """)
        .gte("earnings_date", str(today))
        .lte("earnings_date", str(week))
        .order("earnings_date")
        .execute()
        .data
    )

    earnings_today = [
        e for e in earnings
        if e["earnings_date"] == str(today)
    ]

    return {
        "top_picks": rankings[:10],
        "highest_scores": rankings[:25],
        "earnings_today": earnings_today,
        "earnings_this_week": earnings,
        "stats": {
            "companies": len(rankings),
            "earnings_this_week": len(earnings),
            "average_score": round(
                sum(r["ai_score"] for r in rankings) / len(rankings),
                1,
            ) if rankings else 0,
        },
    }