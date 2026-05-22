from fastapi import (
    APIRouter,
    Depends
)

from org_struct.application.use_cases import (
    AddDepartment,
    AddEmployee,
    GetDepartment,
    MoveDepartment,
    DeleteDepartment,
)
from org_struct.shared.request_dtos import (
    AddDepartmentRequest,
    AddEmployeeRequest,
    GetDepartmentRequest,
    MoveDepartmentRequest,
    DeletionMode,
    DeleteDepartmentRequest,
)
from org_struct.shared.response_dtos import (
    DepartmentDTO,
    EmployeeDTO,
    DepartmentTreeDTO,
    MessageResponse,
)
from org_struct.interfaces.http_api.dependencies import (
    get_add_department_use_case,
    get_add_employee_use_case,
    get_get_department_use_case,
    get_move_department_use_case,
    get_delete_department_use_case,
)


router = APIRouter()


@router.post("/departments", status_code=201)
def add_department(
        data: AddDepartmentRequest,
        add_department_use_case: AddDepartment = Depends(get_add_department_use_case),
) -> DepartmentDTO:
    return add_department_use_case.execute(data=data)


@router.post("/departments/{id}/employees", status_code=201)
def add_employee(
        id: int,
        data: AddEmployeeRequest,
        add_employee_use_case: AddEmployee = Depends(get_add_employee_use_case),
) -> EmployeeDTO:
    data.department_id = id
    return add_employee_use_case.execute(data=data)


@router.get("/departments/{id}")
def get_department(
        id: int,
        depth: int = 1,
        include_employees: bool = True,
        get_department_use_case: GetDepartment = Depends(get_get_department_use_case),
) -> DepartmentTreeDTO:
    data = GetDepartmentRequest(
        department_id=id,
        depth=depth,
        include_employees=include_employees
    )
    return get_department_use_case.execute(data=data)


@router.patch("/departments/{id}")
def move_department(
        id: int,
        data: MoveDepartmentRequest,
        move_department_use_case: MoveDepartment = Depends(get_move_department_use_case),
) -> DepartmentDTO:
    data.id = id
    return move_department_use_case.execute(data=data)


@router.delete("/departments/{id}", status_code=204)
def delete_department(
        id: int,
        mode: DeletionMode,
        reassign_to_department_id: int | None = None,
        delete_department_use_case: DeleteDepartment = Depends(get_delete_department_use_case),
):
    data = DeleteDepartmentRequest(
        id=id,
        mode=mode,
        reassign_to_department_id=reassign_to_department_id
    )
    return delete_department_use_case.execute(data=data)
