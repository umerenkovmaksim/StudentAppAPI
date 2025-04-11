from __future__ import annotations

from datetime import time

from pydantic import BaseModel, ConfigDict, Field

from app.students.schemas import SGroupAdd


class SLesson(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str = Field(..., max_length=300)
    teacher_id: int | None = Field(None)
    group_id: int = Field(...)
    building: int | None = Field(None)
    cabinet: str | None = Field(None)
    time_from: time = Field(...)
    time_to: time = Field(...)
    day_of_week: int = Field(...)
    split: int = Field(...)

class SLessonAdd(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str = Field(..., max_length=300)
    teacher: STeacherAdd | None = Field(None)
    group: SGroupAdd = Field(...)
    building: int | None = Field(None)
    cabinet: str | None = Field(None)
    time_from: time = Field(...)
    time_to: time = Field(...)
    day_of_week: int = Field(...)
    split: int = Field(...)

class SLessonUpdDesc(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str | None = Field(None, max_length=300)
    teacher: str | None = Field(None)
    group: SGroupAdd | None = Field(None)
    building: int | None = Field(None)
    cabinet: str | None = Field(None)
    time_from: time | None = Field(None)
    time_to: time | None = Field(None)
    day_of_week: int | None = Field(None)
    split: int | None = Field(None)


class STeacher(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    telegram_id: int | None = Field(None)
    first_name: str | None = Field(None)
    middle_name: str | None = Field(None)
    last_name: str | None = Field(None)
    short_name: str = Field(..., max_length=100)


class STeacherAdd(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    telegram_id: int | None = Field(None)
    first_name: str | None = Field(None)
    middle_name: str | None = Field(None)
    last_name: str | None = Field(None)
    short_name: str = Field(..., max_length=100)
