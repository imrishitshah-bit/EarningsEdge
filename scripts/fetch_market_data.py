from scripts.config import supabase
from scripts.providers.market_data import get_historical_prices
def fetch_market_data(company_id: int, ticker: str):

    print(f"\nFetching {ticker}...")

    prices = get_historical_prices(ticker)

    if not prices:
        print(f"No data for {ticker}")
        return 0

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

    (
        supabase.table("market_data")
        .upsert(
            rows,
            on_conflict="company_id,trading_date",
        )
        .execute()
    )

    print(f"Stored {len(rows)} rows")

    return len(rows)

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

        try:

            stored = fetch_market_data(
                company["id"],
                company["ticker"],
            )

            total_rows += stored

        except Exception as e:

            print(f"Error for {company['ticker']}")
            print(e)

    print()
    print(f"Finished. Stored {total_rows} rows.")

if __name__ == "__main__":
    main()