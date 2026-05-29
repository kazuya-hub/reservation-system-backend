from datetime import datetime

from sqlmodel import SQLModel

from ..models.users import UserBase


class UserCreate(UserBase):
    hashed_password: str


class UserRead(UserBase):
    user_id: int


class UserUpdate(SQLModel):
    public_user_id: str | None = None
    email: str | None = None


class LessonSeriesCreate(SQLModel):
    name: str


class LessonSeriesRead(SQLModel):
    lesson_series_id: int
    name: str


class LessonSeriesUpdate(SQLModel):
    name: str | None = None


class StudioCreate(SQLModel):
    name: str


class StudioRead(SQLModel):
    studio_id: int
    name: str


class StudioUpdate(SQLModel):
    name: str | None = None


class TeacherCreate(SQLModel):
    name: str


class TeacherRead(SQLModel):
    teacher_id: int
    name: str


class TeacherUpdate(SQLModel):
    name: str | None = None
