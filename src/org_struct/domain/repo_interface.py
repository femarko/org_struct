from dataclasses import dataclass
from datetime import datetime
from sqlalchemy.orm import Mapped
from typing import (
    Protocol,
    TypeVar,
)



class DepartmentProto(Protocol):
    id: Mapped[int]
    name: Mapped[str]
    parent_id: Mapped[int | None]
    created_at: Mapped[datetime]


class EmployeeProto(Protocol):
    id: Mapped[int]
    department_id: Mapped[int]
    full_name: Mapped[str]
    position: Mapped[str]
    hired_at: Mapped[datetime]


T_Model = TypeVar("T_Model", bound=DepartmentProto | EmployeeProto)


class RepoProto(Protocol):
    def add(self, model: T_Model) -> int: ...
    def get_by_id(self, model_id: int) -> T_Model | None: ...
    def find_by_name_and_parent_id(
            self,
            name: str,
            parent_id: int
    ) -> int | None: ...
    def delete(self, model: T_Model) -> None: ...


@dataclass
class Repositories:
    department: RepoProto
    employee: RepoProto
