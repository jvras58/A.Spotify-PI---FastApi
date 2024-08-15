from pydantic import BaseModel
from enum import Enum


class Client_auth(BaseModel):
    client_id: str
    client_secret: str


class SpotifyType(str, Enum):
    artist = "artist"
    album = "album"
