from typing import Optional

from fastapi import APIRouter

from backend.app.services.earnings_service import get_this_week_earnings

router = APIRouter(
    prefix="/earnings",
    tags=["Earnings"],
)


@router.get("/this-week")
def earnings_this_week(
    sector: Optional[str] = None,
):
    return get_this_week_earnings(sector)