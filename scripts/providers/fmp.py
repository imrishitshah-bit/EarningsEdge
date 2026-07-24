import os
from datetime import date, timedelta
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[2] / ".env")

API_KEY = os.getenv("FMP_API_KEY")

if not API_KEY:
    raise ValueError("FMP_API_KEY is missing from .env")


def get_upcoming_earnings(days: int = 7):
    today = date.today()
    end_date = today + timedelta(days=days)

    url = (
        "https://financialmodelingprep.com/stable/earnings-calendar"
        f"?from={today}"
        f"&to={end_date}"
        f"&apikey={API_KEY}"
    )

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    return response.json()


def normalize_earnings(record: dict):
    session = (record.get("time") or "").upper()

    if session not in ["AMC", "BMO"]:
        session = None

    return {
        "ticker": record.get("symbol"),
        "company_name": record.get("name") or record.get("symbol"),
        "earnings_date": record.get("date"),
        "session": session,
        "eps_estimate": record.get("epsEstimated"),
        "revenue_estimate": record.get("revenueEstimated"),
    }