from sqlalchemy.orm import Mapped, mapped_column

from app.utils.base_model import AbstractBaseModel


class Artist(AbstractBaseModel):
    """
    Representa a tabela Artistas no banco de dados.
    """

    __tablename__ = 'Artists'

    id: Mapped[int] = mapped_column(primary_key=True, name='id')
    artist_id: Mapped[str] = mapped_column(name='id_artista')
    name: Mapped[str] = mapped_column(name='str_username')
    genre: Mapped[str] = mapped_column(name='genero')
    followers: Mapped[str] = mapped_column(name='qntd_seguidores')
    popularity: Mapped[str] = mapped_column(name='popularidade')
