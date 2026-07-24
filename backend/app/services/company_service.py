from backend.app.database import supabase


def get_company(ticker: str):
    company = (
        supabase.table("companies")
        .select("*")
        .eq("ticker", ticker.upper())
        .single()
        .execute()
    )

    if not company.data:
        return None

    earnings = (
        supabase.table("earnings")
        .select("*")
        .eq("company_id", company.data["id"])
        .order("earnings_date", desc=True)
        .execute()
    )

    return {
        "company": company.data,
        "earnings": earnings.data,
    }