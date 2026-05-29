
from fastapi import APIRouter
from sqlalchemy import func
from sqlmodel import select

from ..dependencies.db import SessionDep
from ..dependencies.users import CurrentUserDep

from ..models.masters import Studio, Teacher, LessonSeries
from ..models.lessons import Lesson, Reservation
from ..schemas.lessons import LessonRead
from ..schemas.reservations import ReservationCreate, ReservationRead

router = APIRouter()



@router.get("/lessons")
async def read_lessons(session: SessionDep) -> list[LessonRead]:
    statement = select(Lesson)
    lessons = session.exec(statement).all()
    lesson_read_list = []
    for lesson in lessons:
        lesson_read = LessonRead.model_validate(lesson)
        studio_name = session.get(Studio, lesson.studio_id).name
        teacher_name = session.get(Teacher, lesson.teacher_id).name
        lesson_series_name = session.get(LessonSeries, lesson.lesson_series_id).name

        reservation_count_statement = select(func.count()).where(Reservation.lesson_id == lesson.lesson_id)
        current_reservations = session.exec(reservation_count_statement).one()

        lesson_read.studio_name = studio_name
        lesson_read.teacher_name = teacher_name
        lesson_read.lesson_series_name = lesson_series_name
        lesson_read.current_reservations = int(current_reservations)
        lesson_read_list.append(lesson_read)
    return lesson_read_list

@router.get("/lessons/me/reserved")
async def read_reserved_lessons(session: SessionDep, current_user: CurrentUserDep) -> list[LessonRead]:
    reservation_statement = select(Reservation).where(Reservation.user_id == current_user.user_id)
    reservations = session.exec(reservation_statement).all()
    lesson_read_list = []
    for reservation in reservations:
        lesson = session.get(Lesson, reservation.lesson_id)
        lesson_read = LessonRead.model_validate(lesson)
        studio_name = session.get(Studio, lesson.studio_id).name
        teacher_name = session.get(Teacher, lesson.teacher_id).name
        lesson_series_name = session.get(LessonSeries, lesson.lesson_series_id).name

        reservation_count_statement = select(func.count()).where(Reservation.lesson_id == lesson.lesson_id)
        current_reservations = session.exec(reservation_count_statement).one()

        lesson_read.studio_name = studio_name
        lesson_read.teacher_name = teacher_name
        lesson_read.lesson_series_name = lesson_series_name
        lesson_read.current_reservations = int(current_reservations)
        lesson_read_list.append(lesson_read)
    return lesson_read_list

@router.get("/lessons/{lesson_id}")
async def read_lesson(lesson_id: int, session: SessionDep) -> LessonRead:
    lesson = session.get(Lesson, lesson_id)
    if not lesson:
        return None
    
    studio_name = session.get(Studio, lesson.studio_id).name
    teacher_name = session.get(Teacher, lesson.teacher_id).name
    lesson_series_name = session.get(LessonSeries, lesson.lesson_series_id).name

    reservation_count_statement = select(func.count()).where(Reservation.lesson_id == lesson_id)
    current_reservations = session.exec(reservation_count_statement).one()

    lesson_read = LessonRead.model_validate(lesson)
    lesson_read.studio_name = studio_name
    lesson_read.lesson_series_name = lesson_series_name
    lesson_read.teacher_name = teacher_name
    lesson_read.current_reservations = int(current_reservations)
    return lesson_read

@router.get("/lessons/series/{lesson_series_id}")
async def read_lessons_by_series(lesson_series_id: int, session: SessionDep) -> list[LessonRead]:
    statement = select(Lesson).where(Lesson.lesson_series_id == lesson_series_id)
    lessons = session.exec(statement).all()
    return [LessonRead.model_validate(lesson) for lesson in lessons]


@router.post("/reservations")
async def create_reservation(
    reservation_create: ReservationCreate, 
    session: SessionDep, 
    current_user: CurrentUserDep
) -> ReservationRead:
    reservation_create.user_id = current_user.user_id
    reservation = Reservation.model_validate(reservation_create)
    session.add(reservation)
    session.commit()
    session.refresh(reservation)
    return ReservationRead.model_validate(reservation)

@router.get("/reservations")
async def read_reservations(session: SessionDep) -> list[ReservationRead]:
    statement = select(Reservation)
    reservations = session.exec(statement).all()
    return [ReservationRead.model_validate(reservation) for reservation in reservations]

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
