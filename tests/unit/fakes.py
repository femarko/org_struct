from datetime import (
    datetime,
    timezone,
)
from typing import Any

from org_struct.domain.models import (
    Department,
    Employee,
)



class FakeDepartmentRepo:
    def __init__(self):
        self.data = {}

    def add(self, dept) -> Any:
        dept.id = len(self.data) + 1
        dept.created_at = datetime.now(timezone.utc)
        self.data[dept.id] = dept
        return dept

    def get_by_id(self, id) -> Any | None:
        return self.data.get(id)

    def delete(self, dept) -> None:
        self.data.pop(dept.id, None)

    def find_by_name_and_parent_id(self, name, parent_id) -> bool:
        return any(
            d.name == name and d.parent_id == parent_id
            for d in self.data.values()
        )

    def get_children(self, parent_id) -> list[Any]:
        return [
            d
            for d in self.data.values()
            if d.parent_id == parent_id
        ]


class FakeEmployeeRepo:
    def __init__(self):
        self.data = []

    def add(self, emp) -> Any:
        emp.id = len(self.data) + 1
        emp.created_at = datetime.now(timezone.utc)
        emp.department = Department(id=1, name="Root")
        emp.department.id = 1
        self.data.append(emp)
        return emp

    def get_by_department_id(self, department_id) -> list[Any]:
        return [
            e
            for e in self.data
            if e.department_id == department_id
        ]

    def delete(self, emp) -> None:
        self.data.remove(emp)
