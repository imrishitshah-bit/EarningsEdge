def score(earnings):
    if earnings["revenue_estimate"] is not None:
        return 20, "+20 Revenue estimate available"

    return 0, "No revenue estimate"