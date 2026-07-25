def relative_strength_score(technical):
    if technical is None:
        return 0, []

    rsi = technical.get("rsi")

    if rsi is None:
        return 0, []

    if 55 <= rsi <= 70:
        return 10, ["Strong relative strength"]

    if 45 <= rsi < 55:
        return 6, ["Average relative strength"]

    return 2, ["Weak relative strength"]