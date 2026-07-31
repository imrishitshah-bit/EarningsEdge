def expectation_risk(company, market, earnings):
    """
    Scores how much GOOD NEWS is already priced into the stock.

    Higher score = Higher expectations = Harder to beat.

    Returns:
    {
        score,
        reasons
    }
    """

    score = 0
    reasons = []

    rsi = market.get("rsi")
    volatility = market.get("volatility")
    close = market.get("close")
    sma20 = market.get("sma20")
    market_cap = company.get("market_cap")
    eps = earnings.get("eps_estimate")

    # ------------------------
    # RSI
    # ------------------------

    if rsi is not None:

        if rsi >= 75:

            score += 8
            reasons.append(
                "Extremely bullish sentiment"
            )

        elif rsi >= 65:

            score += 6
            reasons.append(
                "High investor expectations"
            )

        elif rsi >= 55:

            score += 3

    # ------------------------
    # Run Above SMA20
    # ------------------------

    if (
        close is not None
        and sma20 is not None
        and sma20 > 0
    ):

        run = (close - sma20) / sma20

        if run >= 0.15:

            score += 7
            reasons.append(
                "Large rally before earnings"
            )

        elif run >= 0.08:

            score += 5
            reasons.append(
                "Strong run-up before earnings"
            )

        elif run >= 0.03:

            score += 2

    # ------------------------
    # Volatility
    # ------------------------

    if volatility is not None:

        if volatility < 0.25:

            score += 5
            reasons.append(
                "Low implied uncertainty"
            )

        elif volatility < 0.40:

            score += 3

    # ------------------------
    # Mega Caps
    # ------------------------

    if market_cap is not None:

        if market_cap > 1_000_000_000_000:

            score += 3
            reasons.append(
                "Mega-cap with elevated expectations"
            )

        elif market_cap > 300_000_000_000:

            score += 2

    # ------------------------
    # Huge EPS Estimates
    # ------------------------

    if eps is not None:

        if eps > 8:

            score += 3
            reasons.append(
                "Wall Street expects exceptional earnings"
            )

        elif eps > 5:

            score += 2

    score = min(score, 25)

    return {
        "score": score,
        "reasons": reasons,
    }