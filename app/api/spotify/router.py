from http import HTTPStatus
from typing import Annotated

import requests
from cachetools import TTLCache, cached
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.authentication.controller import get_current_user
from app.api.spotify.schemas import SpotifyType
from app.database.session import get_session
from app.models.user import User

router = APIRouter()

db_session_type = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]

token_cache = TTLCache(maxsize=1, ttl=3600)


@cached(cache=token_cache)
@router.get('/{spotify_type}/{spotify_search}')
def search_spotify_data_by_type(
    spotify_type: SpotifyType,
    spotify_search: str,
    current_user: CurrentUser,
):
    """
    Obtem informações do catálogo do Spotify sobre álbuns e artistas que correspondem a uma sequência de palavras-chave.
    """

    spotify_access_token = getattr(current_user, 'spotify_access_token', None)
    print(spotify_access_token)
    if not spotify_access_token:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Token do Spotify não encontrado.',
        )

    url = f'https://api.spotify.com/v1/search?q={spotify_search}&type={spotify_type.value}&limit=40'
    headers = {'Authorization': f'Bearer {spotify_access_token}'}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()
