from fastapi import Request
from typing import Annotated, Optional

from api.authentication.controller import get_current_user

from api.spotify.schemas import OrderType
from api.ranking.controller import RankingController
from models.ranking import Ranking
from database.session import get_session
from fastapi import APIRouter, Depends, Query
from models.user import User
from sqlalchemy.orm import Session

router = APIRouter()
ranking_controller = RankingController()


db_session_type = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]

@router.get('/get_all_rankings')
def read_artists_rankings(
    db_session: db_session_type,
    skip: int = 0,
    limit: int = 100,
    genre: Optional[str] = Query(None),
    order_by: Optional[OrderType] = Query(None),
):
    """
    Obtém uma lista dos rankings `top_genre` e `ranking_artist_genre` do banco de dados.
    """
    criterias = {}
    if genre:
        criterias['genre'] = genre

    rankings = ranking_controller.get_all(db_session, skip, limit, order_by, **criterias)
    return {'rankings': rankings}

@router.get('/get_genre_ranking')
def get_genre_ranking(
    db_session: db_session_type,
    skip: int = 0,
    limit: int = 100,
    genre: Optional[str] = Query(None),
    order_by: Optional[OrderType] = Query(None),
):
    """
    Obtém o ranking de gêneros do banco de dados.
    """
    criterias = {}
    if genre:
        criterias['genre'] = genre

    rankings = ranking_controller.get_all(db_session, skip, limit, order_by, **criterias)
    if rankings:
        genre_ranking = rankings[0].genre_ranking
        return {'genre_ranking': genre_ranking}
    return {'genre_ranking': []}

@router.get('/get_top_ranking')
def get_top_ranking(
    db_session: db_session_type,
    skip: int = 0,
    limit: int = 100,
    genre: Optional[str] = Query(None),
    order_by: Optional[OrderType] = Query(None),
):
    """
    Obtém o top ranking de gêneros do banco de dados.
    """
    criterias = {}
    if genre:
        criterias['genre'] = genre

    rankings = ranking_controller.get_all(db_session, skip, limit, order_by, **criterias)
    if rankings:
        top_ranking = rankings[0].top_genre_ranking
        return {'top_ranking': top_ranking}
    return {'top_ranking': []}


@router.post('/save_ranking', status_code=201)
def save_full_ranking(
    db_session: db_session_type,
    request: Request,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
    genre: Optional[str] = Query(None),
    order_by: Optional[OrderType] = Query(None),
):
    """
    Obtém uma lista de artistas e o top 5 de gêneros mais comuns do banco de dados, 
    e salva como JSON nos campos `genre_ranking` e `top_genre_ranking` na tabela `Rankings`.
    """
    criterias = {}
    if genre:
        criterias['genre'] = genre

    order = None
    if order_by == OrderType.followers:
        order = 'followers DESC'

    artists_data = ranking_controller.get_artists(db_session, skip, limit, order, **criterias)
    genre_ranking, top_ranking = ranking_controller.create_ranking(artists_data)

    ranking = Ranking(
        genre_ranking=genre_ranking,
        top_genre_ranking=top_ranking
    )
    ranking.audit_user_ip = request.client.host
    ranking.audit_user_login = current_user.username
    Rank = ranking_controller.save(db_session, ranking)

    return {'Ranking': Rank}
