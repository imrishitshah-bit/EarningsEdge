from scripts.config import supabase
from scripts.providers.historical_earnings import get_historical_earnings
def fetch_historical_earnings(company_id: int, ticker: str):

    print(f"Fetching {ticker}...")

    earnings = get_historical_earnings(ticker)

    if not earnings:
        print("  No historical earnings")
        return False

    rows = []

    for item in earnings:

        eps_est = item.get("estimatedEps")
        eps_actual = item.get("actualEps")

        rev_est = item.get("estimatedRevenue")
        rev_actual = item.get("actualRevenue")

        rows.append(
            {
                "company_id": company_id,
                "earnings_date": item.get("date"),
                "fiscal_year": item.get("fiscalYear"),
                "fiscal_quarter": item.get("fiscalQuarter"),
                "eps_estimate": eps_est,
                "eps_actual": eps_actual,
                "revenue_estimate": rev_est,
                "revenue_actual": rev_actual,
                "eps_surprise": item.get("epsSurprise"),
                "revenue_surprise": item.get("revenueSurprise"),
                "beat_eps": (
                    eps_actual is not None
                    and eps_est is not None
                    and eps_actual > eps_est
                ),
                "beat_revenue": (
                    rev_actual is not None
                    and rev_est is not None
                    and rev_actual > rev_est
                ),
            }
        )

    (
        supabase.table("historical_earnings")
        .upsert(
            rows,
            on_conflict="company_id,earnings_date",
        )
        .execute()
    )

    print(f"  Stored {len(rows)} earnings")

    return len(rows)

def main():

    companies = (
        supabase.table("companies")
        .select("id,ticker")
        .execute()
        .data
    )

    print(f"Found {len(companies)} companies")

    total = 0

    for company in companies:

        try:

            stored = fetch_historical_earnings(
                company["id"],
                company["ticker"],
            )

            if stored:
                total += stored

        except Exception as e:

            print(e)

    print()
    print(f"Finished. Stored {total} earnings.")

if __name__ == "__main__":
    main()