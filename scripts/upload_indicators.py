import math
import pandas as pd

from scripts.config import supabase


BATCH_SIZE = 500


def clean(value):
    """
    Convert NaN/Infinity to None so JSON serialization succeeds.
    """

    if pd.isna(value):
        return None

    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return None

    return value
def upload_indicators(df: pd.DataFrame):

    records = []

    for _, row in df.iterrows():

        records.append(
            {
                "id": int(row["id"]),
                "rsi": clean(row["rsi"]),
                "macd": clean(row["macd"]),
                "sma20": clean(row["sma20"]),
                "sma50": clean(row["sma50"]),
                "volatility": clean(row["volatility"]),
            }
        )

    total = len(records)

    if total == 0:
        return

    print(
        f"Uploading {total} rows in {(total + BATCH_SIZE - 1) // BATCH_SIZE} batches..."
    )

    for i in range(0, total, BATCH_SIZE):

        batch = records[i : i + BATCH_SIZE]

        (
            supabase.table("market_data")
            .upsert(
                batch,
                on_conflict="id",
            )
            .execute()
        )

        print(
            f"Uploaded {min(i + BATCH_SIZE, total)}/{total}"
        )

def main():

    df = pd.read_csv("indicator_updates.csv")

    upload_indicators(df)

    print("\nDone!")

if __name__ == "__main__":
    main()