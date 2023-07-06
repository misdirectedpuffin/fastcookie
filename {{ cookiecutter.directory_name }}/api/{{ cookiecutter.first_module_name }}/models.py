from decimal import Decimal, getcontext
import re
from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_method
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
    relationship,
)

getcontext().prec = 8
class DbModel(DeclarativeBase):
    """Declarative base"""

    __abstract__ = True

    @classmethod
    def to_snake_case(cls) -> str:
        """PascalCase string as snake case"""
        name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", cls.__name__)
        name = re.sub("__([A-Z])", r"_\1", name)
        name = re.sub("([a-z0-9])([A-Z])", r"\1_\2", name)
        name = re.sub(r"(\d+)", r"_\1", name)
        return name.lower()

    # Generate __tablename__ automatically
    @declared_attr.directive
    def __tablename__(cls) -> str:
        """Autogenerate table name."""
        return cls.to_snake_case()

    def as_dict(self) -> dict:
        """Return a dict representation of the object."""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class {{cookiecutter.first_model_name}}(DbModel):

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    start: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
    end: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
    expired: Mapped[bool] = mapped_column(Boolean, nullable=True, default=False)
    deleted: Mapped[bool] = mapped_column(Boolean, nullable=True, default=False)

