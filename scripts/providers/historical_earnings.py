import time
import requests

from scripts.config import (
    supabase,
    ALPHA_VANTAGE_API_KEY,
)

BASE_URL = "https://www.alphavantage.co/query"

companies = (
    supabase.table("companies")
    .select("id,ticker")
    .execute()
    .data
)

print(f"Found {len(companies)} companies")

for company in companies:

    ticker = company["ticker"]

    print(f"Fetching {ticker}...")

    response = requests.get(
        BASE_URL,
        params={
            "function": "EARNINGS",
            "symbol": ticker,
            "apikey": ALPHA_VANTAGE_API_KEY,
        },
        timeout=30,
    )

    data = response.json()

    if "quarterlyEarnings" not in data:
        print(data)
        time.sleep(15)
        continue

    rows = []

    for q in data["quarterlyEarnings"]:

        estimated = q.get("estimatedEPS")
        reported = q.get("reportedEPS")
        surprise = q.get("surprisePercentage")

        try:
            estimated = float(estimated)
        except:
            estimated = None

        try:
            reported = float(reported)
        except:
            reported = None

        try:
            surprise = float(surprise)
        except:
            surprise = None

        rows.append(
            {
                "company_id": company["id"],
                "earnings_date": q.get("reportedDate"),
                "fiscal_quarter": None,
                "fiscal_year": None,
                "eps_estimate": estimated,
                "eps_actual": reported,
                "revenue_estimate": None,
                "revenue_actual": None,
                "eps_surprise": surprise,
                "revenue_surprise": None,
                "beat_eps": (
                    reported >= estimated
                    if reported is not None and estimated is not None
                    else None
                ),
                "beat_revenue": None,
                "price_before": None,
                "price_after": None,
                "move_1d": None,
                "move_5d": None,
            }
        )

    if rows:

        (
            supabase.table("historical_earnings")
            .upsert(
                rows,
                on_conflict="company_id,earnings_date",
            )
            .execute()
        )

        print(f"Stored {len(rows)} quarters")

    time.sleep(15)

print("Done.")