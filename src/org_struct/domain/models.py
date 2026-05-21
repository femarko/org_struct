from http import server
from typing import (
    Protocol,
    TypeVar,
)

from sqlalchemy import (
    Integer,
    String,
    DateTime,
    func,
    ForeignKey,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)
from datetime import datetime


class SQLAlchBaseModel(DeclarativeBase): ...


class Department(SQLAlchBaseModel):
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("departments.id", ondelete="CASCADE"),
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
        server_default=func.now()
    )
    parent = relationship(
        "Department",
        remote_side=[id],
        back_populates="children",
    )
    children = relationship(
        "Department",
        back_populates="parent",
        cascade="all, delete-orphan",
    )
    employees = relationship("Employee", back_populates="department")


class Employee(SQLAlchBaseModel):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    department_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("departments.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )  
    full_name: Mapped[str] = mapped_column(String(200), nullable=False)
    position: Mapped[str] = mapped_column(String(200), nullable=False)
    hired_at: Mapped[datetime] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
        server_default=func.now()
    )
    department = relationship("Department", back_populates="employees")


class DepartmentProto(Protocol):
    id: Mapped[int]
    name: Mapped[str]
    parent_id: Mapped[int | None]
    created_at: Mapped[datetime]
    parent: Mapped["Department"]
    children: Mapped[list["Department"]]
    employees: Mapped[list["Employee"]]


class EmployeeProto(Protocol):
    id: Mapped[int]
    department_id: Mapped[int]
    full_name: Mapped[str]
    position: Mapped[str]
    hired_at: Mapped[datetime]
    created_at: Mapped[datetime]


T_Model = TypeVar("T_Model", bound=DepartmentProto | EmployeeProto)
T_Department = TypeVar("T_Department", bound=DepartmentProto)
T_Employee = TypeVar("T_Employee", bound=EmployeeProto)
