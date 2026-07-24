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


companies = (
    supabase.table("companies")
    .select("id,ticker")
    .execute()
    .data
)

for company in companies:

    print(f"Processing {company['ticker']}")

    rows = (
        supabase.table("market_data")
        .select("*")
        .eq("company_id", company["id"])
        .order("trading_date")
        .execute()
        .data
    )

    if len(rows) < 50:
        continue

    df = pd.DataFrame(rows)

    df["close"] = df["close"].astype(float)

    df["rsi"] = calculate_rsi(df["close"])

    df["sma20"] = df["close"].rolling(20).mean()

    df["sma50"] = df["close"].rolling(50).mean()

    df["macd"] = calculate_macd(df["close"])

    df["volatility"] = (
        df["close"]
        .pct_change()
        .rolling(20)
        .std()
        * np.sqrt(252)
    )

    for _, row in df.iterrows():

        (
            supabase.table("market_data")
            .update(
                {
                    "rsi": None if pd.isna(row["rsi"]) else float(row["rsi"]),
                    "macd": None if pd.isna(row["macd"]) else float(row["macd"]),
                    "sma20": None if pd.isna(row["sma20"]) else float(row["sma20"]),
                    "sma50": None if pd.isna(row["sma50"]) else float(row["sma50"]),
                    "volatility": None if pd.isna(row["volatility"]) else float(row["volatility"]),
                }
            )
            .eq("id", int(row["id"]))
            .execute()
        )

print("Done.")