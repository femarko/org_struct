from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from org_struct.domain.models import (
    Department,
    Employee
)


class DepartmentRepoProto(Protocol):
    def add(self, model: Department) -> tuple[int, datetime]: ...

    def get_by_id(self, model_id: int) -> Department: ...

    def delete(self, model: Department) -> None: ...

    def get_with_tree(self, department_id: int) -> Department | None: ...

    def find_by_name_and_parent_id(
            self,
            name: str,
            parent_id: int
    ) -> int | None: ...

    def get_by_parent_id(self, parent_id: int) -> Department | None: ...


class EmployeeRepoProto(Protocol):
    def add(self, model: Employee) -> tuple[int, datetime]: ...
    def get_by_id(self, model_id: int) -> Employee: ...
    def delete(self, model: Employee) -> None: ...


@dataclass
class Repositories:
    department: DepartmentRepoProto
    employee: EmployeeRepoProto
