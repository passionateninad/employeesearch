from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class EmployeeOut(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    status: str
    department: Optional[str]
    position: Optional[str]
    location: Optional[str]

class SearchResponse(BaseModel):
    results: List[Dict[str, Any]]
    total: int
