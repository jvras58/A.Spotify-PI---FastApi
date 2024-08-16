from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.utils.base_model import AbstractBaseModel




class Result(AbstractBaseModel):
    """
    Representa a tabela Result no banco de dados.
    """

    __tablename__ = 'results'

    id: Mapped[int] = mapped_column(primary_key=True, name='id')
    search: Mapped[str] = mapped_column(index=True,name='search')
    search_type: Mapped[str] = mapped_column(index=True, name='search_type')
    result: Mapped[JSON] = mapped_column(index=True, name='result')
