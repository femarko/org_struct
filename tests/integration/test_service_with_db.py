from sqlalchemy import text

from org_struct.domain.models import (
    Department,
    Employee,
)
from org_struct.domain.services import Service
from org_struct.infrastructure.db.repositories import (
    EmployeeRepo,
    DepartmentRepo,
)
from org_struct.domain.repo_interface import Repositories
from org_struct.infrastructure.db.sqlalchemy_session import session_factory
from org_struct.shared.enums import DeletionMode



def test_add_department_saves_department_to_db(session, service) -> None:
    result = service.add_department(name="IT", parent_id=None)
    session.commit()

    with session_factory() as new_session:
        fetched = new_session.get(Department, result.id)

    assert fetched is not None
    assert result.name == fetched.name == "IT"
    assert result.parent_id == fetched.parent_id


def test_add_employee_saves_employee_to_db(session, service) -> None:
    stmt = text(
        """
        INSERT INTO departments (id, name, parent_id)
        VALUES (1, 'IT', NULL)
        """
    )
    session.execute(stmt)
    result = service.add_employee(
        department_id=1,
        full_name="John Doe",
        position="Dev"
    )
    session.commit()

    with session_factory() as new_session:
        fetched = new_session.get(Employee, result.id)

    assert fetched is not None
    assert result.department_id == fetched.department_id == 1
    assert result.position == fetched.position == "Dev"
    assert result.full_name == fetched.full_name == "John Doe"


def test_get_department_returns_department_with_tree(session, service):
    stmt1 = text(
        """
        INSERT INTO departments (id, name, parent_id)
        VALUES
            (1, 'IT', NULL),
            (2, 'Backend', 1)
        """
    )
    stmt2 = text(
        """
        INSERT INTO employees (id, department_id, full_name, position)
        VALUES
            (:id, :department_id, :full_name, :position)
        """
    )
    with session_factory() as new_session:
        new_session.execute(stmt1)
        new_session.execute(
            stmt2,
            {
                "id": 1,
                "department_id": 2,
                "full_name": "John Doe",
                "position": "Dev",
            }
        )
        new_session.commit()

    result = service.get_department(
        department_id=1,
        depth=5,
        include_employees=True,
    )
    result_dict = result.model_dump()
    expected = {
        "id": 1,
        "name": "IT",
        "parent_id": None,
        "employees": [],
        "children": [
            {
                "id": 2,
                "name": "Backend",
                "parent_id": 1,
                "employees": [
                    {
                        "id": 1,
                        "department_id": 2,
                        "full_name": "John Doe",
                        "position": "Dev",
                    }
                ],
                "children": []
 
            }
        ],
    }
    assert result_dict == expected


def test_cascade_deletion_removes_department_tree():
    ids = (1, 2, 3, 4)
    stmt1 = text(
        """
        INSERT INTO departments (id, name, parent_id)
        VALUES
            (1, 'IT', NULL),
            (2, 'Web', 1),
            (3, 'Backend', 2),
            (4, 'Frontend', 2)
        """
    )
    stmt2 = text(
        """
        INSERT INTO employees (id, department_id, full_name, position)
        VALUES
            (:id, :department_id, :full_name, :position)
        """
    )

    with session_factory() as new_session_1:
        new_session_1.execute(stmt1)
        for department_id in ids:
            new_session_1.execute(
                stmt2, {
                    "id": department_id,
                    "department_id": department_id,
                    "full_name": "John Doe",
                    "position": "Dev",
                }
        )
        new_session_1.commit()

    with session_factory() as new_session_2:
        s = Service(
            repos=Repositories(
                employee=EmployeeRepo(session=new_session_2, model_cls=Employee),
                department=DepartmentRepo(session=new_session_2, model_cls=Department),
            )   
        )
        s.delete_department(
            department_id=1,
            reassign_to_department_id=None,
            mode=DeletionMode.CASCADE,
        )
        new_session_2.commit()
    
    with session_factory() as new_session_3:
        fetched_departments = [new_session_3.get(Department, id) for id in ids]
        fetched_employees = [new_session_3.get(Employee, id) for id in ids]
    
    assert all(d is None for d in fetched_departments)
    assert all(e is None for e in fetched_employees)
