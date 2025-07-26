from typing import Generator
from sqlalchemy.engine import Engine
from sqlmodel import create_engine, Session
from .config import settings


def engine() -> Engine:
    return create_engine(settings().database_url)


def get_session() -> Generator[Session, None, None]:
    with Session(engine()) as session:
        yield session
