from dataclasses import dataclass
from datetime import datetime
from typing import (
    Protocol,
    Sequence,
)

from org_struct.domain.models import (
    Department,
    Employee
)


class DepartmentRepoProto(Protocol):
    def add(self, model: Department) -> Department: ...
    def get_by_id(self, model_id: int) -> Department: ...
    def delete(self, model: Department) -> None: ...
    def find_by_name_and_parent_id(
            self,
            name: str,
            parent_id: int | None
    ) -> Sequence[int]: ...
    def get_children(self, parent_id: int) -> Sequence[Department]: ...


class EmployeeRepoProto(Protocol):
    def add(self, model: Employee) -> Employee: ...
    def get_by_id(self, model_id: int) -> Employee: ...
    def delete(self, model: Employee) -> None: ...
    def get_by_department_id(
            self,
            department_id: int
    ) -> Sequence[Employee]: ...


@dataclass
class Repositories:
    department: DepartmentRepoProto
    employee: EmployeeRepoProto
