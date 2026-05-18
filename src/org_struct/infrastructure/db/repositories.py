from typing import Generic
from datetime import datetime

from anyio.lowlevel import T

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

    def add(self, model: T_Model) -> tuple[int, datetime]:
        self.session.add(model)
        self.session.flush()
        return model.id, model.created_at

    def get_by_id(self, model_id: int) -> T_Model | None:
        return self.session.get(self.model_cls, model_id)
    
    def find_by_name_and_parent_id(
            self,
            name: str,
            parent_id: int
    ) -> int | None:
        dep_fetched = self.session.query(self.model_cls).filter_by(
            name=name,
            parent_id=parent_id
        ).one()
        result = dep_fetched.id if dep_fetched else None
        return result

    def delete(self, model: T_Model) -> None:
        self.session.delete(model)


class DepartmentRepo(BaseRepository[T_Department]): ...


class EmployeeRepo(BaseRepository[T_Employee]): ...
