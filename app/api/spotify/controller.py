from sqlalchemy import select

from app.database.session import Session
from app.models.artist import Artist
from app.utils.base_model import AbstractBaseModel
from app.utils.generic_controller import GenericController


class ArtistController(GenericController):
    def __init__(self) -> None:
        super().__init__(Artist)

    def get_artist_by_name(self, db_session: Session, name: str) -> Artist:
        return db_session.scalar(select(Artist).where(Artist.name == name))

    def save(self, db_session: Session, obj: Artist) -> AbstractBaseModel:
        existe_artist = self.get_artist_by_name(db_session, obj.name)
        if existe_artist:
            if (
                existe_artist.followers != obj.followers
                or existe_artist.popularity != obj.popularity
            ):
                existe_artist.followers = obj.followers
                existe_artist.popularity = obj.popularity
                db_session.commit()
                return existe_artist
            else:
                return existe_artist
        return super().save(db_session, obj)
