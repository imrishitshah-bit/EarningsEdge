import requests

from scripts.config import ALPHA_VANTAGE_API_KEY

BASE_URL = "https://www.alphavantage.co/query"


def get_historical_earnings(symbol: str):

    response = requests.get(
        BASE_URL,
        params={
            "function": "EARNINGS",
            "symbol": symbol,
            "apikey": ALPHA_VANTAGE_API_KEY,
        },
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    if "quarterlyEarnings" not in data:
        return []

    return data["quarterlyEarnings"]