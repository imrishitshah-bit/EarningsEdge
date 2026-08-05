from fastapi import APIRouter

from backend.app.services.sector_service import (
    get_sector_rotation,
    get_companies_by_sector,
)

router = APIRouter(
    prefix="/sector",
    tags=["Sector"],
)


@router.get("/rotation")
def sector_rotation():
    return get_sector_rotation()


@router.get("/{sector}")
def companies_in_sector(sector: str):
    return get_companies_by_sector(sector)