from datetime import datetime

from backend.app.database import supabase
from backend.app.services.score_service import get_score


def update_all_scores():

    companies = (
        supabase.table("companies")
        .select("id,ticker")
        .execute()
        .data
    )

    print(f"Updating {len(companies)} companies...")

    rankings = []

    for company in companies:

        ticker = company["ticker"]

        try:

            score = get_score(ticker)

            if score is None:
                continue

            score["company_id"] = company["id"]

            rankings.append(score)

            print(f"✓ {ticker}")

        except Exception as e:

            print(f"✗ {ticker}: {e}")

    rankings.sort(
        key=lambda x: x["ai_score"],
        reverse=True,
    )

    for rank, stock in enumerate(rankings, start=1):

        supabase.table("scores").upsert({

            "company_id": stock["company_id"],
            "ticker": stock["ticker"],
            "company_name": stock["company_name"],

            "ai_score": stock["ai_score"],
            "rank": rank,

            "grade": stock["grade"],
            "confidence": stock["confidence"],
            "recommendation": stock["recommendation"],
            "risk_level": stock["risk_level"],

            "summary": stock["summary"],

            "strengths": stock["strengths"],
            "weaknesses": stock["weaknesses"],
            "reasons": stock["reasons"],
            "breakdown": stock["breakdown"],

            # NEW FIELDS
            "probability": stock["probability"],
            "expected_move": stock["expected_move"],
            "expected_move_confidence": stock["expected_move_confidence"],
            "bull_case": stock["bull_case"],
            "base_case": stock["base_case"],
            "bear_case": stock["bear_case"],
            "target_price": stock["target_price"],

            # Earnings
            "earnings_date": stock["earnings_date"],
            "eps_estimate": stock["eps_estimate"],
            "revenue_estimate": stock["revenue_estimate"],

            # JSON blobs
            "technical": stock["technical"],
            "historical": stock["historical"],

            "updated_at": datetime.utcnow().isoformat(),

        }).execute()

    print(f"\nFinished updating {len(rankings)} scores.")