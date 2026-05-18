from ast import TypeVar

from pydantic import BaseModel

from org_struct.shared.validators import validate_string



class AddDepartmentRequest(BaseModel):
    name: str
    parent_id: int | None

    validate_name = validate_string("name")


class AddEmployeeRequest(BaseModel):
    full_name: str
    position: str
    department_id: int

    validate_full_name = validate_string("full_name")
    validate_position = validate_string("position")


class GetDepartment(BaseModel):
   depth: int
   include_employees: bool
 