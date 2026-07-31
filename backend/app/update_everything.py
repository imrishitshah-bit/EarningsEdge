from backend.app.services.cleanup_old_earnings import cleanup_old_earnings
from backend.app.services.update_earnings import update_earnings
from backend.app.services.update_market import update_market
from backend.app.services.update_valuation import update_valuation
from backend.app.services.scoring.update_scores import update_all_scores


def run():

    print("STEP 1")
    cleanup_old_earnings()

    print("STEP 2")
    update_earnings()

    print("STEP 3")
    update_market()

    print("STEP 4")
    update_valuation()

    print("STEP 5")
    update_all_scores()

    print("DONE")


run()