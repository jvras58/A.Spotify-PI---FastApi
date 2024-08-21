from typing import Annotated

from api.authentication.controller import get_current_user
from api.user.controller import UserController
from api.user.schemas import UserList, UserPublic, UserSchema
from database.session import get_session
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi import status as HTTP_STATUS
from models.user import User
from sqlalchemy.orm import Session
from utils.base_schemas import SimpleMessageSchema
from utils.exceptions import IntegrityValidationException, ObjectNotFoundException

router = APIRouter()
user_controller = UserController()

Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', status_code=201, response_model=UserPublic)
async def create_new_user(user: UserSchema, request: Request, session: Session):

    new_user: User = User(**user.model_dump())
    new_user.audit_user_ip = request.client.host
    new_user.audit_user_login = user.username

    try:
        return user_controller.save(session, new_user)
    except IntegrityValidationException as ex:
        raise HTTPException(
            status_code=HTTP_STATUS.HTTP_400_BAD_REQUEST,
            detail='Object USER was not accepted',
        ) from ex


@router.get(
    '/{user_id}',
    status_code=HTTP_STATUS.HTTP_200_OK,
    response_model=UserPublic,
)
def get_user_by_id(user_id: int, db_session: Session):
    return user_controller.get(db_session, user_id)


@router.get('/', response_model=UserList)
def read_users(db_session: Session, skip: int = 0, limit: int = 100):
    users: list[User] = user_controller.get_all(db_session, skip, limit)
    return {'users': users}


@router.put('/{user_id}', response_model=UserPublic)
def update_existing_user(
    user_id: int,
    user: UserSchema,
    request: Request,
    db_session: Session,
    current_user: CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTP_STATUS.FORBIDDEN, detail='Not enough permissions'
        )

    try:
        new_user: User = User(**user.model_dump())
        new_user.id = user_id
        new_user.audit_user_ip = request.client.host
        new_user.audit_user_login = current_user.username

        return user_controller.update(db_session, new_user)
    except ObjectNotFoundException as ex:
        raise HTTPException(status_code=404, detail=ex.args[0]) from ex


@router.delete('/{user_id}', response_model=SimpleMessageSchema)
def delete_existing_user(
    user_id: int,
    db_session: Session,
    current_user: CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTP_STATUS.FORBIDDEN, detail='Not enough permissions'
        )
    try:
        user_controller.delete(db_session, user_id)
    except ObjectNotFoundException as ex:
        raise HTTPException(status_code=404, detail=ex.args[0]) from ex

    return {'detail': 'User deleted'}
