from fastapi import APIRouter, HTTPException

from backend.app.services.company_service import get_company

router = APIRouter(
    prefix="/companies",
    tags=["Companies"],
)


@router.get("/{ticker}")
def company_details(ticker: str):
    company = get_company(ticker)

    if company is None:
        raise HTTPException(
            status_code=404,
            detail="Company not found",
        )

    return company