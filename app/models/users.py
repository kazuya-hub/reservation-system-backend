
from sqlmodel import SQLModel, Field

class UserBase(SQLModel):
    public_user_id: str = Field(index=True, unique=True)
    email: str = Field(index=True)

class User(UserBase, table=True):
    __tablename__ = "m_users"
    user_id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
