import requests

from scripts.config import FMP_API_KEY

BASE_URL = "https://financialmodelingprep.com/stable/earnings-calendar"


def get_upcoming_earnings():

    url = (
        f"{BASE_URL}"
        f"?from=today"
        f"&to=+60days"
        f"&apikey={FMP_API_KEY}"
    )

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    data = response.json()

    if not isinstance(data, list):
        return []

    return data