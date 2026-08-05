import requests
import os

FMP_API_KEY = os.getenv("FMP_API_KEY")


def get_price(symbol: str, date: str):

    url = (
        f"https://financialmodelingprep.com/stable/"
        f"historical-price-eod/light"
        f"?symbol={symbol}"
        f"&from={date}"
        f"&to={date}"
        f"&apikey={FMP_API_KEY}"
    )

    response = requests.get(url, timeout=30)

    if response.status_code != 200:
        print(f"Failed to fetch price for {symbol} ({date})")
        return None

    data = response.json()

    if not isinstance(data, list):
        return None

    if len(data) == 0:
        return None

    return data[0]["close"]