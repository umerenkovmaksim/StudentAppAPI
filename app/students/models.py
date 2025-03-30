from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base, int_pk, str_null_true, str_uniq


class Group(Base):
    id: Mapped[int_pk]
    short_name: Mapped[str_uniq]
    degree: Mapped[int]
    institute: Mapped[str]
    major: Mapped[str_null_true]
    major_profile: Mapped[str_null_true]
    chat_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=True)

    students: Mapped[list['Student']] = relationship('Student', back_populates='group')
    lessons: Mapped[list['Lesson']] = relationship('Lesson', back_populates='group') # type: ignore  # noqa: F821


class Student(Base):
    id: Mapped[int_pk]
    student_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=True)
    first_name: Mapped[str_null_true]
    last_name: Mapped[str_null_true]
    group_id: Mapped[int] = mapped_column(ForeignKey('groups.id'), nullable=True)

    group: Mapped['Group'] = relationship(back_populates='students', cascade="all,delete")
    feedbacks: Mapped[list['Feedback']] = relationship('Feedback', back_populates='user', cascade="all,delete") # type: ignore  # noqa: F821

class GroupLeadership(Base):
    id: Mapped[int_pk]
    group_id: Mapped[int] = mapped_column(ForeignKey('groups.id'), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('students.id'), nullable=False)

class StudentConfirmation(Base):
    id: Mapped[int_pk]
    student_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
    email: Mapped[str]
    first_name: Mapped[str_null_true]
    last_name: Mapped[str_null_true]

    exist_user: Mapped[int] = mapped_column(ForeignKey('students.id'), nullable=True)
    code: Mapped[str]
    attempts: Mapped[int] = mapped_column(default=3, nullable=True)


