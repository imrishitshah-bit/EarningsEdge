from backend.app.database import supabase


def get_rankings():

    return (
        supabase.table("scores")
        .select("*")
        .order("rank")
        .execute()
        .data
    )