from scripts.update_earnings import main as update_earnings
from scripts.update_company_profiles import main as update_profiles
from scripts.fetch_market_data import main as fetch_market
from scripts.calculate_indicators import main as calculate
from scripts.upload_indicators import main as upload
from backend.app.update_scores import update_all_scores


def main():

    print("Updating earnings...")
    update_earnings()

    print("Updating company profiles...")
    update_profiles()

    print("Updating market data...")
    fetch_market()

    print("Calculating indicators...")
    calculate()

    print("Uploading indicators...")
    upload()

    print("Generating AI scores...")
    update_all_scores()

    print("\nDaily update complete.")


if __name__ == "__main__":
    main()