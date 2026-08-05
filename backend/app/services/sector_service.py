from backend.app.database import supabase


def get_sector_rotation():
    """
    Returns sector rankings.
    """

    sectors = (
        supabase.table("sector_rotation")
        .select("*")
        .order("rank")
        .execute()
        .data
    )

    return sectors


def get_companies_by_sector(sector: str):
    """
    Returns all companies in a sector ordered by Edge Score.
    """

    print(f"\n========== DEBUG ==========")
    print(f"Requested sector: '{sector}'")

    companies = (
        supabase.table("companies")
        .select("*")
        .eq("sector", sector)
        .execute()
        .data
    )

    print(f"Companies returned: {len(companies)}")
    print(companies)

    scores = (
        supabase.table("scores")
        .select("*")
        .execute()
        .data
    )

    print(f"Scores returned: {len(scores)}")

    score_lookup = {
        score["company_id"]: score
        for score in scores
    }

    results = []

    for company in companies:

        score = score_lookup.get(company["id"])

        if score is None:
            print(
                f"No score found for "
                f"{company['ticker']} "
                f"(company_id={company['id']})"
            )
            continue

        results.append(
            {
                "ticker": company["ticker"],
                "company_name": company["company_name"],
                "sector": company["sector"],
                "industry": company["industry"],
                "logo_url": company["logo_url"],
                "score": score["ai_score"],
                "recommendation": score["recommendation"],
                "confidence": score["confidence"],
                "rank": score["rank"],
                "earnings_date": score["earnings_date"],
            }
        )

    results.sort(
        key=lambda x: x["score"] or 0,
        reverse=True,
    )

    print(f"Returning {len(results)} companies")
    print("===========================\n")

    return results