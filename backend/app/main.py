from fastapi import FastAPI
from backend.app.routes.dashboard import router as dashboard_router
from backend.app.routes.homepage import router as homepage_router
from backend.app.routes.earnings import router as earnings_router
from backend.app.routes.companies import router as companies_router
from backend.app.routes.scores import router as scores_router
from backend.app.routes.rankings import router as rankings_router
from backend.app.api.prediction_stats import (
    router as prediction_stats_router,
)
from backend.app.api.sector import (
    router as sector_router,
)
app = FastAPI(
    title="EarningsEdge API",
    version="1.0.0",
)
app.include_router(dashboard_router)
app.include_router(homepage_router)
app.include_router(earnings_router)
app.include_router(companies_router)
app.include_router(scores_router)
app.include_router(rankings_router)


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