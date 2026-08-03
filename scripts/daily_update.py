import sys
import time
from pathlib import Path

# When executed directly as a script, Python sets sys.path[0] to the scripts folder.
# Add the project root so package imports like `from scripts...` work correctly.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.update_earnings import main as update_earnings
from scripts.update_company_profiles import main as update_profiles
from scripts.fetch_market_data import main as fetch_market
from scripts.calculate_indicators import main as calculate
from scripts.upload_indicators import main as upload
from scripts.update_scores import update_all_scores


def run_step(name, func):
    """Runs one pipeline step with logging and error handling."""

    print(f"\n{name}...")

    start = time.time()

    try:
        func()

        elapsed = time.time() - start

        print(f"✓ {name} completed ({elapsed:.1f}s)")

        return True

    except Exception as e:

        elapsed = time.time() - start

        print(f"✗ {name} failed ({elapsed:.1f}s)")
        print(f"Error: {e}")

        return False


def main():

    overall_start = time.time()

    print("\n========================================")
    print("      EarningsEdge Daily Update")
    print("========================================")

    results = []

    results.append(run_step("Updating earnings", update_earnings))
    results.append(run_step("Updating company profiles", update_profiles))
    results.append(run_step("Fetching market data", fetch_market))
    results.append(run_step("Calculating indicators", calculate))
    results.append(run_step("Uploading indicators", upload))
    results.append(run_step("Generating AI scores", update_all_scores))

    total_time = time.time() - overall_start

    successful = sum(results)
    failed = len(results) - successful

    print("\n========================================")
    print("Daily Update Summary")
    print("========================================")
    print(f"Successful steps : {successful}")
    print(f"Failed steps     : {failed}")
    print(f"Total runtime    : {total_time:.1f} seconds")
    print("========================================\n")


if __name__ == "__main__":
    main()