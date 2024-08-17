from datetime import datetime, timedelta

from bcrypt import checkpw, gensalt, hashpw
from fastapi import HTTPException
from jose import jwt
import requests
import logging
from app.utils.settings import get_settings




# Obtém o logger
logger = logging.getLogger(__name__)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    current_time = datetime.utcnow()
    expire = current_time + timedelta(minutes=get_settings().SECURITY_ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({'exp': expire})
    to_encode.update({'nbf': current_time})
    to_encode.update({'iat': current_time})
    to_encode.update({'iss': 'Spotify-Backend'})

    # Tenta obter o token do Spotify
    try:
        spotify_token = get_spotify_api_token()
        to_encode.update({'spotify_access_token': spotify_token.get('access_token')})
    except Exception as e:
        logger.error(f"Acesso à API do Spotify não concedido: {str(e)}")
    encoded_jwt = jwt.encode(
        to_encode,
        get_settings().SECURITY_API_SECRET_KEY,
        algorithm=get_settings().SECURITY_ALGORITHM,
    )

    return encoded_jwt

def get_spotify_api_token():
    """
    Solicita token de API do Spotify
    """
    url = "https://accounts.spotify.com/api/token"
    spotify_client_data = {
        "grant_type": "client_credentials",
        "client_id": get_settings().CLIENT_ID, 
        "client_secret": get_settings().CLIENT_SECRET
    }
    response = requests.post(url, data=spotify_client_data)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()


def get_password_hash(password: str) -> bytes:
    salt = gensalt()
    return hashpw(password.encode('utf-8'), salt)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    plain_password_encoded = plain_password.encode('utf-8')

    # Esta converção é necessária para que o bcrypt consiga comparar
    # as senhas quando a string vem do BD.
    if isinstance(hashed_password, str):
        hashed_password = bytes(hashed_password, 'utf-8')

    return checkpw(plain_password_encoded, hashed_password)


def extract_username(jwt_token: str) -> str:
    """
    Extrai o username (sub) do payload do JWT.
    """
    payload = jwt.decode(
        jwt_token,
        get_settings().SECURITY_API_SECRET_KEY,
        algorithms=[get_settings().SECURITY_ALGORITHM],
    )
    return payload.get('sub')

def extract_spotify_token(jwt_token: str) -> str | None:
    """
    Extrai o token de acesso do Spotify do payload do JWT.
    """
    payload = jwt.decode(
        jwt_token,
        get_settings().SECURITY_API_SECRET_KEY,
        algorithms=[get_settings().SECURITY_ALGORITHM],
    )
    return payload.get('spotify_access_token')
