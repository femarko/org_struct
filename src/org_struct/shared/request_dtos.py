from datetime import (
    datetime,
    timezone,
)

from pydantic import (
    BaseModel,
    Field,
    model_validator,
) 
from org_struct.shared.enums import DeletionMode
from org_struct.shared.validators import validate_string



class AddDepartmentRequest(BaseModel):
    name: str = Field(
        examples=["Sales"]
    )
    parent_id: int | None = Field(
        default=None,
        examples=[1]
    )

    validate_name = validate_string("name")


class AddEmployeeRequest(BaseModel):
    full_name: str
    position: str
    department_id: int | None = None
    hired_at: datetime | None = Field(
        default=datetime.now(timezone.utc),
        examples=[None]
    )

    validate_full_name = validate_string("full_name")
    validate_position = validate_string("position")

    model_config = {
        "json_schema_extra": {
            "example": {
                "full_name": "John Doe",
                "position": "Sales Manager",
                "hired_at": "2022-01-01T00:00:00Z"
            }
        }
    }


class GetDepartmentRequest(BaseModel):
   department_id: int
   depth: int
   include_employees: bool
 

class MoveDepartmentRequest(BaseModel):
    name: str | None = None
    new_parent_id: int | None = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "new_parent_id": 2
            }
        }
    }


class DeleteDepartmentRequest(BaseModel):
    id: int
    mode: DeletionMode
    reassign_to_department_id: int | None
    
    @model_validator(mode="after")
    def validate_reassign(self):
        if self.mode == DeletionMode.REASSIGN and self.reassign_to_department_id is None:
            raise ValueError("`reassign_to_department_id` is missing")
        return self
