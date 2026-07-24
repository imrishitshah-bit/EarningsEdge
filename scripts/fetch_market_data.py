from scripts.config import supabase
from scripts.providers.market_data import get_historical_prices


def main():
    companies = (
        supabase.table("companies")
        .select("id,ticker")
        .execute()
        .data
    )

    print(f"Found {len(companies)} companies")

    total_rows = 0

    for company in companies:
        ticker = company["ticker"]
        company_id = company["id"]

        print(f"\nFetching {ticker}...")

        try:
            prices = get_historical_prices(ticker)

            if not prices:
                print(f"No data for {ticker}")
                continue

            rows = []

            for price in prices:
                rows.append(
                    {
                        "company_id": company_id,
                        "trading_date": price["date"],
                        "open": price["open"],
                        "high": price["high"],
                        "low": price["low"],
                        "close": price["close"],
                        "volume": price["volume"],
                    }
                )

            result = (
                supabase.table("market_data")
                .upsert(
                    rows,
                    on_conflict="company_id,trading_date"
                )
                .execute()
            )

            print("Supabase returned:", result.data)

            total_rows += len(rows)

            print(f"Stored {len(rows)} rows")

        except Exception as e:
            print(f"Error for {ticker}")
            print(e)

    print(f"\nFinished. Attempted to store {total_rows} rows.")


if __name__ == "__main__":
    main()