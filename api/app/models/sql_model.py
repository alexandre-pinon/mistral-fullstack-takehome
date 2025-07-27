from sqlmodel import SQLModel as _SQLModel
from sqlalchemy import Enum
from pydantic.alias_generators import to_snake
from sqlalchemy.orm import declared_attr
from uuid import uuid4, UUID
from datetime import datetime
from sqlmodel import Field, Column

from .domain_model import Role


class SQLModel(_SQLModel):
    @declared_attr
    def __tablename__(cls) -> str:
        return to_snake(cls.__name__) + "s"


class ChatMessage(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    role: Role = Field(sa_column=Column(Enum(Role)))
    content: str
    created_at: datetime = Field(default_factory=datetime.now, index=True)
