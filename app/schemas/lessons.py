
from datetime import datetime
from sqlmodel import SQLModel



class LessonRead(SQLModel):
    lesson_id: int
    start_at: datetime
    end_at: datetime
    studio_name: str | None = None
    lesson_series_name: str | None = None
    teacher_name: str | None = None
    max_reservations: int | None = None
    current_reservations: int | None = None
