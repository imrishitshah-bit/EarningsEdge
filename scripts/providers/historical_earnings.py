def historical_score(history):
    """
    Historical Earnings Score (0-100)

    Measures how consistently the company
    performs during earnings.
    """

    if not history:

        return {
            "score": 50,
            "reasons": ["Limited earnings history"],
        }

    score = 0
    reasons = []

    total = len(history)

    # ---------------------------------
    # EPS Beat Rate (0-40)
    # ---------------------------------

    eps_beats = sum(
        1
        for row in history
        if row["beat_eps"]
    )

    beat_rate = eps_beats / total

    if beat_rate >= 0.90:

        score += 40
        reasons.append("Exceptional EPS beat history")

    elif beat_rate >= 0.75:

        score += 35
        reasons.append(f"Beat EPS in {eps_beats} of last {total}")

    elif beat_rate >= 0.60:

        score += 28
        reasons.append("Strong earnings consistency")

    elif beat_rate >= 0.50:

        score += 20

    elif beat_rate >= 0.30:

        score += 12

    else:

        score += 5
        reasons.append("Weak earnings history")

    # ---------------------------------
    # Average Surprise (0-30)
    # ---------------------------------

    surprises = [
        row["eps_surprise"]
        for row in history
        if row["eps_surprise"] is not None
    ]

    if surprises:

        avg = sum(surprises) / len(surprises)

        if avg >= 20:

            score += 30
            reasons.append(f"Average EPS surprise +{avg:.1f}%")

        elif avg >= 10:

            score += 24
            reasons.append(f"Average EPS surprise +{avg:.1f}%")

        elif avg >= 5:

            score += 18

        elif avg >= 0:

            score += 12

        elif avg >= -5:

            score += 8

        else:

            score += 2
            reasons.append("Negative surprise history")

    # ---------------------------------
    # Current Beat Streak (0-20)
    # ---------------------------------

    streak = 0

    for row in history:

        if row["beat_eps"]:
            streak += 1
        else:
            break

    if streak >= 8:

        score += 20
        reasons.append("8 consecutive EPS beats")

    elif streak >= 6:

        score += 16

    elif streak >= 4:

        score += 12

    elif streak >= 2:

        score += 8

    elif streak >= 1:

        score += 4

    # ---------------------------------
    # Data Availability (0-10)
    # ---------------------------------

    if total >= 8:

        score += 10

    elif total >= 6:

        score += 8

    elif total >= 4:

        score += 6

    elif total >= 2:

        score += 4

    else:

        score += 2

    score = max(0, min(score, 100))

    return {
        "score": score,
        "reasons": reasons,
    }