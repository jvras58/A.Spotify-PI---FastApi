from enum import Enum

from pydantic import BaseModel


class ArtistSchema(BaseModel):
    name: str
    followers: int
    popularity: int
    genre: str
    audit_user_ip: str = None
    audit_user_login: str = None

    class Config:
        from_attributes = True


class ArtistList(BaseModel):
    """
    Representa uma lista de artistas no sistema.
    """

    artists: list[ArtistSchema]


class GeneroSchema(BaseModel):
    genre: str
    count: int


class TopGenresdict(BaseModel):
    """
    Representa lista de top 5 generos no sistema.
    """

    top_genres: list[GeneroSchema]


class SpotifyType(str, Enum):
    artist = 'artist'
    album = 'album'

class OrderType(str, Enum):
    followers = "followers"
