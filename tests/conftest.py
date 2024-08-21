import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from unittest.mock import patch
from app.api.spotify.controller import ArtistController
from app.database.session import get_session
from app.models.artist import Artist
from app.models.user import User
from app.startup import app
from app.utils.base_model import Base
from app.utils.security import get_password_hash
from tests.factory.user_factory import UserFactory


@pytest.fixture
def client(session):
    """
    Contexto de webclient para teste de APIRest

    Returns:
        TestClient: Uma instancia de TestClient do FastAPI.
    """

    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()

    return TestClient(app)


@pytest.fixture
def session():
    """
    Contexto de Session para teste de estrutura de banco de dados.

    Yields:
        Session: Uma instancia de Session do SQLAlchemy
    """
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
        # echo=True,
    )

    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    yield Session()
    Base.metadata.drop_all(engine)


@event.listens_for(Engine, 'connect')
def set_sqlite_pragma(dbapi_connection, connection_record):
    """
    Define o pragma de chaves estrangeiras para conexões de banco de dados SQLite.

    Args:
        dbapi_connection: O objeto de conexão com o banco de dados.
        connection_record: O objeto de registro de conexão.
    """
    cursor = dbapi_connection.cursor()
    cursor.execute('PRAGMA foreign_keys=ON')
    cursor.close()


@pytest.fixture
def user(session):
    """
    Cria uma ingessão de User para os testes.

    Args:
        session (Session): Uma instância de Session do SQLAlchemy.

    Returns:
        User: Uma instância de User do sistema.
    """
    clr_password = 'testtest'
    user = User(
        username='Teste',
        display_name='User Teste',
        email='teste@test.com',
        password=get_password_hash(clr_password),
        audit_user_ip='0.0.0.0',
        audit_user_login='tester',
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    user.clear_password = clr_password
    return user


@pytest.fixture
def other_user(session):
    """
    Cria uma ingessão de User para os testes.

    Args:
        session (Session): Uma instância de Session do SQLAlchemy.

    Returns:
        User: Uma instância de User do sistema.
    """
    clr_password = 'Qwert123'
    user = User(
        username='TesteOutro',
        email='teste_outro@test.com',
        display_name='User Teste Outro',
        password=get_password_hash(clr_password),
        audit_user_ip='0.0.0.0',
        audit_user_login='tester',
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    user.clear_password = clr_password
    return user


@pytest.fixture
def user_10(session):
    """
    Cria uma lista de 10 objetos Users para os testes.
    """
    UserFactory.reset_sequence()
    user: list[User] = UserFactory.build_batch(10)
    session.add_all(user)
    session.commit()

    return user


@pytest.fixture
def token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.username, 'password': user.clear_password},
    )
    return response.json()['access_token']

# TODO: refatorar para tbm ter um factory de artistas
@pytest.fixture
def Spotify(session):
    """
    Cria uma ingessão de Spotify para os testes.

    Args:
        session (Session): Uma instância de Session do SQLAlchemy.

    Returns:
        Spotify: Uma instância de Spotify do sistema.
    """

    artist = Artist(
        name='Teste',
        genre='Pop',
        popularity=10,
        followers=100,
        artist_id='1',
        audit_user_ip='0.0.0.0',
        audit_user_login='tester',
    )
    session.add(artist)
    session.commit()
    session.refresh(artist)

    return artist

@pytest.fixture
def mock_get_spotify_data():
    with patch.object(ArtistController, 'get_spotify_data') as mock:
        yield mock

@pytest.fixture
def mock_fetch_artists_info():
    with patch.object(ArtistController, 'fetch_artists_info') as mock:
        yield mock
