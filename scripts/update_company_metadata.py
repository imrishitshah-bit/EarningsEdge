from scripts.config import supabase
from scripts.providers.company_profile import get_company_profile


def main():

    companies = (
        supabase.table("companies")
        .select("id,ticker")
        .execute()
        .data
    )

    print(f"Updating {len(companies)} companies...\n")

    updated = 0

    for company in companies:

        ticker = company["ticker"]

        try:

            profile = get_company_profile(ticker)

            if profile is None:
                print(f"⚠ No profile found for {ticker}")
                continue

            (
                supabase.table("companies")
                .update(
                    {
                        "company_name": profile.get("companyName"),
                        "exchange": profile.get("exchange"),
                        "sector": profile.get("sector"),
                        "industry": profile.get("industry"),
                        "market_cap": profile.get("marketCap"),
                        "website": profile.get("website"),
                        "logo_url": profile.get("image"),
                        "country": profile.get("country"),
                        "currency": profile.get("currency"),
                        "description": profile.get("description"),
                        "ceo": profile.get("ceo"),
                        "full_time_employees": profile.get("fullTimeEmployees"),
                        "ipo_date": profile.get("ipoDate"),
                    }
                )
                .eq("id", company["id"])
                .execute()
            )

            updated += 1
            print(f"✓ {ticker}")

        except Exception as e:

            print(f"✗ {ticker}")
            print(e)

    print("\n==============================")
    print(f"Updated {updated} companies.")
    print("==============================")


if __name__ == "__main__":
    main()