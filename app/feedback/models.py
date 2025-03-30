from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base, int_pk


class Feedback(Base):
    id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(ForeignKey('students.id'), nullable=False)
    title: Mapped[str]
    text: Mapped[str]

    user = relationship('Student', back_populates='feedbacks')
