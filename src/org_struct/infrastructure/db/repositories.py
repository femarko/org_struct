from typing import (
    Generic,
    Protocol,
    TypeVar,
)

from org_struct.infrastructure.db.sqlalchemy_session import sqlalchemy_session


class HasID(Protocol):
    id: int


T_Model = TypeVar("T_Model", bound=HasID)


class BaseRepository(Generic[T_Model]):
    def __init__(
            self,
            session: sqlalchemy_session,
            model_cls: type[T_Model]
    ) -> None:
        self.session = session
        self.model_cls = model_cls

    def add(self, model: T_Model) -> int:
        self.session.add(model)
        self.session.flush()
        return model.id

    def get_by_id(self, model_id: int) -> T_Model | None:
        return self.session.get(self.model_cls, model_id)

    def delete(self, model: T_Model) -> None:
        self.session.delete(model)


class DepartmentRepo(BaseRepository): ...


class EmployeeRepo(BaseRepository): ...
