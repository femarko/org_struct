from enum import StrEnum

from pydantic import BaseModel, model_validator 
from org_struct.shared.validators import validate_string



class AddDepartmentRequest(BaseModel):
    name: str
    parent_id: int | None = None

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


class DeletionMode(StrEnum):
    CASCADE = "cascade"
    REASSIGN = "reassign"


class DeleteDepartmentRequest(BaseModel):
    department_id: int
    mode: DeletionMode
    reassign_to_department_id: int | None
    
    @model_validator(mode="after")
    def validate_reassign(self):
        if self.mode == DeletionMode.REASSIGN and self.reassign_to_department_id is None:
            raise ValueError("`reassign_to_department_id` is missing")
        return self
