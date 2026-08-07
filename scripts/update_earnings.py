from scripts.config import supabase

from scripts.providers.earnings_calendar import get_upcoming_earnings

from scripts.create_company import create_company
from scripts.update_company_profiles import update_company_profile
from scripts.fetch_historical_earnings import fetch_historical_earnings
from scripts.fetch_market_data import fetch_market_data
from scripts.calculate_indicators import calculate_indicators
from scripts.upload_indicators import upload_indicators

from backend.app.services.scoring.update_scores import update_all_scores


def upsert_earnings(company_id: int, earning: dict):
    """
    Insert or update an upcoming earnings event.

    Session/timing is intentionally left as None for V1.
    Session data will be handled in V2.
    """

    earnings_data = {
        "company_id": company_id,
        "earnings_date": earning["date"],
        "session": None,
        "fiscal_quarter": earning.get("fiscalQuarter"),
        "fiscal_year": earning.get("fiscalYear"),
        "eps_estimate": earning.get("epsEstimated"),
        "revenue_estimate": earning.get("revenueEstimated"),
    }

    response = (
        supabase.table("earnings")
        .upsert(
            earnings_data,
            on_conflict="company_id,earnings_date",
        )
        .execute()
    )

    return response


def main():

    print("=" * 50)
    print("DOWNLOADING UPCOMING EARNINGS")
    print("=" * 50)

    earnings = get_upcoming_earnings()

    if not earnings:
        print("No upcoming earnings found.")
        return

    print(f"Downloaded {len(earnings)} earnings.\n")

    # -----------------------------------------
    # Load existing companies
    # -----------------------------------------

    companies = (
        supabase.table("companies")
        .select("id,ticker")
        .execute()
        .data
    )

    company_map = {
        company["ticker"].upper(): company["id"]
        for company in companies
    }

    existing_companies = 0
    new_companies = 0
    successful_earnings = 0

    # -----------------------------------------
    # Process earnings
    # -----------------------------------------

    for earning in earnings:

        ticker = earning["symbol"].upper()

        print("\n" + "=" * 50)
        print(ticker)
        print("=" * 50)

        company_id = company_map.get(ticker)

        # -----------------------------------------
        # Existing company
        # -----------------------------------------

        if company_id:

            existing_companies += 1

            print("Existing company")

            try:

                upsert_earnings(
                    company_id,
                    earning,
                )

                successful_earnings += 1

                print(
                    f"✓ Earnings uploaded: "
                    f"{earning['date']}"
                )

            except Exception as e:

                print(
                    f"✗ Failed earnings upload for {ticker}"
                )

                print(e)

            continue

        # -----------------------------------------
        # New company
        # -----------------------------------------

        print("New company discovered")

        new_companies += 1

        try:

            # Create company
            company_id = create_company(ticker)

            company_map[ticker] = company_id

            # Company profile
            update_company_profile(
                company_id,
                ticker,
            )

            # Historical earnings
            fetch_historical_earnings(
                company_id,
                ticker,
            )

            # Historical market data
            fetch_market_data(
                company_id,
                ticker,
            )

            # Technical indicators
            indicators = calculate_indicators(
                company_id,
                ticker,
            )

            if indicators is not None:
                upload_indicators(indicators)

            # Upcoming earnings
            upsert_earnings(
                company_id,
                earning,
            )

            successful_earnings += 1

            print(
                f"✓ Finished onboarding {ticker}"
            )

        except Exception as e:

            print(
                f"✗ Failed onboarding {ticker}"
            )

            print(e)

    # -----------------------------------------
    # Update Edge Scores
    # -----------------------------------------

    print("\n" + "=" * 50)
    print("UPDATING EDGE SCORES")
    print("=" * 50)

    try:

        update_all_scores()

    except Exception as e:

        print("✗ Failed to update Edge Scores")
        print(e)

    # -----------------------------------------
    # Summary
    # -----------------------------------------

    print("\n" + "=" * 50)
    print("UPDATE COMPLETE")
    print("=" * 50)

    print(
        f"Total earnings downloaded : {len(earnings)}"
    )

    print(
        f"Successful earnings uploads: "
        f"{successful_earnings}"
    )

    print(
        f"Existing companies         : "
        f"{existing_companies}"
    )

    print(
        f"New companies onboarded    : "
        f"{new_companies}"
    )

    print("=" * 50)


if __name__ == "__main__":
    main()