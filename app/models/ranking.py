from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column

from utils.base_model import AbstractBaseModel


class Ranking(AbstractBaseModel):
    """
    Representa a tabela Ranking no banco de dados.
    """

    __tablename__ = 'Rankings'

    id: Mapped[int] = mapped_column(primary_key=True, name='id')
    genre_ranking: Mapped[dict] = mapped_column(JSON, name='ranking_genero')
    top_genre_ranking: Mapped[dict] = mapped_column(JSON, name='ranking_top_genero')
