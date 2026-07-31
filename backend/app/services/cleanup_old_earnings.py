from datetime import date

from backend.app.database import supabase


def cleanup_old_earnings():

    today = date.today().isoformat()

    (
        supabase.table("earnings")
        .delete()
        .lt("earnings_date", today)
        .execute()
    )

    print("Old earnings removed.")