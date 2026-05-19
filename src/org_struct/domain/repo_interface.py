from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from anyio.lowlevel import T

from org_struct.domain.models import (
    T_Model,
    T_Department,
    T_Employee,
)



class RepoProto(Protocol[T_Model]):
    def add(self, model: T_Model) -> tuple[int, datetime]: ...
    def get_by_id(self, model_id: int) -> T_Model | None: ...
    def find_by_name_and_parent_id(
            self,
            name: str,
            parent_id: int
    ) -> int | None: ...
    def delete(self, model: T_Model) -> None: ...


class DepartmentRepoProto(RepoProto[T_Department]):
    def get_with_tree(self, department_id: int) -> T_Department | None: ...


class EmployeeRepoProto(RepoProto[T_Employee]): ...


@dataclass
class Repositories:
    department: DepartmentRepoProto
    employee: EmployeeRepoProto
