from typing import (
    Generic,
    Sequence,
)
from sqlalchemy import select

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
    def find_by_name_and_parent_id(
            self,
            name: str,
            parent_id: int | None
    ) -> Sequence[int]:
        stmt = select(self.model_cls.id).filter_by(
            name = name,
            parent_id = parent_id
        )
        return self.session.execute(stmt).scalars().all()
    
    def get_children(
            self,
            parent_id: int
    ) -> Sequence[T_Department]:
        stmt = select(self.model_cls).filter_by(parent_id=parent_id)
        return self.session.execute(stmt).scalars().all()
        

class EmployeeRepo(BaseRepository[T_Employee]):
    def get_by_department_id(
            self,
            department_id: int,
    ) -> Sequence[T_Employee]:
        stmt = select(self.model_cls).filter_by(department_id = department_id)
        return self.session.execute(stmt).scalars().all()
