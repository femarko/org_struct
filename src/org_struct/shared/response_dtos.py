from datetime import (
    datetime,
    timezone,
)
from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
)
from typing import TypeVar


class DepartmentDTO(BaseModel):
    id: int = Field(examples=[42])
    name: str = Field(examples=["Sales"])
    parent_id: int | None = Field(examples=[1])
    created_at: datetime = Field(
        default=datetime.now(timezone.utc),
        examples=["2022-01-01T00:00:00Z"]
    )

    model_config = ConfigDict(from_attributes=True)


class EmployeeDTO(BaseModel):
    id: int = Field(examples=[3])
    department_id: int = Field(examples=[42])
    position: str = Field(examples=["Sales Manager"])
    full_name: str = Field(examples=["John Doe"])
    created_at: datetime = Field(
        default=datetime.now(timezone.utc),
        examples=["2022-01-01T00:00:00Z"]
    )

    class Config:
        from_attributes = True


class TreeDTO(BaseModel):
    id: int
    name: str
    parent_id: int | None
    children: list["TreeDTO"] = Field(default_factory=list)

    class Config:
        from_attributes = True
        extra = "ignore"
        json_schema_extra = {
            "example": {
                "id": 42,
                "name": "Sales",
                "parent_id": None,
                "children": [
                    {
                        "id": 43,
                        "name": "Wholesale",
                        "parent_id": 42,
                        "children": []
                    }
                ]
            }
        }


class TreeWithEmployeesDTO(BaseModel):
    id: int
    name: str
    parent_id: int | None
    employees: list["EmployeeDTO"] = Field(default_factory=list)
    children: list["TreeWithEmployeesDTO"] = Field(default_factory=list)


    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 42,
                "name": "Sales",
                "parent_id": None,
                "employees": [
                    {
                        "id": 3,
                        "department_id": 42,
                        "position": "Sales Manager",
                        "full_name": "John Doe",
                        "created_at": "2022-01-01T00:00:00Z"
                    }
                ],
                "children": [
                    {
                        "id": 43,
                        "name": "Wholesale",
                        "parent_id": 42,
                        "employees": [
                            {
                                "id": 2,
                                "department_id": 43,
                                "position": "Wholesaler",
                                "full_name": "Jack Trader",
                                "created_at": "2026-05-21T16:47:40.815396Z"
                            }
                        ],
                        "children": []
                    }
                ]
            }
        }


TreeDTO.model_rebuild()


TreeWithEmployeesDTO.model_rebuild()


T_ResponseDTO = TypeVar(
    "T_ResponseDTO",
    bound=DepartmentDTO | EmployeeDTO | TreeDTO | TreeWithEmployeesDTO
)
