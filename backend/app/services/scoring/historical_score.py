def historical_score(history):
    """
    Scores historical earnings performance (0-20)

    Rewards consistency over lucky quarters.
    """

    if not history:

        return {
            "score": 5,
            "reasons": ["No historical earnings available"],
        }

    score = 0
    reasons = []

    total = len(history)

    eps_beats = sum(
        1
        for row in history
        if row["beat_eps"]
    )

    beat_rate = eps_beats / total

    # -----------------------------
    # Beat Rate
    # -----------------------------

    if beat_rate >= 0.90:

        score += 9
        reasons.append("Exceptional EPS beat history")

    elif beat_rate >= 0.75:

        score += 7
        reasons.append(
            f"Beat EPS in {eps_beats} of last {total}"
        )

    elif beat_rate >= 0.60:

        score += 5
        reasons.append("Strong earnings consistency")

    elif beat_rate >= 0.40:

        score += 3

    else:

        score += 1
        reasons.append("Weak earnings history")

    # -----------------------------
    # Average Surprise
    # -----------------------------

    surprises = [
        row["eps_surprise"]
        for row in history
        if row["eps_surprise"] is not None
    ]

    if surprises:

        avg = sum(surprises) / len(surprises)

        if avg >= 20:

            score += 6
            reasons.append(
                f"Average EPS surprise +{avg:.1f}%"
            )

        elif avg >= 10:

            score += 5
            reasons.append(
                f"Average EPS surprise +{avg:.1f}%"
            )

        elif avg >= 5:

            score += 3

        elif avg < -5:

            score -= 2
            reasons.append(
                "Negative surprise history"
            )

    # -----------------------------
    # Beat Streak
    # -----------------------------

    streak = 0

    for row in history:

        if row["beat_eps"]:
            streak += 1
        else:
            break

    if streak >= 8:

        score += 3
        reasons.append("8 consecutive EPS beats")

    elif streak >= 6:

        score += 2

    elif streak >= 4:

        score += 1

    score = max(0, min(score, 20))

    return {
        "score": score,
        "reasons": reasons,
    }