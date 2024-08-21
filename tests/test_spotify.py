

from unittest.mock import ANY
from app.api.spotify.schemas import SpotifyType


def test_read_artists(client, Spotify):
    response = client.get("/spotify/")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_search_spotify_data_by_type(client,mock_get_spotify_data, token):
    mock_get_spotify_data.return_value = {"some_key": "some_value"}
    response = client.get("/spotify/artist/artist_search", headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert response.json() == {"some_key": "some_value"}

    # Verificando se a função get_spotify_data foi chamada corretamente
    mock_get_spotify_data.assert_called_once_with(
        spotify_type=SpotifyType.artist,
        spotify_search="artist_search",
        spotify_access_token=ANY,
    )

# def test_add_new_artists(client, mock_fetch_artists_info):
#     # Mockando o retorno da função fetch_artists_info
#     mock_fetch_artists_info.return_value = [
#         {"id": "1", "name": "Artist 1"},
#         {"id": "2", "name": "Artist 2"}
#     ]

#     response = client.post(
#         "spotify/artists/",
#         params={"artist_ids": ["1", "2"]},
#         headers={"Authorization": "Bearer mocked_token"}  # Token mockado
#     )

#     assert response.status_code == 201
#     assert len(response.json()) == 2

#     mock_fetch_artists_info.assert_called_once_with(
#         "mocked_token", ["1", "2"]
#     )
