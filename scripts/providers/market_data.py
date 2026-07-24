import requests

from scripts.config import FMP_API_KEY


BASE_URL = "https://financialmodelingprep.com/stable/historical-price-eod/full"


def get_historical_prices(symbol: str):
    url = (
        f"{BASE_URL}"
        f"?symbol={symbol}"
        f"&apikey={FMP_API_KEY}"
    )

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    data = response.json()

    if not isinstance(data, list):
        return []

    return data