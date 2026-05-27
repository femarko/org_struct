import pytest
from typing import Any, Generator

from sqlalchemy.orm.session import Session
from sqlalchemy.sql import text

from org_struct.infrastructure.db.sqlalchemy_session import session_factory
from org_struct.domain.models import (
    Employee,
    Department,
)
from org_struct.domain.repo_interface import Repositories
from org_struct.infrastructure.db.repositories import (
    EmployeeRepo,
    DepartmentRepo,
)
from org_struct.domain.services import Service



@pytest.fixture
def session() -> Generator[Session, Any, None]:
    session = session_factory()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(autouse=True)
def clean_db(session) -> Generator[None, Any, None]:
    session.execute(
        text("""
            TRUNCATE TABLE employees, departments
            RESTART IDENTITY CASCADE
        """)
    )
    session.commit()
    yield
    session.execute(
        text("""
            TRUNCATE TABLE employees, departments
            RESTART IDENTITY CASCADE
        """)
    )
    session.commit()
    session.close()


@pytest.fixture
def service(session) -> Service:
    employee_repo = EmployeeRepo(session=session, model_cls=Employee)
    department_repo = DepartmentRepo(session=session, model_cls=Department)
    service = Service(
        repos=Repositories(
            employee=employee_repo,
            department=department_repo,
        )
    )
    return service
