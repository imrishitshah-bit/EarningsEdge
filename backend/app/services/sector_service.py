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
    Returns all companies in a sector ordered by EarningsEdge Score.
    """

    companies = (
        supabase.table("companies")
        .select(
            """
            ticker,
            company_name,
            sector,
            scores (
                ai_score,
                recommendation,
                confidence,
                rank,
                earnings_date
            )
            """
        )
        .eq("sector", sector)
        .execute()
        .data
    )

    results = []

    for company in companies:

        if not company["scores"]:
            continue

        score = company["scores"][0]

        results.append(
            {
                "ticker": company["ticker"],
                "company_name": company["company_name"],
                "sector": company["sector"],
                "score": score["ai_score"],
                "recommendation": score["recommendation"],
                "confidence": score["confidence"],
                "rank": score["rank"],
                "earnings_date": score["earnings_date"],
            }
        )

    results.sort(
        key=lambda x: x["score"],
        reverse=True,
    )

    return results