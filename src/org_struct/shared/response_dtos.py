from datetime import datetime

from pydantic import BaseModel
from typing import TypeVar


class DepartmentDTO(BaseModel):
    department_id: int
    name: str
    parent_id: int | None
    created_at: datetime


class EmployeeDTO(BaseModel):
    employee_id: int
    department_id: int
    position: str
    full_name: str
    created_at: datetime


class DepartmentTreeDTO(BaseModel):
    department: DepartmentDTO
    employees: list[EmployeeDTO] | None
    children: list[DepartmentDTO]


T_ResponseDTO = TypeVar("T_ResponseDTO", bound=DepartmentDTO | EmployeeDTO)
