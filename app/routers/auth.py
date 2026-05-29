from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from ..core.auth import send_email_verification
from ..dependencies.db import SessionDep
from ..schemas.auth import Token
from ..services.auth import issue_access_token, request_registration, complete_registration, is_public_user_id_available

router = APIRouter()


class RegisterRequest(BaseModel):
    email: str

class RegisterCompleteRequest(BaseModel):
    token: str
    public_user_id: str
    password: str


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep,
) -> Token:
    access_token = issue_access_token(session, form_data.username, form_data.password)
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return Token(access_token=access_token, token_type="bearer")

@router.post("/register-request")
async def register_request(
    form_data: RegisterRequest,
    session: SessionDep,
):
    token = request_registration(session, form_data.email)
    try:
        verification_url = send_email_verification(form_data.email, token)
    except RuntimeError:
        return {"token": token}

@router.post("/register-complete-request")
async def register_complete_request(
    form_data: RegisterCompleteRequest,
    session: SessionDep,
):
    token = form_data.token
    public_user_id = form_data.public_user_id
    password = form_data.password

    try:
        complete_registration(session, token, public_user_id, password)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    return {"message": "registration complete"}


class PublicUserIdAvailabilityRequest(BaseModel):
    public_user_id: str

class PublicUserIdAvailabilityResponse(BaseModel):
    available: bool

@router.post("/public-user-id/availability")
async def check_public_user_id_availability(
    form_data: PublicUserIdAvailabilityRequest,
    session: SessionDep,
):
    public_user_id = form_data.public_user_id
    is_available = is_public_user_id_available(session, public_user_id)
    return PublicUserIdAvailabilityResponse(available=is_available)
