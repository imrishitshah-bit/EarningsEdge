def score(earnings):
    if earnings["eps_estimate"] is not None:
        return 20, "+20 EPS estimate available"

    return 0, "No EPS estimate"