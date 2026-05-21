from dotenv.cli import get
from fastapi import Depends

from org_struct.infrastructure.db.sqlalchemy_session import get_session
from org_struct.domain.models import (
    Department,    
    Employee,
)
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


def get_department_repo(session = Depends(get_session)) -> DepartmentRepo:
    return DepartmentRepo(session=session, model_cls=Department)


def get_employee_repo(session = Depends(get_session)) -> EmployeeRepo:
    return EmployeeRepo(session=session, model_cls=Employee)


def get_repos(
        department=Depends(get_department_repo),
        employee=Depends(get_employee_repo),
) -> Repositories:
    return Repositories(
        department=department,
        employee=employee,
    )


def get_add_department_use_case(repos=Depends(get_repos)) -> AddDepartment:
    return AddDepartment(repos)


def get_add_employee_use_case(repos=Depends(get_repos)) -> AddEmployee:
    return AddEmployee(repos)


def get_get_department_use_case(repos=Depends(get_repos)) -> GetDepartment:
    return GetDepartment(repos)


def get_move_department_use_case(repos=Depends(get_repos)) -> MoveDepartment:
    return MoveDepartment(repos)


def get_delete_department_use_case(repos=Depends(get_repos)) -> DeleteDepartment:
    return DeleteDepartment(repos)
