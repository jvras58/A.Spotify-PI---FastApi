from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    """
    Classe que representa qualque entidade no sistema.
    """

    pass


@dataclass
class AbstractBaseModel:
    """
    Classe abstrata que representa qualquer entidade que cinterá as propriedades base
    para se auditada.
    """

    __abstract__ = True

    audit_user_ip: Mapped[str] = mapped_column(String(16), name='audit_user_ip')
    audit_created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), name='audit_created_at'
    )
    audit_updated_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        name='audit_updated_on',
    )
    audit_user_login: Mapped[str] = mapped_column(name='audit_user_login')

    def __init__(self, **kwargs: dict) -> None:
        """Initialize the model."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)

    def _as_dict(self, jump_immutable_fields: bool = True) -> dict:
        """Return the model as a dictionary. Excludind audit attributes.

        This method is used to serialize the model to prepare it for update
        model.
        """
        # This fields are handled by the database.
        immutable_fields = ['audit_created_at', 'audit_updated_at']
        return {
            attr.key: getattr(self, attr.key)
            for attr in self.__mapper__.column_attrs
            if jump_immutable_fields and attr.key not in immutable_fields
        }

    def get_updated_data(self, obj: 'AbstractBaseModel') -> None:
        """Update the model with the new data."""
        for key, value in obj._as_dict().items():  # noqa: SLF001
            setattr(self, key, value)

    def __repr__(self) -> str:
        """Return the model representation."""
        return f'<{self.__class__.__name__} {self.id}>'
