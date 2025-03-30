from datetime import time
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base, int_null_true, int_pk, str_null_true, str_uniq

if TYPE_CHECKING:
    from app.students.models import Group


class Lesson(Base):
    id: Mapped[int_pk]
    name: Mapped[str]
    group_id: Mapped[int] = mapped_column(ForeignKey('groups.id'), nullable=False)
    teacher_id: Mapped[int] = mapped_column(ForeignKey('teachers.id'), nullable=True)
    building: Mapped[int_null_true]
    cabinet: Mapped[str_null_true]
    time_from: Mapped[time]
    time_to: Mapped[time]
    day_of_week: Mapped[int]
    split: Mapped[int]

    teacher: Mapped['Teacher'] = relationship('Teacher', back_populates='lessons', lazy='joined', cascade='all,delete') # type: ignore
    group: Mapped['Group'] = relationship('Group', back_populates='lessons', lazy='joined', cascade='all,delete') # type: ignore


class Teacher(Base):
    id: Mapped[int_pk]
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=True)
    first_name: Mapped[str_null_true]
    middle_name: Mapped[str_null_true]
    last_name: Mapped[str_null_true]
    short_name: Mapped[str_uniq] = mapped_column(unique=True, nullable=False)
    lessons: Mapped[list['Lesson']] = relationship('Lesson', back_populates='teacher') # type: ignore
