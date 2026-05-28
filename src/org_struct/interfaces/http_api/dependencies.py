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
from org_struct.domain.services import Service



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


def get_domain_service(repos=Depends(get_repos)) -> Service:
    return Service(repos)
