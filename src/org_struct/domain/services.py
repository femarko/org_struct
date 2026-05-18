from org_struct.domain.errors import (
    DepartmentNameConflict,
    DepartmentNotFound,
)
from org_struct.domain.repo_interface import RepoProto
from org_struct.domain.models import Department


def avoid_department_name_conflict(
            parent_id: int,
            name: str,
            repo: RepoProto
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
            repo: RepoProto,
            return_department: bool = False,
) -> Department | None:
        department = repo.get_by_id(department_id)
        if department is None:
            raise DepartmentNotFound(
                f"Department with ID `{department_id}` does not exist."
                f"Employee cannot be added"
            )
        if return_department:
            return department
