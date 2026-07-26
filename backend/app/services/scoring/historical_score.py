def historical_score(history):
    """
    Scores historical earnings performance (0-20)
    """

    if not history:
        return 5, ["No historical earnings available."]

    score = 0
    reasons = []

    total = len(history)

    eps_beats = sum(
        1 for h in history
        if h["beat_eps"] is True
    )

    beat_rate = eps_beats / total

    # ------------------------
    # Beat Rate
    # ------------------------

    if beat_rate >= 0.80:
        score += 8
        reasons.append(
            f"Beat EPS in {eps_beats} of last {total} quarters"
        )

    elif beat_rate >= 0.60:
        score += 6
        reasons.append(
            "Strong EPS beat history"
        )

    elif beat_rate >= 0.40:
        score += 4

    else:
        score += 1
        reasons.append(
            "Weak earnings beat history"
        )

    # ------------------------
    # Average Surprise
    # ------------------------

    surprises = [
        h["eps_surprise"]
        for h in history
        if h["eps_surprise"] is not None
    ]

    if surprises:

        avg = sum(surprises) / len(surprises)

        if avg >= 15:
            score += 7
            reasons.append(
                f"Average EPS surprise +{avg:.1f}%"
            )

        elif avg >= 5:
            score += 5
            reasons.append(
                f"Average EPS surprise +{avg:.1f}%"
            )

        elif avg >= 0:
            score += 3

        else:
            score += 1
            reasons.append(
                "Negative average EPS surprise"
            )

    # ------------------------
    # Consecutive Beats
    # ------------------------

    streak = 0

    for h in history:

        if h["beat_eps"]:
            streak += 1
        else:
            break

    if streak >= 4:
        score += 5
        reasons.append(
            f"{streak} consecutive EPS beats"
        )

    elif streak >= 2:
        score += 3

    return min(score, 20), reasons