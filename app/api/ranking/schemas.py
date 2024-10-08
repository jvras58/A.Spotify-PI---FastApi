from typing import List, Optional

from pydantic import BaseModel


class ArtistRanking(BaseModel):
    """Representa um artista."""

    artist_name: str
    followers: int


class RankingResponse(BaseModel):
    """Representa o ranking."""

    id: int
    audit_user_ip: str = None
    audit_user_login: str = None
    genre_select: Optional[str] = None
    order_by: Optional[str] = None
    top_genre_ranking: List[ArtistRanking]
    genre_ranking: List[str]


class RankingList(BaseModel):
    """
    Representa uma lista de Rankings do sistema.
    """

    rankings: list[RankingResponse]


class GenreRanking(BaseModel):
    """
    Representa o ranking de gêneros.
    """

    id: int
    genre_select: Optional[str] = None
    order_by: Optional[str] = None
    genre_ranking: List[str]


class TopRanking(BaseModel):
    """
    Representa o top_ranking pelos gêneros.
    """

    id: int
    genre_select: Optional[str] = None
    order_by: Optional[str] = None
    top_ranking: Optional[List[ArtistRanking]]
