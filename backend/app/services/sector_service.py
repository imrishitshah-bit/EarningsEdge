from backend.app.database import supabase


def get_sector_rotation():
    return (
        supabase.table("sector_rotation")
        .select("*")
        .order("rank")
        .execute()
        .data
    )


def get_companies_by_sector(sector: str):
    return (
        supabase.rpc(
            "get_companies_by_sector",
            {"sector_name": sector},
        )
        .execute()
        .data
    )