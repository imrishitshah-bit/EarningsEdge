import pandas as pd

from scripts.config import supabase


def _calculate_rsi(series: pd.Series, window: int = 14) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=window, min_periods=window).mean()
    avg_loss = loss.rolling(window=window, min_periods=window).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi


def _calculate_macd(series: pd.Series, fast: int = 12, slow: int = 26) -> pd.Series:
    fast_ema = series.ewm(span=fast, adjust=False).mean()
    slow_ema = series.ewm(span=slow, adjust=False).mean()
    return fast_ema - slow_ema


def calculate_indicators(company_id: int, ticker: str):
    """Calculate technical indicators for one company."""

    print(f"Calculating indicators for {ticker}...")

    rows = (
        supabase.table("market_data")
        .select("id,close,trading_date")
        .eq("company_id", company_id)
        .order("trading_date", desc=False)
        .execute()
        .data
    )

    if not rows:
        print(f"No market data found for {ticker}.")
        return None

    df = pd.DataFrame(rows)
    df = df.sort_values("trading_date")
    df = df[df["close"].notna()].copy()
    df["close"] = pd.to_numeric(df["close"], errors="coerce")

    df["rsi"] = _calculate_rsi(df["close"])
    df["macd"] = _calculate_macd(df["close"])
    df["sma20"] = df["close"].rolling(20).mean()
    df["sma50"] = df["close"].rolling(50).mean()
    df["volatility"] = df["close"].pct_change().rolling(20).std()

    return df[["id", "rsi", "macd", "sma20", "sma50", "volatility"]]


def main():
    """Calculate technical indicators for all companies and write them to indicator_updates.csv."""

    company_ids = (
        supabase.table("market_data")
        .select("company_id")
        .execute()
        .data
    )

    if not company_ids:
        print("No market_data rows found.")
        return None

    company_ids = sorted({row["company_id"] for row in company_ids if row.get("company_id") is not None})
    indicator_frames = []

    for company_id in company_ids:
        company = (
            supabase.table("companies")
            .select("ticker")
            .eq("id", company_id)
            .single()
            .execute()
            .data
        )

        ticker = company["ticker"] if company else str(company_id)
        indicators = calculate_indicators(company_id, ticker)

        if indicators is not None:
            indicator_frames.append(indicators)

    if not indicator_frames:
        print("No indicator rows were generated.")
        return None

    output_df = pd.concat(indicator_frames, ignore_index=True)
    output_df.to_csv("indicator_updates.csv", index=False)

    print(f"Wrote {len(output_df)} indicator rows to indicator_updates.csv")
    return output_df
