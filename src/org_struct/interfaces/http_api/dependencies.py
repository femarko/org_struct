from fastapi import Depends
from sqlalchemy.orm import Session

from org_struct.infrastructure.db.sqlalchemy_session import get_session
from org_struct.domain.repo_interface import Repositories
from org_struct.infrastructure.db.repositories import (
    EmployeeRepo,
    DepartmentRepo,
)
from org_struct.application.use_cases import (
    AddDepartment,
    AddEmployee,
    GetDepartment,
    MoveDepartment,
    DeleteDepartment,
)

repositories = Repositories(
    department=DepartmentRepo(session=Depends(get_session)),
    employee=EmployeeRepo(session=Depends(get_session)),
)


def get_repositories() -> Repositories:
    return repositories


def get_add_department_use_case() -> AddDepartment:
    return AddDepartment(repos=repositories)


def get_add_employee_use_case() -> AddEmployee:
    return AddEmployee(repos=repositories)


def get_get_department_use_case() -> GetDepartment:
    return GetDepartment(repos=repositories)


def get_move_department_use_case() -> MoveDepartment:
    return MoveDepartment(repos=repositories)


def get_delete_department_use_case() -> DeleteDepartment:
    return DeleteDepartment(repos=repositories)
