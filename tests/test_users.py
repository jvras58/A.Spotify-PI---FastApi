from sqlalchemy import select

from app.api.user.schemas import UserPublic
from app.models.user import User
from tests.factory.user_factory import UserFactory


def test_create_user(session):
    """
    Teste de criação de User no banco de dados.

    Args:
        session (Session): Instancia de Session do SQLAlchemy provisionada pelo Fixture.
    """

    # GIVEN ------
    # Dada uma Instancia de User com os dados abaixo é salva no banco de dados;
    new_user = UserFactory.build()
    new_user.id = None
    new_user.username = 'user.test'
    session.add(new_user)
    session.commit()

    # WHEN ------
    # Quando executa-se uma busca com um fultro que aponta para o usuário anteriormente
    # salvo;
    user = session.scalar(select(User).where(User.username == 'user.test'))

    # THEN ------
    # Então uma instancia de User é retornada do banco de dados com os mesmos dados que
    # foi salvo anteriormente.
    assert user.username == 'user.test'
    assert user.display_name == new_user.display_name
    assert user.email == new_user.email
    assert user.password == new_user.password
    assert user.audit_user_ip == new_user.audit_user_ip
    assert user.audit_user_login == new_user.audit_user_login
    assert user.audit_created_at
    assert user.audit_updated_on


def test_create_user_success(client):
    response = client.post(
        '/users/',
        json={
            'username': 'teste',
            'display_name': 'teste Ribeiro',
            'email': 'teste@cin.br',
            'password': 'Qwert123',
        },
    )

    assert response.status_code == 201
    assert response.json()['id']
    assert response.json()['username'] == 'teste'
    assert response.json()['display_name'] == 'teste Ribeiro'
    assert response.json()['email'] == 'teste@cin.br'
    assert 'password' not in response.json()


def test_create_user_already_exists_fail(client, user):

    response = client.post(
        '/users/',
        json={
            'username': 'Teste',
            'display_name': 'User Teste',
            'email': 'teste@test.com',
            'password': 'Qwert123',
        },
    )

    assert response.status_code == 400
    assert response.json() == {'detail': 'Object USER was not accepted'}


def test_read_users(client, token):

    response = client.get('/users/', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert 'users' in response.json()
    assert len(response.json()['users']) == 1


def test_get_user_by_id(client, user, token):

    response = client.get(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == 200
    assert response.json()['id'] == user.id
    assert response.json()['username'] == user.username
    assert response.json()['display_name'] == user.display_name
    assert response.json()['email'] == user.email
    assert 'password' not in response.json()


def test_read_users_with_users(client, user, token):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/', headers={'Authorization': f'Bearer {token}'})
    assert response.json() == {'users': [user_schema]}


def test_update_user_success(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'OutroUsuário',
            'display_name': 'Outro Usuário',
            'email': 'alterado@ufpe.br',
            'password': 'SenhaMudada',
        },
    )

    assert response.status_code == 200
    assert response.json()['id'] == user.id
    assert response.json()['username'] == 'OutroUsuário'
    assert response.json()['display_name'] == 'Outro Usuário'
    assert response.json()['email'] == 'alterado@ufpe.br'
    assert 'password' not in response.json()


def test_update_user_fail(client, user):
    response = client.put(
        '/users/2',
        json={
            'username': 'OutroUsuário',
            'email': 'alterado@ufpe.br',
            'password': 'SenhaMudada',
        },
    )

    assert response.status_code == 401
    assert response.json() == {'detail': 'Not authenticated'}


def test_delete_user_success(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == 200
    assert response.json() == {'detail': 'User deleted'}


def test_delete_user_fail(client, user):
    response = client.delete('/users/2')

    assert response.status_code == 401
    assert response.json() == {'detail': 'Not authenticated'}
