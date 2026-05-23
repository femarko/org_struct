from typing import Generic
from datetime import datetime
from anyio.lowlevel import T
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from org_struct.domain.errors import DepartmentNotFound
from org_struct.domain.models import (
    T_Model,
    T_Department,
    T_Employee,
)
from org_struct.infrastructure.db.sqlalchemy_session import sqlalchemy_session



class BaseRepository(Generic[T_Model]):
    def __init__(
            self,
            session: sqlalchemy_session,
            model_cls: type[T_Model]
    ) -> None:
        self.session = session
        self.model_cls = model_cls

    def add(self, model: T_Model) -> T_Model:
        self.session.add(model)
        self.session.flush()
        return model

    def get_by_id(self, model_id: int) -> T_Model:
        result = self.session.get(self.model_cls, model_id)
        if result is None:
            raise DepartmentNotFound(
                f"Department with ID `{model_id}` does not exist."
            )
        return result

    def delete(self, model: T_Model) -> None:
        self.session.delete(model)


class DepartmentRepo(BaseRepository[T_Department]):
    def get_with_tree(
            self,
            department_id: int,
        ) -> T_Department | None:
        return (
            self.session.query(self.model_cls)
            .options(
                selectinload(self.model_cls.children),
                selectinload(self.model_cls.employees),
            )
            .filter(self.model_cls.id == department_id)
            .one()
        )

    def find_by_name_and_parent_id(
            self,
            name: str,
            parent_id: int
    ) -> int | None:
        stmt = select(self.model_cls.id).filter_by(
            name = name,
            parent_id = parent_id
        )
        return self.session.execute(stmt).scalar_one_or_none()


class EmployeeRepo(BaseRepository[T_Employee]): ...
