from backend.app.database import supabase
from backend.app.services.score_service import get_score


def get_rankings():

    companies = (
        supabase.table("companies")
        .select("ticker")
        .execute()
        .data
    )

    rankings = []

    for company in companies:
        print(f"Scoring {company['ticker']}...")

        try:
            result = get_score(company["ticker"])

            if result:
                rankings.append(result)

        except Exception as e:
            print(f"FAILED {company['ticker']}: {e}")

    rankings.sort(
        key=lambda x: x["ai_score"],
        reverse=True
    )

    for i, stock in enumerate(rankings, start=1):
        stock["rank"] = i

    return rankings