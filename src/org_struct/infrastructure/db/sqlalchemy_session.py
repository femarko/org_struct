from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import (
    sessionmaker,
    Session as sqlalchemy_session,
)

from org_struct.config import get_settings



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
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
