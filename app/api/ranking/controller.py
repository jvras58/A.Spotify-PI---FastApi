from collections import Counter
from typing import List
from api.spotify.controller import ArtistController
from models.artist import Artist
from database.session import Session
from models.ranking import Ranking
from utils.base_model import AbstractBaseModel
from utils.generic_controller import GenericController


artist_controller = ArtistController()


class RankingController(GenericController):
    def __init__(self) -> None:
        super().__init__(Ranking)

    def get_artists(self, db_session, skip, limit, order, **criterias):
        return artist_controller.get_all(db_session, skip, limit, order=order, **criterias)

    def save(self, db_session: Session, obj: Ranking) -> AbstractBaseModel:
        # TODO: Implementar a lógica de salvar sem permitir duplicidades no banco de dados
        return super().save(db_session, obj)

    def create_ranking(self, artists_data: List[Artist]):
        top_ranking = [
            {
                "artist_name": artist.name,
                "followers": artist.followers
            }
            for artist in artists_data
        ]

        genre_counter = Counter()
        for artist in artists_data:
            genres = artist.genre.split(', ')
            genre_counter.update(genres)

        top_genres = genre_counter.most_common(5)
        genre_ranking = [genre for genre, count in top_genres]

        return genre_ranking, top_ranking
