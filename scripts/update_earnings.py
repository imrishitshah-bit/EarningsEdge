from scripts.config import supabase

from scripts.providers.earnings_calendar import get_upcoming_earnings

from scripts.create_company import create_company

from scripts.update_company_profiles import update_company_profile

from scripts.fetch_historical_earnings import (
    fetch_historical_earnings,
)

from scripts.fetch_market_data import (
    fetch_market_data,
)

from scripts.calculate_indicators import (
    calculate_indicators,
)

from scripts.upload_indicators import (
    upload_indicators,
)

from backend.app.services.scoring.update_scores import (
    update_all_scores,
)


def upsert_earnings(company_id: int, earning: dict):

    (
        supabase.table("earnings")
        .upsert(
            {
                "company_id": company_id,
                "earnings_date": earning.get("date"),
                "session": earning.get("time"),
                "fiscal_quarter": earning.get("fiscalQuarter"),
                "fiscal_year": earning.get("fiscalYear"),
                "eps_estimate": earning.get("epsEstimated"),
                "revenue_estimate": earning.get("revenueEstimated"),
            },
            on_conflict="company_id,earnings_date",
        )
        .execute()
    )

def main():

    print("=" * 50)
    print("DOWNLOADING EARNINGS CALENDAR")
    print("=" * 50)

    earnings = get_upcoming_earnings()

    if not earnings:

        print("No upcoming earnings found.")
        return

    print(f"Downloaded {len(earnings)} earnings.\n")

    new_companies = 0
    existing_companies = 0

    companies = (
        supabase.table("companies")
        .select("id,ticker")
        .execute()
        .data
    )

    company_map = {
        c["ticker"].upper(): c["id"]
        for c in companies
    }

    for earning in earnings:

        ticker = earning.get("symbol", "").upper()

        if ticker == "":
            continue

        print(f"\n{'=' * 50}")
        print(ticker)
        print("=" * 50)

        company_id = company_map.get(ticker)

        if company_id:

            existing_companies += 1

            print("Existing company")

            upsert_earnings(
                company_id,
                earning,
            )

            continue

        new_companies += 1

        print("New company discovered")

        try:

            company_id = create_company(ticker)

            update_company_profile(
                company_id,
                ticker,
            )

            fetch_historical_earnings(
                company_id,
                ticker,
            )

            fetch_market_data(
                company_id,
                ticker,
            )

            indicators = calculate_indicators(
                company_id,
                ticker,
            )

            if indicators is not None:
                upload_indicators(indicators)

            upsert_earnings(
                company_id,
                earning,
            )

            company_map[ticker] = company_id

            print(f"Finished onboarding {ticker}")

        except Exception as e:

            print(f"Failed onboarding {ticker}")
            print(e)

        print("\n")
    print("=" * 50)
    print("UPDATING AI SCORES")
    print("=" * 50)

    update_all_scores()

    print("\n")
    print("=" * 50)
    print("UPDATE COMPLETE")
    print("=" * 50)
    print(f"Total earnings downloaded : {len(earnings)}")
    print(f"Existing companies        : {existing_companies}")
    print(f"New companies onboarded   : {new_companies}")
    print("=" * 50)

if __name__ == "__main__":
    main()