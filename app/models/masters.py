from sqlmodel import Field, SQLModel


class LessonSeriesBase(SQLModel):
    name: str


class LessonSeries(LessonSeriesBase, table=True):
    __tablename__ = "m_lesson_series"
    lesson_series_id: int | None = Field(default=None, primary_key=True)


class StudioBase(SQLModel):
    name: str


class Studio(StudioBase, table=True):
    __tablename__ = "m_studios"
    studio_id: int | None = Field(default=None, primary_key=True)


class TeacherBase(SQLModel):
    name: str


class Teacher(TeacherBase, table=True):
    __tablename__ = "m_teachers"
    teacher_id: int | None = Field(default=None, primary_key=True)
