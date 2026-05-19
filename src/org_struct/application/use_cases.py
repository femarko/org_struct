from typing import Generic

from org_struct.domain.repo_interface import Repositories
from org_struct.domain.services import (
    check_department_exists,
    avoid_department_name_conflict,
    limit_tree,
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
        department_id, created_at = self.repos.department.add(department)
        return DepartmentDTO(
            department_id=department_id,
            name=department.name,
            parent_id=department.parent_id,
            created_at=created_at,
        )


class AddEmployee(BaseUseCase[EmployeeDTO]):
    def execute(self, data: AddEmployeeRequest) -> EmployeeDTO:
        _ = check_department_exists(data.department_id, self.repos.department)
        employee = Employee(
            department_id=data.department_id,
            full_name=data.full_name,
            position=data.position,
        )
        employee_id, created_at = self.repos.employee.add(employee)
        return EmployeeDTO(
            employee_id=employee_id,
            department_id=employee.department_id,
            position=employee.position,
            full_name=employee.full_name,
            created_at=created_at,
        )


class GetDepartment(BaseUseCase[DepartmentTreeDTO]):
    def execute(self, data: GetDepartmentRequest) -> DepartmentTreeDTO:
        department =self.repos.department.get_with_tree(data.department_id)
        if department is None:
            raise DepartmentNotFound(
                f"Department with ID `{data.department_id}` does not exist."
            )
        department = limit_tree(department, data.depth)
        return DepartmentTreeDTO.model_validate(department)

