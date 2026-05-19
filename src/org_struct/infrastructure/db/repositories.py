from typing import Generic
from datetime import datetime
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import NoResultFound as SQLAlchemyNoResultFound

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

    def add(self, model: T_Model) -> tuple[int, datetime]:
        self.session.add(model)
        self.session.flush()
        return model.id, model.created_at

    def get_by_id(self, model_id: int) -> T_Model | None:
        return self.session.get(self.model_cls, model_id)

    def delete(self, model: T_Model) -> None:
        self.session.delete(model)


class DepartmentRepo(BaseRepository[T_Department]):
    def get_with_tree(self, department_id: int) -> T_Department | None:
        return (
            self.session.query(self.model_cls)
            .options(
                selectinload(self.model_cls.children),
                selectinload(self.model_cls.employees),
            )
            .filter(self.model_cls.id == department_id)
            .one()
        )
    
    def get_by_parent_id(self, parent_id: int) -> T_Department | None:
        try:
            result = (
                self.session.query(self.model_cls)
                .filter(self.model_cls.parent_id == parent_id)
                .one()
            )
        except SQLAlchemyNoResultFound as e:
            raise DepartmentNotFound(
                f"Department with {parent_id=} does not exist"
            ) from e
        else:
            return result

    def find_by_name_and_parent_id(
            self,
            name: str,
            parent_id: int
    ) -> int | None:
        try:
            dep_fetched = self.session.query(self.model_cls).filter_by(
                name=name,
                parent_id=parent_id
            ).one()
        except SQLAlchemyNoResultFound as e:
            raise DepartmentNotFound(
                f"Department with {name=} name and {parent_id=} "
                f"does not exist"
            ) from e
        else:
            result = dep_fetched.id if dep_fetched else None
            return result


class EmployeeRepo(BaseRepository[T_Employee]): ...
