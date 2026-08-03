from backend.app.database import supabase
from backend.app.services.scoring.final_score import calculate_score
from backend.app.services.scoring.expected_move import expected_move
from backend.app.services.scoring.probability import probability
from backend.app.services.scenario_service import scenarios
from backend.app.services.scoring.price_target import price_target
from datetime import datetime, timezone

def get_score(ticker: str):

    # ---------------------------------
    # Company
    # ---------------------------------

    company_result = (
        supabase.table("companies")
        .select("*")
        .eq("ticker", ticker.upper())
        .single()
        .execute()
    )

    if not company_result.data:
        return None

    company = company_result.data

    # ---------------------------------
    # Upcoming Earnings
    # ---------------------------------

    today = datetime.now(timezone.utc).date().isoformat()
    earnings_result = (
    supabase.table("earnings")
    .select("*")
    .eq("company_id", company["id"])
    .gte("earnings_date", today)
    .order("earnings_date")
    .limit(1)
    .execute()
    )
    
    if not earnings_result.data:
        return {
            "ticker": company["ticker"],
            "company_name": company["company_name"],
            "ai_score": 0,
            "confidence": "Very Low",
            "reasons": [
                "No upcoming earnings found."
            ],
        }

    earnings = earnings_result.data[0]

    # ---------------------------------
    # Latest Technical Data
    # ---------------------------------

    market_rows = (
        supabase.table("market_data")
        .select("*")
        .eq("company_id", company["id"])
        .order("trading_date", desc=True)
        .limit(100)
        .execute()
        .data
    )

    market = None

    for row in market_rows:

        if (
            row["rsi"] is not None
            and row["macd"] is not None
            and row["sma20"] is not None
            and row["sma50"] is not None
            and row["volatility"] is not None
        ):
            market = row
            break

    if market is None:

        return {
            "ticker": company["ticker"],
            "company_name": company["company_name"],
            "ai_score": 50,
            "confidence": "Low",
            "reasons": [
                "Technical indicators have not been calculated yet."
            ],
            "earnings_date": earnings["earnings_date"],
            "eps_estimate": earnings["eps_estimate"],
            "revenue_estimate": earnings["revenue_estimate"],
            "technical": None,
        }

    # ---------------------------------
    # Historical Earnings
    # ---------------------------------

    history = (
        supabase.table("historical_earnings")
        .select("*")
        .eq("company_id", company["id"])
        .order("earnings_date", desc=True)
        .limit(8)
        .execute()
        .data
    )

    # ---------------------------------
    # AI Score
    # ---------------------------------

    result = calculate_score(
        company,
        earnings,
        market,
        history,
    )

    score = result["score"]
    confidence = result["confidence"]
    reasons = result["reasons"]
    breakdown = result["breakdown"]

    # ---------------------------------
    # Expected Move
    # ---------------------------------

    move_data = expected_move(
        market,
        history,
    )

    move = move_data["move"]
    move_confidence = move_data["confidence"]

    # ---------------------------------
    # Probability
    # ---------------------------------

    prob = probability(score)

    # ---------------------------------
    # Bull / Base / Bear
    # ---------------------------------

    cases = scenarios(move)

    # ---------------------------------
    # Target Price
    # ---------------------------------

    target = price_target(
        market["close"],
        score,
        move,
    )

    positives = [
        r for r in reasons
        if not any(
            x in r.lower()
            for x in [
                "weak",
                "negative",
                "declining",
                "below",
                "high volatility",
                "bearish",
            ]
        )
    ]

    negatives = [
        r for r in reasons
        if r not in positives
    ]

    return {

        "ticker": company["ticker"],
        "company_name": company["company_name"],

        "ai_score": score,

        "grade": (
            "A+"
            if score >= 95 else
            "A"
            if score >= 90 else
            "A-"
            if score >= 85 else
            "B+"
            if score >= 80 else
            "B"
            if score >= 75 else
            "B-"
            if score >= 70 else
            "C+"
            if score >= 60 else
            "C"
            if score >= 50 else
            "C-"
            if score >= 40 else
            "D"
            if score >= 30 else
            "F"
        ),

        "confidence": confidence,

        "recommendation": (
            "Strong Buy"
            if score >= 85 else
            "Buy Before Earnings"
            if score >= 72 else
            "Watch Closely"
            if score >= 55 else
            "Neutral"
            if score >= 40 else
            "Avoid"
        ),

        "risk_level": (
            "Low"
            if market["volatility"] < 0.35 else
            "Medium"
            if market["volatility"] < 0.60 else
            "High"
        ),

        "summary": (
            f"{company['ticker']} has an AI Score of {score}/100 "
            f"with {confidence.lower()} confidence. "
            f"The stock currently shows "
            f"{len(positives)} positive signals and "
            f"{len(negatives)} cautionary signals heading into earnings."
        ),

        "strengths": positives,
        "weaknesses": negatives,

        "reasons": reasons,
        "breakdown": breakdown,

        "probability": prob,

        "expected_move": move,
        "expected_move_confidence": move_confidence,

        "bull_case": cases["bull"],
        "base_case": cases["base"],
        "bear_case": cases["bear"],

        "target_price": target,

        "earnings_date": earnings["earnings_date"],
        "eps_estimate": earnings["eps_estimate"],
        "revenue_estimate": earnings["revenue_estimate"],

        "technical": {

            "close": market["close"],
            "rsi": market["rsi"],
            "macd": market["macd"],
            "sma20": market["sma20"],
            "sma50": market["sma50"],
            "volatility": market["volatility"],
            "trading_date": market["trading_date"],

        },

        "historical": {

            "quarters_analyzed": len(history),

            "eps_beats": sum(
                1
                for h in history
                if h["beat_eps"]
            ),

            "average_surprise": round(

                sum(
                    h["eps_surprise"]
                    for h in history
                    if h["eps_surprise"] is not None
                )

                / max(

                    1,

                    len(
                        [
                            h
                            for h in history
                            if h["eps_surprise"] is not None
                        ]
                    ),

                ),

                2,

            ),

        },

    }