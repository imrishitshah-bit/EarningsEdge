from fastapi import APIRouter

from backend.app.services.prediction_stats_service import (
    get_prediction_stats,
)

router = APIRouter(
    prefix="/prediction-stats",
    tags=["Prediction Stats"],
)


@router.get("")
def prediction_stats():
    return get_prediction_stats()