def scenarios(expected_move):
    """
    Returns bull, base, and bear percentage moves.
    """

    if expected_move is None:
        return {
            "bull": None,
            "base": None,
            "bear": None,
        }

    return {
        "bull": round(expected_move * 1.5, 1),
        "base": round(expected_move, 1),
        "bear": round(-expected_move, 1),
    }