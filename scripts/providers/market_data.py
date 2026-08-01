import yfinance as yf


def get_historical_prices(symbol: str):
    """
    Download approximately 5 years of daily price history from Yahoo Finance.
    Returns data in the same format expected by fetch_market_data.py.
    """

    try:
        ticker = yf.Ticker(symbol)

        df = ticker.history(
            period="5y",
            interval="1d",
            auto_adjust=False,
        )

        if df.empty:
            print(f"No Yahoo Finance data for {symbol}")
            return []

        df = df.reset_index()

        prices = []

        for _, row in df.iterrows():

            prices.append(
                {
                    "date": row["Date"].strftime("%Y-%m-%d"),
                    "open": float(row["Open"]),
                    "high": float(row["High"]),
                    "low": float(row["Low"]),
                    "close": float(row["Close"]),
                    "volume": int(row["Volume"]),
                }
            )

        return prices

    except Exception as e:

        print(f"Yahoo Finance error for {symbol}: {e}")
        return []