from http import HTTPStatus
from typing import List, Annotated

import requests
from cachetools import TTLCache, cached
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.authentication.controller import get_current_user
from app.api.spotify.schemas import ArtistInfo, SpotifyType
from app.database.session import get_session
from app.models.user import User

router = APIRouter()

db_session_type = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]

token_cache = TTLCache(maxsize=1, ttl=3600)


@cached(cache=token_cache)
@router.get('/{spotify_type}/{spotify_search}', summary="Obter informações do catálogo do Spotify", response_model=dict)
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

@cached(cache=token_cache)
@router.get('/artists', response_model=List[ArtistInfo])
def get_artists_info(
    current_user: CurrentUser,
    artist_ids: List[str] = Query(..., description="Lista de IDs de artistas no Spotify"),
) -> List[ArtistInfo]:
    """
    Obtem informações processadas sobre uma lista de artistas usando seus IDs do Spotify.
    
    Retorna nome do artista, quantidade de seguidores e popularidade.
    
    - **artist_ids**: Uma lista de IDs de artistas no Spotify.
    """
    spotify_access_token = getattr(current_user, 'spotify_access_token', None)
    if not spotify_access_token:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Token do Spotify não encontrado.',
        )

    # FIXME: ponto morto isso nunca vai ser falso pois o Query obriga a passar as informações...
    if not artist_ids:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='É necessário fornecer pelo menos um ID de artista.',
        )

    ids_str = ','.join(artist_ids)
    url = f'https://api.spotify.com/v1/artists?ids={ids_str}'
    headers = {'Authorization': f'Bearer {spotify_access_token}'}

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        try:
            detail = response.json()
        except ValueError:
            detail = response.text
        raise HTTPException(status_code=response.status_code, detail=detail)

    data = response.json()
    artists_info = []

    for artist in data.get('artists', []):
        artist_info = {
            'name': artist.get('name'),
            'followers': artist.get('followers', {}).get('total'),
            'popularity': artist.get('popularity'),
        }
        artists_info.append(ArtistInfo(**artist_info))

    return artists_info
