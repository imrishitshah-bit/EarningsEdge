from datetime import date

from backend.app.database import supabase


def get_this_week_earnings(sector: str | None = None):

    today = date.today().isoformat()

    earnings = (
        supabase.table("earnings")
        .select("*")
        .gte("earnings_date", today)
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

        if sector and company.get("sector") != sector:
            continue

        results.append(
            {
                "ticker": company["ticker"],
                "company_name": company["company_name"],
                "sector": company.get("sector"),
                "industry": company.get("industry"),
                "logo_url": company.get("logo_url"),
                "earnings_date": earning["earnings_date"],
                "session": earning["session"],
                "eps_estimate": earning["eps_estimate"],
                "revenue_estimate": earning["revenue_estimate"],
            }
        )

    return results