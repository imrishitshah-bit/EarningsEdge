from backend.app.database import supabase


def get_prediction_stats():
    """
    Returns prediction accuracy statistics.
    """

    rows = (
        supabase.table("prediction_history")
        .select("correct")
        .eq("checked", True)
        .execute()
        .data
    )

    correct = sum(
        1 for row in rows
        if row["correct"] is True
    )

    wrong = sum(
        1 for row in rows
        if row["correct"] is False
    )

    total = correct + wrong

    accuracy = 0

    if total > 0:
        accuracy = round(
            (correct / total) * 100,
            1,
        )

    return {
        "correct": correct,
        "wrong": wrong,
        "total": total,
        "accuracy": accuracy,
    }