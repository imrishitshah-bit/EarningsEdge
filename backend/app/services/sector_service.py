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

    companies = (
        supabase.table("companies")
        .select("*")
        .eq("sector", sector)
        .execute()
        .data
    )

    if not companies:
        return []

    scores = (
        supabase.table("scores")
        .select("*")
        .execute()
        .data
    )

    score_lookup = {
        score["company_id"]: score
        for score in scores
    }

    results = []

    for company in companies:

        score = score_lookup.get(company["id"])

        if not score:
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
        key=lambda x: x["score"],
        reverse=True,
    )

    return results