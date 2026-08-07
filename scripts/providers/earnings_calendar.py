import requests
from datetime import date, timedelta

from scripts.config import FMP_API_KEY

BASE_URL = "https://financialmodelingprep.com/stable/earnings-calendar"


def get_upcoming_earnings():

    today = date.today()
    end_date = today + timedelta(days=60)

    url = (
        f"{BASE_URL}"
        f"?from={today.isoformat()}"
        f"&to={end_date.isoformat()}"
        f"&apikey={FMP_API_KEY}"
    )

    response = requests.get(
        url,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    if not isinstance(data, list):
        print("Unexpected FMP response:")
        print(data)
        return []

    # Extra safety: only keep genuinely upcoming earnings
    upcoming = [
        earning
        for earning in data
        if earning.get("date")
        and earning["date"] >= today.isoformat()
    ]

    return upcoming