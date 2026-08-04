import requests
import os

FMP_API_KEY = os.getenv("FMP_API_KEY")


def get_historical_earnings(ticker: str):

    url = (
        "https://financialmodelingprep.com/stable/"
        f"historical-earnings?symbol={ticker}"
        f"&apikey={FMP_API_KEY}"
    )

    print(url)

    response = requests.get(url, timeout=30)

    print("Status:", response.status_code)
    print(response.text)

    if response.status_code != 200:
        return []

    data = response.json()

    return data