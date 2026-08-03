import yfinance as yf

ticker = yf.Ticker("AMD")

print(ticker.fast_info)
print()
print(ticker.info)