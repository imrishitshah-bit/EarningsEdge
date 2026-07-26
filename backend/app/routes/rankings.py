from fastapi import APIRouter

from backend.app.services.rankings_service import get_rankings

router = APIRouter(
    prefix="/rankings",
    tags=["Rankings"],
)


@router.get("")
def rankings():
    return get_rankings()