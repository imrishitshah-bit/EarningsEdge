import requests

from scripts.config import FMP_API_KEY

BASE_URL = "https://financialmodelingprep.com/stable/profile"


def get_company_profile(symbol: str):

    url = (
        f"{BASE_URL}"
        f"?symbol={symbol}"
        f"&apikey={FMP_API_KEY}"
    )

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    data = response.json()

    if not isinstance(data, list):
        return None

    if len(data) == 0:
        return None

    return data[0]