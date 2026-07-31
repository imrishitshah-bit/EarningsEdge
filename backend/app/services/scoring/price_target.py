def price_target(current_price, score, expected_move):
    """
    Returns the AI target price after earnings.
    """

    if current_price is None or expected_move is None:
        return None

    move = expected_move / 100

    if score >= 90:
        multiplier = 1.25

    elif score >= 80:
        multiplier = 1.00

    elif score >= 70:
        multiplier = 0.60

    elif score >= 60:
        multiplier = 0.20

    else:
        multiplier = -0.50

    target = current_price * (1 + move * multiplier)

    return round(target, 2)