from fastapi import APIRouter

from backend.app.services.homepage_service import get_homepage

router = APIRouter(
    prefix="/homepage",
    tags=["Homepage"],
)


@router.get("")
def homepage():
    return get_homepage()