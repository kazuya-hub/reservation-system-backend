# 参考: https://fastapi.tiangolo.com/ja/tutorial/security/

from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from pydantic import BaseModel
from sqlmodel import SQLModel, Session, Field, create_engine, select


SECRET_KEY = "52cb5216e33ff2bb2f18fec35816f7b9e2842632523884032a5ee024dfacaa41"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



class UserBase(SQLModel):
    public_user_id: str = Field(index=True, unique=True)
    email: str = Field(index=True)

class User(UserBase, table=True):
    __tablename__ = "m_users"
    user_id: int | None = Field(default=None, primary_key=True)
    hashed_password: str

class UserCreate(UserBase):
    hashed_password: str

class UserRead(UserBase):
    user_id: int

class UserUpdate(SQLModel):
    public_user_id: str | None = None
    email: str | None = None

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = { "check_same_thread": False }
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    public_user_id: str | None = None



password_hash = PasswordHash.recommended()

DUMMY_HASH = password_hash.hash("dummypassword")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

origins = [
    "http://localhost:5173", # vueのデフォルト
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.middleware("http")
# async def printout(request: Request, call_next):
#     print(dict(request))
#     return await call_next(request)



@app.on_event("startup")
def on_startup():
    create_db_and_tables()



def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_hash.hash(password)


def get_user_by_public_id(session: Session, public_user_id: str) -> User | None:
    statement = select(User).where(User.public_user_id == public_user_id)
    return session.exec(statement).first()


def authenticate_user(session: Session, public_user_id: str, password: str) -> User | bool:
    user = get_user_by_public_id(session, public_user_id)

    if not user: # 存在しないユーザーに対してもダミーのverify処理を行う。タイミング攻撃を防止するため。
        verify_password(password, DUMMY_HASH)
        return False

    if not verify_password(password, user.hashed_password):
        return False

    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


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
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        public_user_id = payload.get("sub")
        if public_user_id is None:
            raise credentials_exception
        token_data = TokenData(public_user_id=public_user_id)
    except InvalidTokenError:
        raise credentials_exception

    user = get_user_by_public_id(session, token_data.public_user_id)
    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    return current_user


@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep,
) -> Token:
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.public_user_id}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")


@app.get("/users/me/")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> UserRead:
    return UserRead.model_validate(current_user)
