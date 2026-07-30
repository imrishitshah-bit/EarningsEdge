from backend.app.database import supabase
from backend.app.services.score_service import get_score


def update_all_scores():
    print("Loading companies...")

    companies = (
        supabase.table("companies")
        .select("id, ticker")
        .execute()
        .data
    )

    print(f"Found {len(companies)} companies.\n")

    rankings = []

    # ----------------------------
    # Calculate all scores
    # ----------------------------

    for company in companies:

        ticker = company["ticker"]

        try:
            score = get_score(ticker)

            if score is None:
                print(f"⚠ {ticker}: skipped (no score)")
                continue

            score["company_id"] = company["id"]
            rankings.append(score)

            print(f"✓ Scored {ticker} ({score['ai_score']})")

        except Exception as e:
            print(f"✗ {ticker} failed")
            print(e)
            continue

    if not rankings:
        print("\nNo scores generated.")
        return

    # ----------------------------
    # Rank companies
    # ----------------------------

    rankings.sort(
        key=lambda x: x["ai_score"],
        reverse=True,
    )

    print(f"\nSaving {len(rankings)} scores...\n")

    # ----------------------------
    # Save to Supabase
    # ----------------------------

    saved = 0

    for rank, stock in enumerate(rankings, start=1):

        try:

            payload = {
                "company_id": stock["company_id"],
                "ticker": stock["ticker"],
                "company_name": stock["company_name"],
                "ai_score": stock["ai_score"],
                "grade": stock["grade"],
                "confidence": stock["confidence"],
                "recommendation": stock["recommendation"],
                "risk_level": stock["risk_level"],
                "summary": stock["summary"],
                "strengths": stock["strengths"],
                "weaknesses": stock["weaknesses"],
                "reasons": stock["reasons"],
                "breakdown": stock["breakdown"],
                "earnings_date": stock["earnings_date"],
                "eps_estimate": stock["eps_estimate"],
                "revenue_estimate": stock["revenue_estimate"],
                "technical": stock["technical"],
                "historical": stock["historical"],
                "rank": rank,
            }

            (
                supabase.table("scores")
                .upsert(
                    payload,
                    on_conflict="ticker",
                )
                .execute()
            )

            saved += 1

            print(f"✓ Saved {stock['ticker']}")

        except Exception as e:

            print(f"✗ Failed to save {stock['ticker']}")
            print(e)

    print("\n==========================")
    print(f"Finished!")
    print(f"Companies scored : {len(rankings)}")
    print(f"Scores saved     : {saved}")
    print("==========================")