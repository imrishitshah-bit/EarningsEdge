from pathlib import Path
import pandas as pd
import yfinance as yf
import time

# Create output folder
output_dir = Path("data/raw/prices")
output_dir.mkdir(parents=True, exist_ok=True)

print("Getting S&P 500 companies...")

# We'll start with a small test list
tickers = [
    "AAPL",
    "MSFT",
    "NVDA",
    "AMD",
    "META",
    "AMZN",
    "GOOGL",
    "TSM",
    "AVGO",
    "MU"
]
# Yahoo Finance uses '-' instead of '.'
tickers = [ticker.replace(".", "-") for ticker in tickers]

print(f"Found {len(tickers)} companies.\n")

success = 0
failed = []

for i, ticker in enumerate(tickers, start=1):
    print(f"[{i}/{len(tickers)}] Downloading {ticker}...")

    try:
        df = yf.download(
            ticker,
            start="2018-01-01",
            progress=False,
            auto_adjust=False,
        )

        if len(df) > 0:
            df.to_csv(output_dir / f"{ticker}.csv")
            success += 1
        else:
            failed.append(ticker)

    except Exception:
        failed.append(ticker)

    # Be nice to Yahoo's servers
    time.sleep(0.25)

print("\nDownload complete!")
print(f"Successful: {success}")
print(f"Failed: {len(failed)}")

if failed:
    print("\nFailed tickers:")
    print(failed)