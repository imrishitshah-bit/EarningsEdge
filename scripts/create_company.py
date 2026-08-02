from scripts.config import supabase


def create_company(ticker: str):

    ticker = ticker.upper()

    # Already exists?
    existing = (
        supabase.table("companies")
        .select("id")
        .eq("ticker", ticker)
        .execute()
    )

    if existing.data:
        return existing.data[0]["id"]

    # Create minimal company
    result = (
        supabase.table("companies")
        .insert(
            {
                "ticker": ticker,
                "company_name": ticker,
            }
        )
        .execute()
    )

    if not result.data:
        raise Exception(f"Failed to create company {ticker}")

    company_id = result.data[0]["id"]

    print(f"✓ Created {ticker}")

    return company_id