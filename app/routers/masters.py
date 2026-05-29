
from fastapi import APIRouter
from sqlmodel import select

from ..dependencies.db import SessionDep
from ..models.masters import LessonSeries, Studio, Teacher
from ..schemas.masters import LessonSeriesRead, StudioRead, TeacherRead

router = APIRouter()

# TODO: 具体的な処理内容は本来Serviceに書くべき

@router.get("/lesson-series")
async def read_lesson_series(session: SessionDep) -> list[LessonSeriesRead]:
    statement = select(LessonSeries)
    lesson_series_list = session.exec(statement).all()
    return [LessonSeriesRead.model_validate(lesson_series) for lesson_series in lesson_series_list]

@router.get("/lesson-series/{lesson_series_id}")
async def read_lesson_series_by_id(lesson_series_id: int, session: SessionDep) -> LessonSeriesRead:
    lesson_series = session.get(LessonSeries, lesson_series_id)
    if not lesson_series:
        return None
    return LessonSeriesRead.model_validate(lesson_series)


@router.get("/studios")
async def read_studios(session: SessionDep) -> list[StudioRead]:
    statement = select(Studio)
    studios = session.exec(statement).all()
    return [StudioRead.model_validate(studio) for studio in studios]

@router.get("/studios/{studio_id}")
async def read_studio_by_id(studio_id: int, session: SessionDep) -> StudioRead:
    studio = session.get(Studio, studio_id)
    if not studio:
        return None
    return StudioRead.model_validate(studio)


@router.get("/teachers")
async def read_teachers(session: SessionDep) -> list[TeacherRead]:
    statement = select(Teacher)
    teachers = session.exec(statement).all()
    return [TeacherRead.model_validate(teacher) for teacher in teachers]

@router.get("/teachers/{teacher_id}")
async def read_teacher_by_id(teacher_id: int, session: SessionDep) -> TeacherRead:
    teacher = session.get(Teacher, teacher_id)
    if not teacher:
        return None
    return TeacherRead.model_validate(teacher)
