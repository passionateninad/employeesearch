from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from app.models import Employee, ColumnConfig

def get_visible_columns(db: Session, company_id: int) -> list[str]:
    configs = db.query(ColumnConfig).filter_by(organization_id=company_id, is_visible=True).all()
    return [c.column_name for c in configs]

def search_employees(
    db: Session,
    company_id: int,
    status: list[str] = None,
    location: str = None,
    department: str = None,
    position: str = None,
    name: str = None,
    page: int = 1,
    page_size: int = 10,
) -> tuple[list[Employee], int]:
    query = db.query(Employee).filter(Employee.organization_id == company_id)

    if status:
        query = query.filter(Employee.status.in_(status))
    if location:
        query = query.filter(func.lower(Employee.location) == location.lower())
    if department:
        query = query.filter(func.lower(Employee.department) == department.lower())
    if position:
        query = query.filter(func.lower(Employee.position) == position.lower())
    if name:
        query = query.filter(
            or_(
                func.lower(Employee.first_name).like(f"%{name.lower()}%"),
                func.lower(Employee.last_name).like(f"%{name.lower()}%")
            )
        )

    total = query.count()
    employees = query.offset((page - 1) * page_size).limit(page_size).all()

    return employees, total
