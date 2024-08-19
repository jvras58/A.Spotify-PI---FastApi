from enum import Enum

from pydantic import BaseModel


class ArtistSchema(BaseModel):
    name: str
    followers: int
    popularity: int
    genre: str
    audit_user_ip: str = None
    audit_user_login: str = None

class ArtistList(BaseModel):
    """
    Representa uma lista de artistas no sistema.
    """

    artists: list[ArtistSchema]

class SpotifyType(str, Enum):
    artist = 'artist'
    album = 'album'
