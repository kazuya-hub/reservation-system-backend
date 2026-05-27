from datetime import datetime

from sqlmodel import SQLModel


class ReservationCreate(SQLModel):
    lesson_id: int
    user_id: int
    created_at: datetime | None = None


class ReservationRead(SQLModel):
    reservation_id: int
    lesson_id: int
    user_id: int
    created_at: datetime


class ReservationUpdate(SQLModel):
    lesson_id: int | None = None
    user_id: int | None = None
