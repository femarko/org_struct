from datetime import datetime

from org_struct.domain.errors import (
    DepartmentNameConflict,
    DepartmentNotFound,
    DepartmentCycleError,
)
from org_struct.domain.repo_interface import Repositories
from org_struct.domain.models import (
    Department,
    Employee,
)
from org_struct.shared.response_dtos import (
    DepartmentDTO,
    EmployeeDTO,
    TreeDTO,
    TreeWithEmployeesDTO,
)
from org_struct.shared.enums import DeletionMode



class Service:
    def __init__(self, repos: Repositories) -> None:
        self.repos = repos

    def _avoid_department_name_conflict(
          self,
          parent_id: int | None,
          name: str,
    ) -> None:
        if self.repos.department.find_by_name_and_parent_id(
            name=name,
            parent_id=parent_id
        ):
            raise DepartmentNameConflict(
                f"Department with the same name and parent_id "
                f"or a top level department with the same name "
                f"already exists"
            )

    def _check_department_exists(
          self,
          department_id: int,
    ) -> Department:
        department = self.repos.department.get_by_id(department_id)
        if department is None:
            raise DepartmentNotFound(
                f"Department with ID `{department_id}` does not exist. "
                f"Employee cannot be added"
            )
        return department

    def _limit_tree(
          self,
          department: Department,
          depth: int,
          current: int = 1,
    ) -> Department:
        depth = max(1, min(depth, 5))
        if current >= depth:
            department.children = []
            return department
        for child in department.children:
            self._limit_tree(child, depth, current + 1)
        return department

    def _avoid_department_cycle(
            self,
            department_id: int,
            new_parent_id: int,
    ) -> None:
        current_department_id = new_parent_id
        while current_department_id is not None:
            if current_department_id == department_id:
                raise DepartmentCycleError("Department cycle detected")
            current_department_id = (
                self.repos.department.get_by_id(current_department_id)
                .parent_id
            )

    def add_department(
        self,
        name: str,
        parent_id: int | None = None,
    ) -> DepartmentDTO:
        self._avoid_department_name_conflict(
            parent_id,
            name,
        )
        department = Department(
            name=name,
            parent_id=parent_id,
        )
        department_with_id = self.repos.department.add(department)
        return DepartmentDTO.model_validate(department_with_id)

    def add_employee(
        self,
        department_id: int,
        full_name: str,
        position: str,
        hired_at: datetime | None = None
    ) -> EmployeeDTO:
        _ = self._check_department_exists(department_id)
        employee = Employee(
            department_id=department_id,
            full_name=full_name,
            position=position,
        )
        if hired_at is not None:
            employee.hired_at = hired_at
        employee_with_id = self.repos.employee.add(employee)
        return EmployeeDTO.model_validate(employee_with_id)
    
    def get_department(
        self,
        department_id: int,
        depth: int,
        include_employees: bool,
    ) -> TreeDTO | TreeWithEmployeesDTO:
        department =self.repos.department.get_with_tree(department_id)
        if department is None:
            raise DepartmentNotFound(
                f"Department with ID `{department_id}` does not exist."
            )
        department = self._limit_tree(department, depth)
        result = TreeWithEmployeesDTO if include_employees else TreeDTO
        return result.model_validate(department)

    def move_department(
        self,
        department_id: int,
        new_parent_id: int,
    ) -> DepartmentDTO:
        department = self._check_department_exists(department_id)
        self._avoid_department_cycle(
            department_id,
            new_parent_id,
        )
        department.parent_id = new_parent_id
        return DepartmentDTO.model_validate(department)

    def delete_department(
            self,
            department_id: int,
            reassign_to_department_id: int,
            mode: DeletionMode,
    ) -> None:
        department = self._check_department_exists(department_id)
        if mode == DeletionMode.CASCADE:
            self.repos.department.delete(department) 
            return
        target_department = self._check_department_exists(
            reassign_to_department_id
        )
        if target_department.id == department.id:
            raise ValueError(
                f"`reassign_to_department_id` cannot be the same "
                f"as `department_id`"
            )
        for employee in department.employees:
            employee.department = target_department
        for child in department.children:
            child.parent_id = department.parent_id
        self.repos.department.delete(department)
