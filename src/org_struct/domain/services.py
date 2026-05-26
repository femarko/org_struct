from datetime import datetime

from org_struct.domain.errors import (
    DepartmentNameConflict,
    DepartmentNotFound,
    DepartmentCycleError,
    EmployeeReassignmentError,
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
                f"Department with ID `{department_id}` does not exist"
            )
        return department

    def _build_tree(
          self,
          department: Department,
          depth: int = 1,
          current_depth: int = 1,
    ) -> dict:
        depth = max(1, min(depth, 5))
        result = {
            "id": department.id,
            "name": department.name,
            "parent_id": department.parent_id,
            "employees": [],
            "children": [],
        }
        if current_depth >= depth:
            return result
        employees = self.repos.employee.get_by_department_id(
            department_id=department.id
        )
        result["employees"] = [
            EmployeeDTO(
                id=employee.id,
                department_id=employee.department_id,
                full_name=employee.full_name,
                position=employee.position,
            )
            for employee in employees
        ]
        children = self.repos.department.get_children(
            parent_id=department.id
        )
        result["children"] = [
            self._build_tree(
                department=child,
                depth=depth,
                current_depth=current_depth + 1
            )
            for child in children
        ]
        return result

    def _avoid_department_cycle(
            self,
            department_id: int,
            new_parent_id: int,
    ) -> None:
        current_department_id = new_parent_id
        while current_department_id is not None:
            if current_department_id == department_id:
                raise DepartmentCycleError("Department cycle detected")
            new_parent = self._check_department_exists(current_department_id)
            current_department_id = new_parent.parent_id


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
        department =self._check_department_exists(department_id)
        tree: dict = self._build_tree(department, depth)
        result = TreeWithEmployeesDTO if include_employees else TreeDTO
        return result.model_validate(tree)

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
            raise EmployeeReassignmentError(
                f"`reassign_to_department_id` cannot be the same "
                f"as `department_id`"
            )
        employees = self.repos.employee.get_by_department_id(department_id)
        for employee in employees:
            employee.department_id = target_department.id
        children = self.repos.department.get_children(department_id)
        for child in children:
            child.parent_id = department.parent_id
        self.repos.department.delete(department)
