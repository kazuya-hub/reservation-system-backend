
from sqlmodel import Session, select

from ..models.users import User


def get_user_by_public_id(session: Session, public_user_id: str) -> User | None:
    statement = select(User).where(User.public_user_id == public_user_id)
    return session.exec(statement).first()
