

from fastapi import APIRouter, HTTPException, Depends
import requests
from app.api.spotify.schemas import Client_auth
from typing import  Annotated
from sqlalchemy.orm import Session

from app.database.session import get_session

router = APIRouter()

Session = Annotated[Session, Depends(get_session)]

# TODO: estou aqui:

@router.post("/token")
def get_spotify_api_token(client_auth: Client_auth):
    """
    Solicitar token de API do Spotify

    Usaremos este token de acesso ao portador para fazer login em outras APIs do Spotify

    documentação atual do Spotify:

    https://developer.spotify.com/documentation/general/guides/authorization-guide/#client-credentials-flow

    """
    url = "https://accounts.spotify.com/api/token"
    spotify_client_data = {
        "grant_type": "client_credentials",
        "client_id": client_auth.client_id, 
        "client_secret": client_auth.client_secret
    }
    # TODO: estou aqui: esse data não existe criar um dict falso para testar
    response = requests.post(url, data=spotify_client_data)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail = response.json() )

    return response.json()
