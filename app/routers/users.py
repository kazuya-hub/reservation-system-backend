
from fastapi import APIRouter

from ..dependencies.users import CurrentUserDep
from ..schemas.masters import UserRead

router = APIRouter()



@router.get("/users/me")
async def read_users_me(current_user: CurrentUserDep) -> UserRead:
    return UserRead.model_validate(current_user)
