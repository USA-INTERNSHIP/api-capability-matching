from typing import Any
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    id: Any

    @declared_attr
    def __tablename__(cls) -> str:
        if hasattr(cls, '__tablename__'):
            return cls.__tablename__
        return cls.__name__.lower()