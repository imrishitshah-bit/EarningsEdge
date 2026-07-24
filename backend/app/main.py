from fastapi import FastAPI

from backend.app.routes.earnings import router as earnings_router

app = FastAPI(
    title="EarningsEdge API",
    version="1.0.0",
)

app.include_router(earnings_router)


@app.get("/")
def home():
    return {
        "status": "online",
        "project": "EarningsEdge",
        "version": "1.0.0",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }