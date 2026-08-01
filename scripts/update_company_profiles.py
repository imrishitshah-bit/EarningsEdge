import requests

from scripts.config import supabase, FMP_API_KEY


BASE_URL = "https://financialmodelingprep.com/stable/profile"


def get_company_profile(symbol: str):
    url = (
        f"{BASE_URL}"
        f"?symbol={symbol}"
        f"&apikey={FMP_API_KEY}"
    )

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    data = response.json()

    if not isinstance(data, list) or len(data) == 0:
        return None

    return data[0]


def main():

    companies = (
        supabase.table("companies")
        .select("id,ticker")
        .execute()
        .data
    )

    print(f"Found {len(companies)} companies\n")

    updated = 0

    for company in companies:

        ticker = company["ticker"]

        print(f"Updating {ticker}...")

        try:

            profile = get_company_profile(ticker)

            if profile is None:
                print("No profile found.\n")
                continue

            (
                supabase.table("companies")
                .update(
                    {
                        "company_name": profile.get("companyName"),
                        "exchange": profile.get("exchangeShortName"),
                        "sector": profile.get("sector"),
                        "industry": profile.get("industry"),
                        "market_cap": profile.get("marketCap"),
                        "website": profile.get("website"),
                        "logo_url": profile.get("image"),
                        "country": profile.get("country"),
                        "currency": profile.get("currency"),
                        "description": profile.get("description"),
                    }
                )
                .eq("id", company["id"])
                .execute()
            )

            updated += 1

            print("✓ Updated\n")

        except Exception as e:

            print(f"✗ Failed: {e}\n")

    print("==============================")
    print(f"Finished! Updated {updated} companies.")
    print("==============================")


if __name__ == "__main__":
    main()