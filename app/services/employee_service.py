from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.employee_repository import search_employees, get_visible_columns
from app.models import Employee
from app.utils.logger import logger


def build_employee_result(employee: Employee, columns: list[str]) -> dict:
    valid_columns = set(c.name for c in Employee.__table__.columns)
    safe_columns = [col for col in columns if col in valid_columns]
    invalid_columns = [col for col in columns if col not in valid_columns]

    if invalid_columns:
        logger.warning(f"Invalid column(s) requested: {invalid_columns}")
        raise HTTPException(
            status_code=422,
            detail=f"Invalid column(s): {', '.join(invalid_columns)}"
        )

    return {col: getattr(employee, col) for col in safe_columns}


def search_employee_records(
    db: Session,
    company_id: int,
    status: list[str] = None,
    location: str = None,
    department: str = None,
    position: str = None,
    name: str = None,
    page: int = 1,
    page_size: int = 10,
):
    employees, total = search_employees(
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

    columns = get_visible_columns(db, company_id)
    logger.info(f"Search result: {len(employees)} employees, columns: {columns}")

    results = [build_employee_result(emp, columns) for emp in employees]
    return results, total
