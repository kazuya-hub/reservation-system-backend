from datetime import datetime, timedelta, timezone
import hashlib
import hmac
import secrets
from sqlmodel import select

from pwdlib import PasswordHash
from sqlmodel import Session

from ..core.auth import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, create_access_token
from ..models.users import User
from ..models.email_verifications import EmailVerification
from .users import get_user_by_public_id

password_hash = PasswordHash.recommended()
DUMMY_HASH = password_hash.hash("dummypassword")
VERIFY_TOKEN_HMAC_KEY = b"email-verification:" + SECRET_KEY.encode("utf-8")


def ensure_utc(dt: datetime) -> datetime:
    """Normalize DB-loaded datetime to UTC-aware datetime."""
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def hash_email_verification_token(token: str) -> str:
    """tokenのHMAC-SHA256ハッシュを作成する"""
    return hmac.new(VERIFY_TOKEN_HMAC_KEY, token.encode("utf-8"), hashlib.sha256).hexdigest()


def compare_email_verification_token(token: str, token_hash: str) -> bool:
    """tokenとtoken_hashが一致するかを比較する"""
    computed = hash_email_verification_token(token)
    return hmac.compare_digest(computed, token_hash)


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

def request_registration(session: Session, email: str):
    token = secrets.token_urlsafe(32)
    hashed_token = hash_email_verification_token(token)

    email_verification = EmailVerification(
        email=email,
        hashed_token=hashed_token,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=30),
    )

    statement = select(EmailVerification).where(EmailVerification.email == email)
    existing = session.exec(statement).first()
    if existing:
        # すでに登録リクエストが存在する場合は更新する
        existing.hashed_token = hashed_token
        existing.expires_at = email_verification.expires_at
        existing.consumed_at = None
    else:
        session.add(email_verification)

    session.commit()
    return token


def complete_registration(session: Session, token: str, public_user_id: str, password: str):
    statement = select(EmailVerification
                       ).where(EmailVerification.hashed_token == hash_email_verification_token(token))
    verification = session.exec(statement).first()

    if not verification:
        raise ValueError("invalid token")

    expires_at_utc = ensure_utc(verification.expires_at)
    now_utc = datetime.now(timezone.utc)

    if expires_at_utc < now_utc:
        raise ValueError("token expired")

    if verification.consumed_at is not None:
        raise ValueError("token already consumed")

    if get_user_by_public_id(session, public_user_id):
        raise ValueError("public_user_id already exists")

    user = User(
        public_user_id=public_user_id,
        email=verification.email,
        hashed_password=password_hash.hash(password),
    )
    session.add(user)

    verification.consumed_at = datetime.now(timezone.utc)
    session.add(verification)

    session.commit()
    