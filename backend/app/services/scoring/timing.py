from datetime import date, datetime


def score(earnings):
    earnings_date = datetime.strptime(
        earnings["earnings_date"],
        "%Y-%m-%d"
    ).date()

    days = (earnings_date - date.today()).days

    if 0 <= days <= 7:
        return 20, "+20 Earnings within one week"

    return 0, "Earnings not within one week"