from org_struct.domain.errors import (
    DepartmentNameConflict,
    DepartmentNotFound,
    DepartmentCycleError,
)
from org_struct.domain.repo_interface import DepartmentRepoProto

from org_struct.domain.models import Department


def avoid_department_name_conflict(
          parent_id: int,
          name: str,
          repo: DepartmentRepoProto
) -> None:
        if repo.find_by_name_and_parent_id(
            name=name,
            parent_id=parent_id
        ):
            raise DepartmentNameConflict(
                "Department with same name and pareant_id already exists"
            )


def check_department_exists(
          department_id: int,
          repo: DepartmentRepoProto,
) -> Department:
        department = repo.get_by_id(department_id)
        if department is None:
            raise DepartmentNotFound(
                f"Department with ID `{department_id}` does not exist."
                f"Employee cannot be added"
            )
        return department
        

def limit_tree(
          department: Department,
          depth: int,
          current: int = 1,
) -> Department:
    
    depth = max(1, min(depth, 5))
    
    if current >= depth:
        department.children = []
        return department

    for child in department.children:
        limit_tree(child, depth, current + 1)
    
    return department


def check_department_cycle(
          department_id: int,
          new_parent_id: int,
          repo: DepartmentRepoProto
) -> None:
    current_department_id = new_parent_id
    while current_department_id is not None:
        if current_department_id == department_id:
            raise DepartmentCycleError("Department cycle detected")
        current_department_id = repo.get_by_parent_id(current_department_id)
