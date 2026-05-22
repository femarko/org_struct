from datetime import datetime
from enum import StrEnum
from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
)
from typing import TypeVar



class StatusEnum(StrEnum):
    SUCCESS = "success"
    FAILED = "failed"


class MessageResponse(BaseModel):
    status: StatusEnum
    message: str


class DepartmentDTO(BaseModel):
    id: int
    name: str
    parent_id: int | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class EmployeeDTO(BaseModel):
    id: int
    department_id: int
    position: str
    full_name: str
    created_at: datetime

    class Config:
        from_attributes = True


class DepartmentTreeDTO(BaseModel):
    id: int
    name: str
    parent_id: int | None
    children: list["DepartmentTreeDTO"] = Field(default_factory=list)
    employees: list["EmployeeDTO"] = Field(default_factory=list)

    class Config:
        from_attributes = True


DepartmentTreeDTO.model_rebuild()


T_ResponseDTO = TypeVar(
    "T_ResponseDTO",
    bound=DepartmentDTO | EmployeeDTO | DepartmentTreeDTO | MessageResponse
)
