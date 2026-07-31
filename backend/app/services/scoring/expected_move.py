def expected_move(market, history):

    if market is None:

        return {
            "move": None,
            "confidence": 0
        }

    volatility = market["volatility"]

    if volatility is None:

        return {
            "move": None,
            "confidence": 0
        }

    # very rough estimate

    move = round(volatility * 12, 1)

    confidence = min(
        95,
        60 + int((1 - volatility) * 40)
    )

    return {
        "move": move,
        "confidence": confidence
    }