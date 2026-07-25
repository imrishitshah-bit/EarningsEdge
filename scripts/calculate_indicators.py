import numpy as np
import pandas as pd

from scripts.config import supabase


def calculate_rsi(close, period=14):
    delta = close.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss

    return 100 - (100 / (1 + rs))


def calculate_macd(close):
    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()

    return ema12 - ema26


def fetch_all_market_data(company_id):
    rows = []
    start = 0
    page_size = 1000

    while True:
        batch = (
            supabase.table("market_data")
            .select("*")
            .eq("company_id", company_id)
            .order("trading_date")
            .range(start, start + page_size - 1)
            .execute()
            .data
        )

        if not batch:
            break

        rows.extend(batch)

        print(f"    Loaded {len(rows)} rows...")

        if len(batch) < page_size:
            break

        start += page_size

    return rows


def main():
    companies = (
        supabase.table("companies")
        .select("id,ticker")
        .execute()
        .data
    )

    all_updates = []

    for company in companies:

        print(f"\nProcessing {company['ticker']}")

        rows = fetch_all_market_data(company["id"])

        print(f"Total rows: {len(rows)}")

        if len(rows) < 60:
            continue

        df = pd.DataFrame(rows)

        df["close"] = df["close"].astype(float)

        df["rsi"] = calculate_rsi(df["close"])
        df["macd"] = calculate_macd(df["close"])
        df["sma20"] = df["close"].rolling(20).mean()
        df["sma50"] = df["close"].rolling(50).mean()

        df["volatility"] = (
            df["close"]
            .pct_change()
            .rolling(20)
            .std()
            * np.sqrt(252)
        )

        updates = df[
            [
                "id",
                "rsi",
                "macd",
                "sma20",
                "sma50",
                "volatility",
            ]
        ]

        all_updates.append(updates)

    final_df = pd.concat(all_updates, ignore_index=True)

    final_df.to_csv("indicator_updates.csv", index=False)

    print()
    print(f"Saved {len(final_df)} indicator rows.")
    print("Done.")


if __name__ == "__main__":
    main()