
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from typing import Annotated

from ..core.auth import decode_access_token_subject
from ..services.users import get_user_by_public_id
from ..models.users import User
from .db import SessionDep

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: SessionDep,
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        public_user_id = decode_access_token_subject(token)
    except ValueError:
        raise credentials_exception

    user = get_user_by_public_id(session, public_user_id)
    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    return current_user



CurrentUserDep = Annotated[User, Depends(get_current_active_user)]
