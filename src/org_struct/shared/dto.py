from pydantic_core import PydanticCustomError
from pydantic import (
    BaseModel,
    field_validator,
    ValidationError,
    ValidationInfo,
)

from org_struct.domain.errors import IncorrectData



def validate_string(field_name: str):
    @field_validator(field_name)
    @classmethod
    def _validator(cls, value: str, info: ValidationInfo) -> str:
        value = value.strip()
        if not value:
            raise ValueError(f"{info.field_name} cannot be empty")
        if len(value) > 200:
            raise ValueError(
                f"`{info.field_name}` cannot be longer than 200 characters"
            )
        return value
    return _validator


class DepartmentDTO(BaseModel):
    name: str
    parent_id: int | None

    validate_name = validate_string("name")


class EmployeeDTO(BaseModel):
    full_name: str
    position: str
    department_id: int

    validate_full_name = validate_string("full_name")
    validate_position = validate_string("position")
