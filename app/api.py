from fastapi import APIRouter, Request, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import Employee
from app.schemas import SearchResponse
from app.rate_limiter import is_rate_limited
from app.config import ORG_COLUMN_CONFIG
from app.database import get_db

import traceback

router = APIRouter()

@router.get("/search", response_model=SearchResponse)
def search_employees(
    request: Request,
    status: list[str] = Query(None),
    location: str = Query(None),
    company_id: int = Query(...),
    department: str = Query(None),
    position: str = Query(None),
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db)
):
    try:
        client_ip = request.client.host
        if is_rate_limited(client_ip):
            raise HTTPException(
                status_code=429,
                detail="⛔ Rate limit exceeded. Try again later."
            )

        query = db.query(Employee).filter(Employee.organization_id == company_id)

        if status:
            query = query.filter(Employee.status.in_(status))
        if location:
            query = query.filter(func.lower(Employee.location) == location.lower())
        if department:
            query = query.filter(func.lower(Employee.department) == department.lower())
        if position:
            query = query.filter(func.lower(Employee.position) == position.lower())

        total = query.count()
        employees = query.offset((page - 1) * page_size).limit(page_size).all()

        column_config = ORG_COLUMN_CONFIG.get(company_id, [])
        
        
        print(f"⚠️ company_id={company_id}, employees found: {len(employees)}")
        print(f"🧱 column_config = {column_config}")

        valid_columns = set(c.name for c in Employee.__table__.columns)
        safe_columns = [col for col in column_config if col in valid_columns]
        invalid_columns = [col for col in column_config if col not in valid_columns]

        print(f"✅ safe_columns = {safe_columns}")
        print(f"❌ invalid_columns = {invalid_columns}")



        if invalid_columns:
            raise HTTPException(
                status_code=422,
                detail=f"❌ Invalid column(s): {', '.join(invalid_columns)}"
            )

        results = [
            {col: getattr(emp, col) for col in safe_columns}
            for emp in employees
        ]

        return {"results": results, "total": total}

    except HTTPException as http_exc:
        raise http_exc  # Allow FastAPI to handle known HTTP exceptions

    except Exception as e:
        print("🔥 Internal Server Error:", str(e))