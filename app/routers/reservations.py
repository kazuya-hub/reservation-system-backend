from fastapi import APIRouter
from sqlmodel import select

from ..dependencies.db import SessionDep
from ..dependencies.users import CurrentUserDep

from ..models.lessons import Reservation
from ..schemas.reservations import ReservationCreate, ReservationRead

router = APIRouter()


@router.post("/reservations")
async def create_reservation(
    reservation_create: ReservationCreate,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> ReservationRead:
    reservation_create.user_id = current_user.user_id
    reservation = Reservation.model_validate(reservation_create)
    session.add(reservation)
    session.commit()
    session.refresh(reservation)
    return ReservationRead.model_validate(reservation)


@router.get("/reservations/me")
async def read_my_reservations(session: SessionDep, current_user: CurrentUserDep) -> list[ReservationRead]:
    statement = select(Reservation).where(Reservation.user_id == current_user.user_id)
    reservations = session.exec(statement).all()
    return [ReservationRead.model_validate(reservation) for reservation in reservations]


@router.get("/reservations/{reservation_id}")
async def read_reservation(reservation_id: int, session: SessionDep) -> ReservationRead:
    reservation = session.get(Reservation, reservation_id)
    if not reservation:
        return None
    return ReservationRead.model_validate(reservation)
