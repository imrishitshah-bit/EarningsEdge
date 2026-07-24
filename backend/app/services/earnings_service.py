from backend.app.database import supabase


def get_this_week_earnings():
    """
    Returns upcoming earnings joined with company information.
    """

    earnings = (
        supabase.table("earnings")
        .select("*")
        .order("earnings_date")
        .execute()
        .data
    )

    companies = (
        supabase.table("companies")
        .select("*")
        .execute()
        .data
    )

    company_lookup = {
        company["id"]: company
        for company in companies
    }

    results = []

    for earning in earnings:
        company = company_lookup.get(earning["company_id"])

        if not company:
            continue

        results.append({
            "ticker": company["ticker"],
            "company_name": company["company_name"],
            "earnings_date": earning["earnings_date"],
            "session": earning["session"],
            "eps_estimate": earning["eps_estimate"],
            "revenue_estimate": earning["revenue_estimate"],
        })

    return results