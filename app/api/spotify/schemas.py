from pydantic import BaseModel
from enum import Enum

class response_token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

class Client_auth(BaseModel):
    client_id: str
    client_secret: str


class SpotifyType(str, Enum):
    artist = "artist"
    album = "album"
