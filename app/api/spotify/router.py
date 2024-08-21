from collections import Counter
from http import HTTPStatus
from typing import Annotated, List, Optional

from api.authentication.controller import get_current_user
from api.spotify.controller import ArtistController
from api.spotify.schemas import (
    ArtistList,
    ArtistSchema,
    OrderType,
    SpotifyType,
    TopGenresdict,
)
from database.session import get_session
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from models.artist import Artist
from models.user import User
from sqlalchemy.orm import Session
from utils.exceptions import IntegrityValidationException

router = APIRouter()
artist_controller = ArtistController()

db_session_type = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get('/', response_model=ArtistList)
def read_artists(
    db_session: db_session_type,
    skip: int = 0,
    limit: int = 100,
    genre: Optional[str] = Query(None),
    order_by: Optional[OrderType] = Query(None),
):
    """
    Retorna uma lista de artistas do banco de dados.
    Pode ser filtrada por gênero e/ou ordenada por número de seguidores[followers].
    """
    criterias = {}
    if genre:
        criterias['genre'] = genre

    order = None
    if order_by == OrderType.followers:
        order = 'followers DESC'

    artists: list[Artist] = artist_controller.get_all(
        db_session, skip, limit, order=order, **criterias
    )

    return {'artists': artists}


@router.get('/top5', response_model=TopGenresdict)
def read_ranking_generos_top5(

    db_session: db_session_type,
    skip: int = 0,
    limit: int = 100,
    genre: Optional[str] = Query(None),
):
    """
    Retorna uma top 5 de gêneros mais comuns no banco de dados.
    """
    criterias = {}
    if genre:
        criterias['genre'] = genre

    artists: list[Artist] = artist_controller.get_all(
        db_session, skip, limit, **criterias
    )

    genre_counter = Counter()
    for artist in artists:
        genres = artist.genre.split(', ')
        genre_counter.update(genres)

    top_genres = genre_counter.most_common(5)
    top_genres_list = [{'genre': genre, 'count': count} for genre, count in top_genres]

    return {'top_genres': top_genres_list}


@router.get('/{artist_id}', response_model=ArtistSchema)
def gey_artist_by_id(db_session: db_session_type, artist_id: str):
    """
    Retorna um artista específico do banco de dados pelo seu ID.
    """
    return artist_controller.get(db_session, artist_id)


@router.get(
    '/{spotify_type}/{spotify_search}',
    response_model=dict,
)
async def search_spotify_data_by_type(
    spotify_type: SpotifyType,
    spotify_search: str,
    current_user: CurrentUser,
):
    """
    Obtem informações do catálogo do Spotify sobre álbuns e artistas que correspondem a uma sequência de palavras-chave.
    """

    spotify_access_token = getattr(current_user, 'spotify_access_token', None)
    if not spotify_access_token:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Token do Spotify não encontrado.',
        )

    return await artist_controller.get_spotify_data(
        spotify_type, spotify_search, spotify_access_token
    )


@router.post('/artists', status_code=201, response_model=List[ArtistSchema])
async def add_new_artists(
    current_user: CurrentUser,
    db_session: db_session_type,
    request: Request,
    artist_ids: List[str] = Query(
        ..., description='Lista de IDs de artistas no Spotify'
    ),
) -> ArtistList:
    """
    Cria novos artistas no banco de dados a partir de uma lista de IDs de artistas do Spotify.
    """
    spotify_access_token = getattr(current_user, 'spotify_access_token', None)
    if not spotify_access_token:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Token do Spotify não encontrado.',
        )

    artists = await artist_controller.fetch_artists_info(
        spotify_access_token, artist_ids
    )

    created_artists = []
    for artist in artists:
        artist.audit_user_ip = request.client.host
        artist.audit_user_login = current_user.username

        try:
            saved_artist = artist_controller.save(db_session, artist)
            created_artists.append(saved_artist)
        except IntegrityValidationException as ex:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='objeto Artist não foi aceito',
            ) from ex

    return created_artists
