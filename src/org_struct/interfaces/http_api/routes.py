from re import S

from fastapi import (
    APIRouter,
    Depends
)

from org_struct.domain.services import Service
from org_struct.shared.request_dtos import (
    AddDepartmentRequest,
    AddEmployeeRequest,
    GetDepartmentRequest,
    MoveDepartmentRequest,
    DeleteDepartmentRequest,
)
from org_struct.shared.response_dtos import (
    DepartmentDTO,
    EmployeeDTO,
    TreeDTO,
    TreeWithEmployeesDTO,
)
from org_struct.shared.enums import DeletionMode
from org_struct.interfaces.http_api.dependencies import get_domain_service


departments_router = APIRouter(prefix="/departments", tags=["departments"])


@departments_router.post("/", status_code=201)
def add_department(
        data: AddDepartmentRequest,
        service: Service = Depends(get_domain_service),
) -> DepartmentDTO:
    return service.add_department(data.name, data.parent_id)


@departments_router.post("/{id}/employees", status_code=201)
def add_employee(
        id: int,
        data: AddEmployeeRequest,
        service: Service = Depends(get_domain_service),
) -> EmployeeDTO:
    data.department_id = id
    return service.add_employee(
        data.department_id,
        data.full_name,
        data.position,
        data.hired_at
    )


@departments_router.get("/{id}")
def get_department(
        id: int,
        depth: int = 1,
        include_employees: bool = True,
        service: Service = Depends(get_domain_service),
) -> TreeDTO | TreeWithEmployeesDTO:
    return service.get_department(
        id,
        depth,
        include_employees,
    )


@departments_router.patch("/{id}")
def move_department(
        id: int,
        data: MoveDepartmentRequest,
        service: Service = Depends(get_domain_service),
) -> DepartmentDTO:
    return service.move_department(
        id,
        data.new_parent_id,
    )


@departments_router.delete("/{id}", status_code=204)
def delete_department(
        id: int,
        mode: DeletionMode,
        reassign_to_department_id: int | None = None,
        service: Service = Depends(get_domain_service),
) -> None:
    data = DeleteDepartmentRequest(
        id=id,
        mode=mode,
        reassign_to_department_id=reassign_to_department_id
    )
    service.delete_department(
        id,
        reassign_to_department_id,
        mode,
    )
