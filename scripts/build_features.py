from pathlib import Path
import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import MACD

# Input and output folders
input_dir = Path("data/raw/prices")
output_dir = Path("data/processed")
output_dir.mkdir(parents=True, exist_ok=True)

# Process every CSV
for file in input_dir.glob("*.csv"):

    print(f"Processing {file.name}")

    df = pd.read_csv(file)

    # Flatten multi-level columns if needed
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # Make sure Close is numeric
    df["Close"] = pd.to_numeric(df["Close"], errors="coerce")

    # Technical indicators
    df["RSI"] = RSIIndicator(df["Close"], window=14).rsi()

    macd = MACD(df["Close"])
    df["MACD"] = macd.macd()

    # Moving averages
    df["SMA20"] = df["Close"].rolling(20).mean()
    df["SMA50"] = df["Close"].rolling(50).mean()

    # Returns
    df["Return_20D"] = df["Close"].pct_change(20)

    # Volatility
    df["Volatility"] = df["Close"].rolling(20).std()

    # Save processed file
    df.to_csv(output_dir / file.name, index=False)

print("\nFinished processing all stocks!")