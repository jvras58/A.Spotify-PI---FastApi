from fastapi import APIRouter, HTTPException, Depends
import requests
from app.api.spotify.schemas import response_token, SpotifyType
from app.utils.settings import get_settings
from typing import Annotated
from sqlalchemy.orm import Session
from app.database.session import get_session
from cachetools import TTLCache, cached

router = APIRouter()

db_session_type = Annotated[Session, Depends(get_session)]

# Cache para armazenar o token por um período limitado (ex: 3600 segundos)
token_cache = TTLCache(maxsize=1, ttl=3600)

@cached(cache=token_cache)
@router.post("/token", response_model=response_token)
def get_spotify_api_token():
    """
    Solicitar token de API do Spotify

    Usaremos este token de acesso ao portador para fazer login em outras APIs do Spotify
    Documentação atual do Spotify:
    https://developer.spotify.com/documentation/general/guides/authorization-guide/#client-credentials-flow
    """
    url = "https://accounts.spotify.com/api/token"
    spotify_client_data = {
        "grant_type": "client_credentials",
        "client_id": get_settings().CLIENT_ID, 
        "client_secret": get_settings().CLIENT_SECRET
    }
    response = requests.post(url, data=spotify_client_data)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()

@router.get("/{spotify_type}/{spotify_search}")
def search_spotify_data_by_type(
    spotify_type: SpotifyType,
    spotify_search: str,
):
    """
    Obtem informações do catálogo do Spotify sobre álbuns e artistas que correspondem a uma sequência de palavras-chave.
    Requer autenticação
    """

    # Obter o token de acesso
    token_response = get_spotify_api_token()
    access_token = token_response["access_token"]

    url = f"https://api.spotify.com/v1/search?q={spotify_search}&type={spotify_type.value}&limit=40"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()
