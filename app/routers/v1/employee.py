from fastapi import APIRouter, Request, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.schemas import SearchResponse
# from app.database import get_db
from ...database import get_db
from app.services.employee_service import *

router = APIRouter()

@router.get("/employees/search", response_model=SearchResponse)
def search_employees(
    request: Request,
    status: list[str] = Query(None),
    location: str = Query(None),
    company_id: int = Query(...),
    department: str = Query(None),
    position: str = Query(None),
    name: str = Query(None),
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db),
):
    try:
        results, total = search_employee_records(
            db=db,
            company_id=company_id,
            status=status,
            location=location,
            department=department,
            position=position,
            name=name,
            page=page,
            page_size=page_size,
        )
        return {"results": results, "total": total}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        from app.utils.logger import logger
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
