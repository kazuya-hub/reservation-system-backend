from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class LessonBase(SQLModel):
    start_at: datetime
    end_at: datetime
    lesson_series_id: int = Field(foreign_key="m_lesson_series.lesson_series_id")
    studio_id: int = Field(foreign_key="m_studios.studio_id")
    teacher_id: int = Field(foreign_key="m_teachers.teacher_id")


class Lesson(LessonBase, table=True):
    __tablename__ = "m_lessons"
    lesson_id: int | None = Field(default=None, primary_key=True)


class ReservationBase(SQLModel):
    lesson_id: int = Field(foreign_key="m_lessons.lesson_id")
    user_id: int = Field(foreign_key="m_users.user_id")


class Reservation(ReservationBase, table=True):
    __tablename__ = "t_reservations"
    reservation_id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))