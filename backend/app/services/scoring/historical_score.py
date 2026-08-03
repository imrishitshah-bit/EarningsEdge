def historical_score(history):
    """
    Scores historical earnings performance (0-100)

    Rewards:
    - Beat consistency
    - Average surprise
    - Beat streak
    """

    if not history or len(history) < 4:
        return {
            "score": 50,
            "reasons": [],
        }

    reasons = []

    total = len(history)

    eps_beats = sum(
        1
        for row in history
        if row["beat_eps"]
    )

    beat_rate = eps_beats / total

    surprises = [
        row["eps_surprise"]
        for row in history
        if row["eps_surprise"] is not None
    ]

    avg_surprise = (
        sum(surprises) / len(surprises)
        if surprises
        else 0
    )

    streak = 0

    for row in history:
        if row["beat_eps"]:
            streak += 1
        else:
            break

    # ---------------------------------
    # Base Score
    # ---------------------------------

    score = 40

    # ---------------------------------
    # Beat Rate
    # ---------------------------------

    if beat_rate >= 0.90:
        score += 30
        reasons.append("Exceptional EPS beat history")

    elif beat_rate >= 0.75:
        score += 24
        reasons.append(f"Beat EPS in {eps_beats} of last {total}")

    elif beat_rate >= 0.60:
        score += 18
        reasons.append("Strong earnings consistency")

    elif beat_rate >= 0.40:
        score += 10

    else:
        score -= 10
        reasons.append("Weak earnings history")

    # ---------------------------------
    # Surprise %
    # ---------------------------------

    if avg_surprise >= 20:
        score += 20
        reasons.append(f"Average EPS surprise +{avg_surprise:.1f}%")

    elif avg_surprise >= 10:
        score += 15
        reasons.append(f"Average EPS surprise +{avg_surprise:.1f}%")

    elif avg_surprise >= 5:
        score += 8

    elif avg_surprise < -5:
        score -= 10
        reasons.append("Negative surprise history")

    # ---------------------------------
    # Beat Streak
    # ---------------------------------

    if streak >= 8:
        score += 10
        reasons.append("8 consecutive EPS beats")

    elif streak >= 6:
        score += 7

    elif streak >= 4:
        score += 4

    score = max(0, min(score, 100))

    return {
        "score": score,
        "reasons": reasons,
    }