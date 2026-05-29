from datetime import datetime, timezone

from sqlmodel import SQLModel, Session

from app.core.db import engine

# SQLModel.metadata.create_all の対象になるよう、使用しなくても全モデルをimportする
from app.models.masters import LessonSeries, Studio, Teacher
from app.models.lessons import Lesson, Reservation
from app.models.users import User
from app.models.email_verifications import EmailVerification


def reset_database() -> None:
    # Rebuild all tables so schema changes (added/removed columns) are reflected.
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)


def seed_all() -> None:
    reset_database()

    with Session(engine) as session:
        users = [
            User(
                public_user_id="johndoe",
                email="johndoe@example.com",
                hashed_password="$argon2id$v=19$m=65536,t=3,p=4$wagCPXjifgvUFBzq4hqe3w$CYaIb8sB+wtD+Vu/P4uod1+Qof8h+1g7bbDlBID48Rc",
            ),
            User(
                public_user_id="janedoe",
                email="janedoe@example.com",
                hashed_password="$argon2id$v=19$m=65536,t=3,p=4$wagCPXjifgvUFBzq4hqe3w$CYaIb8sB+wtD+Vu/P4uod1+Qof8h+1g7bbDlBID48Rc",
            ),
        ]
        session.add_all(users)
        session.commit()

        lesson_series_list = [
            LessonSeries(name="朝ヨガ"),
            LessonSeries(name="ピラティス初級"),
            LessonSeries(name="ボディメイク"),
        ]
        session.add_all(lesson_series_list)

        studios = [
            Studio(name="渋谷スタジオ"),
            Studio(name="新宿スタジオ"),
        ]
        session.add_all(studios)

        teachers = [
            Teacher(name="山田先生"),
            Teacher(name="佐藤先生"),
        ]
        session.add_all(teachers)
        session.commit()

        lessons = [
            Lesson(
                start_at=datetime(2026, 6, 1, 10, 0, 0),
                end_at=datetime(2026, 6, 1, 11, 0, 0),
                lesson_series_id=lesson_series_list[0].lesson_series_id,
                studio_id=studios[0].studio_id,
                teacher_id=teachers[0].teacher_id,
                max_reservations=10,
            ),
            Lesson(
                start_at=datetime(2026, 6, 1, 13, 0, 0),
                end_at=datetime(2026, 6, 1, 14, 0, 0),
                lesson_series_id=lesson_series_list[1].lesson_series_id,
                studio_id=studios[1].studio_id,
                teacher_id=teachers[1].teacher_id,
                max_reservations=15,
            ),
            Lesson(
                start_at=datetime(2026, 6, 2, 19, 0, 0),
                end_at=datetime(2026, 6, 2, 20, 0, 0),
                lesson_series_id=lesson_series_list[2].lesson_series_id,
                studio_id=studios[0].studio_id,
                teacher_id=teachers[1].teacher_id,
            ),
            Lesson(
                start_at=datetime(2026, 6, 3, 9, 30, 0),
                end_at=datetime(2026, 6, 3, 10, 30, 0),
                lesson_series_id=lesson_series_list[0].lesson_series_id,
                studio_id=studios[1].studio_id,
                teacher_id=teachers[0].teacher_id,
                max_reservations=12,
            ),
            Lesson(
                start_at=datetime(2026, 6, 4, 18, 0, 0),
                end_at=datetime(2026, 6, 4, 19, 0, 0),
                lesson_series_id=lesson_series_list[1].lesson_series_id,
                studio_id=studios[0].studio_id,
                teacher_id=teachers[1].teacher_id,
                max_reservations=10,
            ),
            Lesson(
                start_at=datetime(2026, 6, 5, 20, 0, 0),
                end_at=datetime(2026, 6, 5, 21, 0, 0),
                lesson_series_id=lesson_series_list[2].lesson_series_id,
                studio_id=studios[1].studio_id,
                teacher_id=teachers[0].teacher_id,
                max_reservations=16,
            ),
            Lesson(
                start_at=datetime(2026, 6, 8, 10, 0, 0),
                end_at=datetime(2026, 6, 8, 11, 0, 0),
                lesson_series_id=lesson_series_list[0].lesson_series_id,
                studio_id=studios[0].studio_id,
                teacher_id=teachers[0].teacher_id,
                max_reservations=10,
            ),
            Lesson(
                start_at=datetime(2026, 6, 9, 13, 0, 0),
                end_at=datetime(2026, 6, 9, 14, 0, 0),
                lesson_series_id=lesson_series_list[1].lesson_series_id,
                studio_id=studios[1].studio_id,
                teacher_id=teachers[1].teacher_id,
                max_reservations=15,
            ),
            Lesson(
                start_at=datetime(2026, 6, 10, 19, 0, 0),
                end_at=datetime(2026, 6, 10, 20, 0, 0),
                lesson_series_id=lesson_series_list[2].lesson_series_id,
                studio_id=studios[0].studio_id,
                teacher_id=teachers[1].teacher_id,
                max_reservations=14,
            ),
            Lesson(
                start_at=datetime(2026, 6, 12, 11, 0, 0),
                end_at=datetime(2026, 6, 12, 12, 0, 0),
                lesson_series_id=lesson_series_list[0].lesson_series_id,
                studio_id=studios[1].studio_id,
                teacher_id=teachers[0].teacher_id,
                max_reservations=12,
            ),
            Lesson(
                start_at=datetime(2026, 6, 15, 17, 30, 0),
                end_at=datetime(2026, 6, 15, 18, 30, 0),
                lesson_series_id=lesson_series_list[1].lesson_series_id,
                studio_id=studios[0].studio_id,
                teacher_id=teachers[1].teacher_id,
                max_reservations=10,
            ),
            Lesson(
                start_at=datetime(2026, 6, 16, 20, 0, 0),
                end_at=datetime(2026, 6, 16, 21, 0, 0),
                lesson_series_id=lesson_series_list[2].lesson_series_id,
                studio_id=studios[1].studio_id,
                teacher_id=teachers[0].teacher_id,
                max_reservations=18,
            ),
        ]
        session.add_all(lessons)
        session.commit()

        reservations = [
            Reservation(
                lesson_id=lessons[0].lesson_id,
                user_id=users[0].user_id,
                created_at=datetime(2026, 5, 27, 9, 0, 0, tzinfo=timezone.utc),
            ),
            Reservation(
                lesson_id=lessons[1].lesson_id,
                user_id=users[1].user_id,
                created_at=datetime(2026, 5, 27, 10, 30, 0, tzinfo=timezone.utc),
            ),
            Reservation(
                lesson_id=lessons[2].lesson_id,
                user_id=users[0].user_id,
                created_at=datetime(2026, 5, 27, 11, 0, 0, tzinfo=timezone.utc),
            ),
            Reservation(
                lesson_id=lessons[0].lesson_id,
                user_id=users[1].user_id,
                created_at=datetime(2026, 5, 27, 12, 0, 0, tzinfo=timezone.utc),
            ),
        ]
        session.add_all(reservations)
        session.commit()


if __name__ == "__main__":
    seed_all()
    print("Seeding completed.")
