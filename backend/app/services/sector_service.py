from backend.app.database import supabase


def get_sector_rotation():
    """
    Returns sector rankings ordered by rank.
    """

    sectors = (
        supabase.table("sector_rotation")
        .select("*")
        .order("rank")
        .execute()
        .data
    )

    return sectors

raise Exception("NEW SECTOR SERVICE IS RUNNING")
def get_companies_by_sector(sector: str):
    """
    Returns all companies in a sector ordered by Edge Score.
    """

    # ------------------------------------
    # Load companies in requested sector
    # ------------------------------------

    companies = (
        supabase.table("companies")
        .select(
            "ticker,company_name,sector,industry,logo_url"
        )
        .eq("sector", sector)
        .execute()
        .data
    )

    if not companies:
        return []

    # ------------------------------------
    # Load scores
    # ------------------------------------

    scores = (
        supabase.table("scores")
        .select(
            """
            ticker,
            ai_score,
            recommendation,
            confidence,
            rank,
            earnings_date
            """
        )
        .execute()
        .data
    )

    # ------------------------------------
    # Match scores by ticker
    # ------------------------------------

    score_lookup = {
        score["ticker"]: score
        for score in scores
    }

    results = []

    for company in companies:

        score = score_lookup.get(company["ticker"])

        if score is None:
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

    # ------------------------------------
    # Highest score first
    # ------------------------------------

    results.sort(
        key=lambda x: x["score"] if x["score"] is not None else 0,
        reverse=True,
    )

    return results