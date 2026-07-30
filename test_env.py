from backend.app.database import supabase

print(
    supabase.table("scores")
    .select("*")
    .limit(1)
    .execute()
)