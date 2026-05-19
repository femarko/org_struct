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


class GetDepartmentRequest(BaseModel):
   department_id: int
   depth: int
   include_employees: bool
 
class MoveDepartmentRequest(BaseModel):
    department_id: int
    new_parent_id: int
