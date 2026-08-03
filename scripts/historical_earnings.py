import requests
import os

FMP_API_KEY = os.getenv("FMP_API_KEY")


def get_historical_earnings(ticker: str):

    url = (
        f"https://financialmodelingprep.com/stable/"
        f"historical-earnings?symbol={ticker}"
        f"&apikey={FMP_API_KEY}"
    )

    response = requests.get(url, timeout=30)

    if response.status_code != 200:
        print(f"Failed to fetch historical earnings for {ticker}")
        return []

    data = response.json()

    if not isinstance(data, list):
        return []

    return data