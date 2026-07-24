from fastapi import FastAPI
from backend.app.database import supabase

app = FastAPI(
    title="EarningsEdge API",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "status": "online",
        "project": "EarningsEdge",
        "version": "1.0.0"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

@app.get("/test-db")
def test_database():
    response = supabase.table("companies").select("*").limit(5).execute()
    return response.data