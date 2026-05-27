from datetime import timedelta

from pwdlib import PasswordHash
from sqlmodel import Session

from ..core.auth import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from ..models.users import User
from .users import get_user_by_public_id

password_hash = PasswordHash.recommended()
DUMMY_HASH = password_hash.hash("dummypassword")


def authenticate_user(session: Session, public_user_id: str, password: str) -> User | None:
    user = get_user_by_public_id(session, public_user_id)

    # タイミング攻撃を防ぐために、ユーザーが取得できなかった場合でもハッシュ検証の処理を行う
    if not user:
        password_hash.verify(password, DUMMY_HASH)
        return None

    if not password_hash.verify(password, user.hashed_password):
        return None

    return user


def issue_access_token(session: Session, public_user_id: str, password: str) -> str | None:
    user = authenticate_user(session, public_user_id, password)
    if not user:
        return None

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return create_access_token(
        data={"sub": user.public_user_id},
        expires_delta=access_token_expires,
    )
