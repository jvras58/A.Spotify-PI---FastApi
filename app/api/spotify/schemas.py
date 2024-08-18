from enum import Enum

from pydantic import BaseModel


class ArtistInfo(BaseModel):
    name: str
    followers: int
    popularity: int
    audit_user_ip: str = None
    audit_user_login: str = None

class SpotifyType(str, Enum):
    artist = 'artist'
    album = 'album'
