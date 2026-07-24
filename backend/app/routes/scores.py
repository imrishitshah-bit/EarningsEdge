from fastapi import APIRouter, HTTPException

from backend.app.services.score_service import get_score

router = APIRouter(
    prefix="/scores",
    tags=["Scores"],
)


@router.get("/{ticker}")
def score(ticker: str):
    result = get_score(ticker)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    return result