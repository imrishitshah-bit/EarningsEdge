from fastapi import APIRouter
from backend.app.database import supabase

router = APIRouter()

@router.get("/debug/companies")
def debug_companies():
    return (
        supabase.table("companies")
        .select("ticker,sector")
        .limit(10)
        .execute()
        .data
    )