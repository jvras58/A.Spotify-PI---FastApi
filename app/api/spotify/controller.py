from http import HTTPStatus
from typing import List

import httpx
from fastapi import HTTPException
from sqlalchemy import select

from app.api.spotify.schemas import SpotifyType
from app.database.session import Session
from app.models.artist import Artist
from app.utils.base_model import AbstractBaseModel
from app.utils.generic_controller import GenericController


class ArtistController(GenericController):
    def __init__(self) -> None:
        super().__init__(Artist)

    def get_artist_by_name(self, db_session: Session, name: str) -> Artist:
        return db_session.scalar(select(Artist).where(Artist.name == name))

    async def get_spotify_data(
        self, spotify_type: SpotifyType, spotify_search: str, spotify_access_token: str
    ) -> dict:
        url = f'https://api.spotify.com/v1/search?q={spotify_search}&type={spotify_type.value}&limit=40'
        headers = {'Authorization': f'Bearer {spotify_access_token}'}
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code, detail=response.json()
            )

        return response.json()

    async def fetch_artists_info(
        self, spotify_access_token: str, artist_ids: List[str]
    ) -> List[Artist]:
        ids_str = ','.join(artist_ids)
        url = f'https://api.spotify.com/v1/artists?ids={ids_str}'
        headers = {'Authorization': f'Bearer {spotify_access_token}'}

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)

        if response.status_code != 200:
            try:
                detail = response.json()
            except ValueError:
                detail = response.text
            raise HTTPException(status_code=response.status_code, detail=detail)

        data = response.json()
        artists_data = data.get('artists', [])

        invalid_ids = [
            artist_id
            for artist_id, artist_data in zip(artist_ids, artists_data)
            if artist_data is None
        ]
        if invalid_ids:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'Um ou mais IDs de artista não encontrados: {", ".join(invalid_ids)}',
            )

        artists = [
            Artist(
                name=artist_data.get('name'),
                followers=artist_data.get('followers', {}).get('total'),
                popularity=artist_data.get('popularity'),
                artist_id=artist_data.get('id'),
                genre=', '.join([genre for genre in artist_data.get('genres', [])]),
            )
            for artist_data in artists_data
            if artist_data is not None
        ]
        return artists

    def save(self, db_session: Session, obj: Artist) -> AbstractBaseModel:
        existe_artist = self.get_artist_by_name(db_session, obj.name)
        if existe_artist:
            if (
                existe_artist.followers != obj.followers
                or existe_artist.popularity != obj.popularity
            ):
                existe_artist.followers = obj.followers
                existe_artist.popularity = obj.popularity
                db_session.commit()
                return existe_artist
            else:
                return existe_artist
        return super().save(db_session, obj)
