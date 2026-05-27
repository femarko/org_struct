import pytest

from org_struct.shared.enums import DeletionMode
from org_struct.shared.response_dtos import (
    DepartmentDTO,
    EmployeeDTO,
)
from org_struct.domain.errors import (
    DepartmentNameConflict,
    DepartmentCycleError,
    DepartmentNotFound,
    EmployeeReassignmentError,
)



@pytest.mark.parametrize(
    "parent_id",
    [None, 3]
)
def test_add_department_creates_root_or_child_department_depending_on_parent_id_argument(service, parent_id):
    svc, repos = service
    result: DepartmentDTO = svc.add_department(name="Backend", parent_id=parent_id)
    assert result.id == 1
    assert result.name == "Backend"
    assert result.parent_id == parent_id
    assert result.created_at is not None


@pytest.mark.parametrize(
    "parent_id, name",
    [
        (None, "Backend"),
        (3, "Backend"),
    ]
)
def test_departments_with_same_names_and_parent_ids_are_not_allowed(service, parent_id, name):
    svc, _ = service
    svc.add_department(name=name, parent_id=parent_id)
    with pytest.raises(DepartmentNameConflict) as e:
        svc.add_department(name="Backend", parent_id=parent_id)
    assert str(e.value) == (
        "Department with the same name and parent_id or a top level department "
        "with the same name already exists"
    )


def test_add_employee_creates_employee(service):
    svc, _ = service
    dept = svc.add_department(name="Backend")
    result: EmployeeDTO = svc.add_employee(
        department_id=dept.id,
        full_name="John Doe",
        position="Dev"
    )
    assert isinstance(result.id, int)
    assert result.department_id == dept.id
    assert result.position == "Dev"
    assert result.full_name == "John Doe"
    assert result.created_at is not None


def test_cannot_add_employee_to_non_existing_department(service):
    svc, _ = service
    wrong_department_id = 999
    with pytest.raises(DepartmentNotFound) as e:
        svc.add_employee(
            department_id=wrong_department_id,
            full_name="John",
            position="Dev"
        )
    assert str(e.value) == (
        f"Department with ID `{wrong_department_id}` does not exist"
    )


def test_cannot_move_department_under_its_child(service):
    svc, _ = service
    root = svc.add_department("Root")
    child = svc.add_department("Child", parent_id=root.id)
    with pytest.raises(DepartmentCycleError) as e:
        svc.move_department(
            department_id=root.id,
            new_parent_id=child.id
        )
    assert str(e.value) == "Department cycle detected"


def test_cascade_deletion_removes_department(service):
    """
    Verifies service-level deletion flow.
    ORM cascade behavior is covered by integration tests.
    """
    svc, repos = service
    root_dept = svc.add_department("Root")
    svc.delete_department(
        department_id=root_dept.id,
        mode=DeletionMode.CASCADE,
        reassign_to_department_id=None,
    )
    assert repos.department.data.get(root_dept.id) is None


def test_reassigning_deletion_reassigns_employees_and_removes_department(service):
    svc, repos = service
    d1 = svc.add_department("A")
    d2 = svc.add_department("B")
    svc.add_employee(
        department_id=d1.id,
        full_name="John",
        position="Dev"
    )
    svc.delete_department(
        department_id=d1.id,
        reassign_to_department_id=d2.id,
        mode=DeletionMode.REASSIGN,
    )
    employee = repos.employee.data[0]
    assert employee.department_id == d2.id


def test_reassigning_deletion_moves_children_to_parent_department(service):
    svc, repos = service
    department_with_id_1 = svc.add_department("A")
    department_with_id_2 = svc.add_department("B", parent_id=department_with_id_1.id)
    department_with_id_3 = svc.add_department("C", parent_id=department_with_id_2.id)
    svc.delete_department(
        department_id=department_with_id_2.id,
        reassign_to_department_id=department_with_id_1.id,
        mode=DeletionMode.REASSIGN,
    )
    assert repos.department.data[3].parent_id == department_with_id_1.id

def test_cannot_reassign_employees_to_department_being_deleted(service):
    svc, _ = service
    d1 = svc.add_department("A")
    with pytest.raises(EmployeeReassignmentError) as e:
        svc.delete_department(
            department_id=d1.id,
            reassign_to_department_id=d1.id,
            mode=DeletionMode.REASSIGN,
        )
    assert str(e.value) == (
        "`reassign_to_department_id` cannot be the same as `department_id`"
    )


def test_move_department_changes_parent_id(service):
    svc, _ = service
    d1 = svc.add_department("A")
    d2 = svc.add_department("B")
    d1_moved = svc.move_department(
        department_id=d1.id,
        new_parent_id=d2.id
    )
    assert d1_moved.parent_id == d2.id


def test_get_department_returns_department_with_tree(service):
    svc, _ = service
    d1 = svc.add_department("A")
    d2 = svc.add_department("B", parent_id=d1.id)
    e2 = svc.add_employee(
        department_id=d2.id,
        full_name="John",
        position="Dev"
    )
    result = svc.get_department(
        department_id=d1.id,
        depth=5,
        include_employees=False,
    )
    result_dict = result.model_dump()
    expected = {
        "id": d1.id,
        "name": d1.name,
        "parent_id": d1.parent_id,
        "children": [
            {
                "id": d2.id,
                "name": d2.name,
                "parent_id": d2.parent_id,
                "children": []
            }
        ]
        }
    assert result_dict == expected
