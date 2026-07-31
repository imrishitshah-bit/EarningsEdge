from datetime import date, timedelta

from config import supabase
from providers.fmp import get_upcoming_earnings, normalize_earnings

# ----------------------------------------
# Determine earnings window
# ----------------------------------------

today = date.today()

# If it's Friday, Saturday or Sunday,
# start with next Monday.

if today.weekday() == 4:      # Friday
    start_date = today + timedelta(days=3)

elif today.weekday() == 5:    # Saturday
    start_date = today + timedelta(days=2)

elif today.weekday() == 6:    # Sunday
    start_date = today + timedelta(days=1)

else:
    start_date = today

end_date = start_date + timedelta(days=7)

print("================================")
print("Updating Earnings Calendar")
print("================================")
print(f"Window: {start_date} -> {end_date}\n")

# ----------------------------------------
# Remove old earnings
# ----------------------------------------

print("Cleaning old earnings...")

(
    supabase.table("earnings")
    .delete()
    .lt("earnings_date", start_date.isoformat())
    .execute()
)

# ----------------------------------------
# Download earnings
# ----------------------------------------

print("Fetching earnings from FMP...\n")

raw_earnings = get_upcoming_earnings()

print(f"Found {len(raw_earnings)} earnings events.\n")

processed = 0
failed = 0
skipped = 0

# ----------------------------------------
# Process earnings
# ----------------------------------------

for record in raw_earnings:

    company = normalize_earnings(record)

    earnings_date = date.fromisoformat(
        company["earnings_date"]
    )

    # Keep only earnings inside our window

    if not (start_date <= earnings_date <= end_date):
        skipped += 1
        continue

    try:

        # ------------------------------
        # Company
        # ------------------------------

        supabase.table("companies").upsert(
            {
                "ticker": company["ticker"],
                "company_name": company["company_name"],
            },
            on_conflict="ticker",
        ).execute()

        company_result = (
            supabase.table("companies")
            .select("id")
            .eq("ticker", company["ticker"])
            .single()
            .execute()
        )

        company_id = company_result.data["id"]

        # ------------------------------
        # Earnings
        # ------------------------------

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

        print(
            f"✓ {company['ticker']} ({company['earnings_date']})"
        )

    except Exception as e:

        failed += 1

        print(f"✗ {company['ticker']}")
        print(e)

# ----------------------------------------
# Summary
# ----------------------------------------

print("\n================================")
print("Earnings Sync Complete")
print("================================")
print(f"Processed : {processed}")
print(f"Skipped   : {skipped}")
print(f"Failed    : {failed}")
print("================================")