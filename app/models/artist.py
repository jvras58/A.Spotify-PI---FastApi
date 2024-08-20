from config.table_registry import table_registry
from sqlalchemy.orm import Mapped, mapped_column
from utils.base_model import AbstractBaseModel


@table_registry.mapped_as_dataclass
class Artist(AbstractBaseModel):
    """
    Representa a tabela Artistas no banco de dados.
    """

    __tablename__ = 'Artists'
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(primary_key=True, name='id')
    artist_id: Mapped[str] = mapped_column(name='id_artista')
    name: Mapped[str] = mapped_column(name='str_username')
    genre: Mapped[str] = mapped_column(name='genero')
    followers: Mapped[str] = mapped_column(name='qntd_seguidores')
    popularity: Mapped[str] = mapped_column(name='popularidade')

    def __init__(self, **kwargs: dict) -> None:
        """Initialize the model."""
        super().__init__(**kwargs)
        for attr, value in kwargs.items():
            setattr(self, attr, value)
