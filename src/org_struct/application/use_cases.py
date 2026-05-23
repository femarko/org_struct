from typing import Generic

from org_struct.domain.repo_interface import Repositories
from org_struct.domain.services import (
    check_department_exists,
    avoid_department_name_conflict,
    limit_tree,
    check_department_cycle,
)
from org_struct.domain.models import (
    Department,
    Employee,
)
from org_struct.domain.errors import DepartmentNotFound
from org_struct.shared.request_dtos import (
    AddDepartmentRequest,
    AddEmployeeRequest,
    GetDepartmentRequest,
    MoveDepartmentRequest,
    DeleteDepartmentRequest,
    DeletionMode,
)
from org_struct.shared.response_dtos import (
    DepartmentDTO,
    EmployeeDTO,
    DepartmentTreeDTO,
    T_ResponseDTO,
)



class BaseUseCase(Generic[T_ResponseDTO]):
    def __init__(self, repos: Repositories) -> None:
        self.repos = repos


    def execute(self, *args, **kwargs)-> T_ResponseDTO:
        raise NotImplementedError


class AddDepartment(BaseUseCase[DepartmentDTO]):
    def execute(self, data: AddDepartmentRequest) -> DepartmentDTO:
        if data.parent_id:
            avoid_department_name_conflict(
                data.parent_id,
                data.name,
                self.repos.department,
            )
        department = Department(
            name=data.name,
            parent_id=data.parent_id,
        )
        self.repos.department.add(department)
        return DepartmentDTO.model_validate(department)


class AddEmployee(BaseUseCase[EmployeeDTO]):
    def execute(self, data: AddEmployeeRequest) -> EmployeeDTO:
        _ = check_department_exists(data.department_id, self.repos.department)
        employee = Employee(
            department_id=data.department_id,
            full_name=data.full_name,
            position=data.position,
        )
        self.repos.employee.add(employee)
        return EmployeeDTO.model_validate(employee)


class GetDepartment(BaseUseCase[DepartmentTreeDTO]):
    def execute(self, data: GetDepartmentRequest) -> DepartmentTreeDTO:
        department =self.repos.department.get_with_tree(data.department_id)
        if department is None:
            raise DepartmentNotFound(
                f"Department with ID `{data.department_id}` does not exist."
            )
        department = limit_tree(department, data.depth)
        return DepartmentTreeDTO.model_validate(department)


class MoveDepartment(BaseUseCase[DepartmentDTO]):
    def execute(
            self,
            data: MoveDepartmentRequest,
        ) -> DepartmentDTO:
        department = check_department_exists(
            data.id,
            self.repos.department
        )
        check_department_cycle(
            data.id,
            data.new_parent_id,
            self.repos.department
        )
        department.parent_id = data.new_parent_id
        return DepartmentDTO.model_validate(department)
    

class DeleteDepartment(BaseUseCase):
    def execute(self, data: DeleteDepartmentRequest) -> None:
        department = check_department_exists(
            data.id,
            self.repos.department
        )

        if data.mode == DeletionMode.CASCADE:
            self.repos.department.delete(department) 
            return
        
        target_department = check_department_exists(
            data.reassign_to_department_id,
            self.repos.department
        )

        if target_department.id == department.id:
            raise ValueError(
                "`reassign_to_department_id` cannot be the same as `department_id`"
            )
        for employee in department.employees:
            employee.department_id = target_department.id

        for child in department.children:
            child.parent_id = department.parent_id
        self.repos.department.delete(department)
