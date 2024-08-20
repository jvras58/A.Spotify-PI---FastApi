from config.table_registry import table_registry
from sqlalchemy import Index
from sqlalchemy.orm import Mapped, mapped_column
from utils.base_model import AbstractBaseModel


@table_registry.mapped_as_dataclass
class User(AbstractBaseModel):
    """
    Representa a tabela Usuário no banco de dados.
    """

    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(
        name='id_user',
        primary_key=True,
        init=False,
        autoincrement=True,
        comment='Identificador do usuario.',
    )
    display_name: Mapped[str] = mapped_column(name='str_display_name')
    username: Mapped[str] = mapped_column(name='str_username')
    password: Mapped[str] = mapped_column(name='str_password')
    email: Mapped[str] = mapped_column(name='str_email')

    __table_args__ = (
        Index('idx_user_username', username, unique=True),
        Index('idx_user_email', email, unique=True),
    )

    def __init__(self, **kwargs: dict) -> None:
        """Initialize the model."""
        super().__init__(**kwargs)
        for attr, value in kwargs.items():
            setattr(self, attr, value)
