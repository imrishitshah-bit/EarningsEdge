from pathlib import Path
import yfinance as yf

# Create the output directory
output_dir = Path("data/raw")
output_dir.mkdir(parents=True, exist_ok=True)

ticker = "AMD"

print(f"Downloading {ticker} price history...")

data = yf.download(
    ticker,
    start="2018-01-01",
    progress=False,
    auto_adjust=False
)

output_file = output_dir / f"{ticker}.csv"
data.to_csv(output_file)

print(f"Downloaded {len(data)} rows.")
print(f"Saved to: {output_file}")