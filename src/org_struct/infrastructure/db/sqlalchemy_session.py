from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.exc import (
    SQLAlchemyError,
    IntegrityError,
) 
from sqlalchemy.orm import (
    sessionmaker,
    Session as sqlalchemy_session,
)

from org_struct.config import get_settings
from org_struct.domain.errors import (
    ORMError,
    ORMIntegrityError,
)



type SessionFactory = sessionmaker[sqlalchemy_session]
engine = create_engine(get_settings().db_url)
session_factory = sessionmaker[sqlalchemy_session](
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_session() -> Generator[sqlalchemy_session, None, None]:
    session = session_factory()
    try:
        yield session
        session.commit()
    except IntegrityError as e:
        session.rollback()
        raise ORMIntegrityError("Constraint violation") from e
    except SQLAlchemyError as e:
        session.rollback()
        raise ORMError("Database operation failed") from e
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
