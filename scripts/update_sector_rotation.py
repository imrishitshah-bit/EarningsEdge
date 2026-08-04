from collections import defaultdict

from scripts.config import supabase


def main():

    print("=" * 50)
    print("UPDATING SECTOR ROTATION")
    print("=" * 50)

    rows = (
        supabase.table("scores")
        .select(
            """
            company_id,
            ai_score,
            companies!inner(
                sector
            )
            """
        )
        .execute()
        .data
    )

    if not rows:
        print("No scores found.")
        return

    sectors = defaultdict(list)

    for row in rows:

        score = row.get("ai_score")

        company = row.get("companies")

        if not company:
            continue

        sector = company.get("sector")

        if sector is None:
            continue

        if score is None:
            continue

        sectors[sector].append(score)

    sector_rows = []

    for sector, scores in sectors.items():

        # Ignore sectors with only one company
        if len(scores) < 2:
            continue

        average = round(sum(scores) / len(scores), 1)

        sector_rows.append(
            {
                "sector": sector,
                "average_score": average,
                "company_count": len(scores),
            }
        )

    sector_rows.sort(
        key=lambda x: x["average_score"],
        reverse=True,
    )

    for rank, row in enumerate(sector_rows, start=1):

        row["rank"] = rank

    (
        supabase.table("sector_rotation")
        .upsert(
            sector_rows,
            on_conflict="sector",
        )
        .execute()
    )

    print(f"Updated {len(sector_rows)} sectors.")

    print("=" * 50)


if __name__ == "__main__":
    main()