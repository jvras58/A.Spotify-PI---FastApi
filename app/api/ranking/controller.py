from collections import Counter
from typing import List

from app.api.spotify.controller import ArtistController
from app.database.session import Session
from app.models.artist import Artist
from app.models.ranking import Ranking
from app.utils.base_model import AbstractBaseModel
from app.utils.generic_controller import GenericController

artist_controller = ArtistController()


class RankingController(GenericController):
    def __init__(self) -> None:
        super().__init__(Ranking)

    def get_artists(self, db_session, skip, limit, order, **criterias):
        return artist_controller.get_all(
            db_session, skip, limit, order=order, **criterias
        )

    def save(self, db_session: Session, obj: Ranking) -> AbstractBaseModel:
        # TODO: Implementar a lógica de salvar sem permitir duplicidades no banco de dados
        return super().save(db_session, obj)

    def create_ranking(self, artists_data: List[Artist]):
        top_ranking = [
            {'artist_name': artist.name, 'followers': artist.followers}
            for artist in artists_data
        ]

        genre_counter = Counter()
        for artist in artists_data:
            genres = artist.genre.split(', ')
            genre_counter.update(genres)

        top_genres = genre_counter.most_common(5)
        genre_ranking = [genre for genre, count in top_genres]

        return genre_ranking, top_ranking
