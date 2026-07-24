from backend.app.services.earnings_service import get_this_week_earnings


def get_homepage():
    earnings = get_this_week_earnings()

    return {
        "featured_stock": None,
        "top_ai_picks": [],
        "market_summary": {
            "status": "Coming Soon"
        },
        "upcoming_earnings": earnings[:10]
    }