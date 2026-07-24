def score(earnings):
    revenue = earnings["revenue_estimate"]

    if revenue is not None and revenue >= 10_000_000_000:
        return 20, "+20 Large-cap revenue profile"

    return 0, "Not a large-cap revenue profile"