from datetime import datetime, timezone

from backend.app.database import supabase
from backend.app.services.score_service import get_score


def update_scores():

    # -----------------------------------------
    # Load Companies
    # -----------------------------------------

    companies = (
        supabase.table("companies")
        .select("id,ticker")
        .execute()
        .data
    )

    if not companies:
        print("No companies found.")
        return

    print(f"\nUpdating {len(companies)} companies...\n")

    company_lookup = {
        company["ticker"]: company["id"]
        for company in companies
    }

    rankings = []

    # -----------------------------------------
    # Calculate Scores
    # -----------------------------------------

    for company in companies:

        ticker = company["ticker"]

        try:

            score = get_score(ticker)

            # Skip failures
            if score is None:
                print(f"Skipping {ticker} (No score)")
                continue

            # Skip companies without upcoming earnings
            if "grade" not in score:
                print(f"Skipping {ticker} (No upcoming earnings)")
                continue

            rankings.append(score)

        except Exception as e:

            print(f"Failed {ticker}: {e}")

    # -----------------------------------------
    # Sort Rankings
    # -----------------------------------------

    rankings.sort(
        key=lambda x: x["ai_score"],
        reverse=True,
    )

    # -----------------------------------------
    # Save Scores
    # -----------------------------------------

    for rank, score in enumerate(rankings, start=1):

        company_id = company_lookup[score["ticker"]]

        data = {

            "company_id": company_id,

            "ticker": score["ticker"],
            "company_name": score["company_name"],

            "ai_score": score["ai_score"],
            "grade": score["grade"],

            "confidence": score["confidence"],
            "recommendation": score["recommendation"],
            "risk_level": score["risk_level"],

            "summary": score["summary"],

            "strengths": score["strengths"],
            "weaknesses": score["weaknesses"],
            "reasons": score["reasons"],

            "breakdown": score["breakdown"],

            "earnings_date": score["earnings_date"],
            "eps_estimate": score["eps_estimate"],
            "revenue_estimate": score["revenue_estimate"],

            "technical": score["technical"],
            "historical": score["historical"],

            "rank": rank,

            "updated_at": datetime.now(
                timezone.utc
            ).isoformat(),

        }

        supabase.table("scores").upsert(data).execute()

        print(
            f"{rank:>3}. "
            f"{score['ticker']:<6} "
            f"{score['ai_score']}/100"
        )

    print(f"\n✅ Updated {len(rankings)} companies successfully!")


if __name__ == "__main__":
    update_scores()

update_all_scores = update_scores
