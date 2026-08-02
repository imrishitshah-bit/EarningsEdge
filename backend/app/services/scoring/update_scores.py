from datetime import datetime

from backend.app.database import supabase
from backend.app.services.score_service import get_score
def update_company_score(company_id: int, ticker: str):

    score = get_score(ticker)

    if score is None:
        return None

    score["company_id"] = company_id

    return score

def update_all_scores():

    # ---------------------------------
    # Clear Current Rankings
    # ---------------------------------

    print("Clearing previous rankings...")

    (
        supabase.table("scores")
        .delete()
        .neq("company_id", 0)
        .execute()
    )

    # ---------------------------------
    # Get Companies Reporting Soon
    # ---------------------------------

    earnings = (
        supabase.table("earnings")
        .select("company_id")
        .execute()
        .data
    )

    company_ids = list(
        {
            row["company_id"]
            for row in earnings
        }
    )

    if not company_ids:

        print("No upcoming earnings found.")
        return

    companies = (
        supabase.table("companies")
        .select("id,ticker")
        .in_("id", company_ids)
        .execute()
        .data
    )

    print(f"Updating {len(companies)} companies...\n")

    rankings = []

    required_fields = [

        "grade",
        "confidence",
        "recommendation",
        "risk_level",
        "summary",

        "strengths",
        "weaknesses",
        "reasons",
        "breakdown",

        "probability",
        "expected_move",
        "expected_move_confidence",

        "bull_case",
        "base_case",
        "bear_case",

        "target_price",

        "earnings_date",
        "eps_estimate",
        "revenue_estimate",

        "technical",
        "historical",

    ]

    # ---------------------------------
    # Generate Scores
    # ---------------------------------

    for company in companies:

        ticker = company["ticker"]

        try:

            score = update_company_score(
            company["id"],
            ticker,
            )

            if score is None:
                print(f"⚠ Skipping {ticker} (no score)")
                continue

            missing = [
                field
                for field in required_fields
                if field not in score
            ]

            if missing:
                print(f"⚠ Skipping {ticker}")
                print(f"Missing fields: {missing}")
                continue

            score["company_id"] = company["id"]

            rankings.append(score)

            print(f"✓ {ticker}")

        except Exception as e:

            print(f"✗ {ticker}")
            print(e)

    # ---------------------------------
    # Sort Rankings
    # ---------------------------------

    rankings.sort(
        key=lambda x: x["ai_score"],
        reverse=True,
    )

    # ---------------------------------
    # Save Rankings
    # ---------------------------------

    for rank, stock in enumerate(rankings, start=1):

        current_score = {

            "company_id": stock["company_id"],
            "ticker": stock["ticker"],
            "company_name": stock["company_name"],

            "ai_score": stock["ai_score"],
            "rank": rank,

            "grade": stock["grade"],
            "confidence": stock["confidence"],
            "recommendation": stock["recommendation"],
            "risk_level": stock["risk_level"],

            "summary": stock["summary"],

            "strengths": stock["strengths"],
            "weaknesses": stock["weaknesses"],
            "reasons": stock["reasons"],
            "breakdown": stock["breakdown"],

            "probability": stock["probability"],
            "expected_move": stock["expected_move"],
            "expected_move_confidence": stock["expected_move_confidence"],

            "bull_case": stock["bull_case"],
            "base_case": stock["base_case"],
            "bear_case": stock["bear_case"],

            "target_price": stock["target_price"],

            "earnings_date": stock["earnings_date"],
            "eps_estimate": stock["eps_estimate"],
            "revenue_estimate": stock["revenue_estimate"],

            "technical": stock["technical"],
            "historical": stock["historical"],

            "updated_at": datetime.utcnow().isoformat(),

        }

        (
            supabase.table("scores")
            .upsert(current_score)
            .execute()
        )

        history_record = current_score.copy()

        history_record.pop("rank", None)
        history_record.pop("updated_at", None)

        history_record["created_at"] = datetime.utcnow().isoformat()

        (
            supabase.table("score_history")
            .insert(history_record)
            .execute()
        )

    print("\n==============================")
    print("Score update complete!")
    print("==============================")
    print(f"Companies scored : {len(rankings)}")
    print("Current rankings updated.")
    print("Historical predictions archived.")