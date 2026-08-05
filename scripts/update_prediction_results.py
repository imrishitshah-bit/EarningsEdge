from datetime import date, timedelta

from scripts.config import supabase
from scripts.providers.historical_price import get_price


def get_previous_price(ticker: str, earnings_date: date):

    current = earnings_date - timedelta(days=1)

    for _ in range(7):

        price = get_price(
            ticker,
            current.isoformat(),
        )

        if price is not None:
            return price

        current -= timedelta(days=1)

    return None


def get_next_price(ticker: str, earnings_date: date):

    current = earnings_date + timedelta(days=1)

    for _ in range(7):

        price = get_price(
            ticker,
            current.isoformat(),
        )

        if price is not None:
            return price

        current += timedelta(days=1)

    return None


def determine_direction(move):

    if move >= 2:
        return "UP"

    if move <= -2:
        return "DOWN"

    return "FLAT"


def prediction_correct(recommendation, move):

    recommendation = recommendation.upper()

    if recommendation == "BUY":
        return move > 0

    if recommendation == "AVOID":
        return move < 0

    if recommendation == "WATCH":
        return abs(move) < 5

    return None


def update_prediction(row):

    ticker = row["ticker"]

    earnings_date = date.fromisoformat(
        row["earnings_date"]
    )

    before = get_previous_price(
        ticker,
        earnings_date,
    )

    after = get_next_price(
        ticker,
        earnings_date,
    )

    if before is None or after is None:

        print(f"Skipping {ticker} (missing prices)")
        return False

    move = ((after - before) / before) * 100

    direction = determine_direction(move)

    correct = prediction_correct(
        row["recommendation"],
        move,
    )

    (
        supabase.table("prediction_history")
        .update(
            {
                "before_close": before,
                "after_close": after,
                "actual_move": round(move, 2),
                "actual_direction": direction,
                "correct": correct,
                "checked": True,
            }
        )
        .eq("id", row["id"])
        .execute()
    )

    print(
        f"{ticker:<6}"
        f"{move:+.2f}%"
        f"   {'✓' if correct else '✗'}"
    )

    return True


def main():

    predictions = (
        supabase.table("prediction_history")
        .select("*")
        .eq("checked", False)
        .lt("earnings_date", date.today().isoformat())
        .execute()
        .data
    )

    if not predictions:

        print("No predictions to update.")
        return

    print(
        f"Updating {len(predictions)} predictions...\n"
    )

    updated = 0

    for row in predictions:

        try:

            if update_prediction(row):
                updated += 1

        except Exception as e:

            print(
                f"Failed {row['ticker']}: {e}"
            )

    print()
    print(
        f"Finished. Updated {updated} predictions."
    )


if __name__ == "__main__":
    main()