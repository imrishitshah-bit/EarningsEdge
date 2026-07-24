from config import supabase
from providers.fmp import get_upcoming_earnings, normalize_earnings

print("Fetching upcoming earnings...\n")

raw_earnings = get_upcoming_earnings()
print(f"Found {len(raw_earnings)} earnings events.\n")

processed = 0
failed = 0

for record in raw_earnings:
    company = normalize_earnings(record)

    try:
        # Insert or update company
        supabase.table("companies").upsert(
            {
                "ticker": company["ticker"],
                "company_name": company["company_name"],
            },
            on_conflict="ticker",
        ).execute()

        # Get company ID
        company_result = (
            supabase.table("companies")
            .select("id")
            .eq("ticker", company["ticker"])
            .single()
            .execute()
        )

        company_id = company_result.data["id"]

        # Insert or update earnings event
        supabase.table("earnings").upsert(
            {
                "company_id": company_id,
                "earnings_date": company["earnings_date"],
                "session": company["session"],
                "eps_estimate": company["eps_estimate"],
                "revenue_estimate": company["revenue_estimate"],
            },
            on_conflict="company_id,earnings_date",
        ).execute()

        processed += 1
        print(f"✓ {company['ticker']}")

    except Exception as e:
        failed += 1
        print(f"✗ {company['ticker']}")
        print(e)

print("\n==============================")
print("Earnings sync complete!")
print("==============================")
print(f"Processed : {processed}")
print(f"Failed    : {failed}")