from pydantic import BaseModel, ConfigDict, EmailStr, Field


def convert_to_optional(schema):
    return {k: v | None for k, v in schema.__annotations__.items()}

class SStudent(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    student_id: int | None = Field(None)
    telegram_id: int | None = Field(None)
    email: EmailStr | None = Field(None)
    first_name: str | None = Field(None, max_length=100)
    last_name: str | None = Field(None, max_length=100)
    group_id: int | None  = Field(None)


class SStudentAdd(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    student_id: int | None = Field(None)
    telegram_id: int | None = Field(None)
    email: EmailStr | None = Field(None)
    first_name: str | None = Field(None, max_length=100)
    last_name: str | None = Field(None, max_length=100)
    group_id: int | None  = Field(None)


class SStudentUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    student_id: int | None = Field(None)
    telegram_id: int | None = Field(None)
    email: EmailStr | None = Field(None)
    first_name: str | None = Field(None, max_length=100)
    last_name: str | None = Field(None, max_length=100)
    group_id: int | None = Field(None)


class SStudentFilter(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int


class SGroup(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    short_name: str = Field(..., min_length=1, max_length=100)
    chat_id: int | None = Field(None)
    degree: int = Field(...)
    major: str | None = Field(None, max_length=200)
    major_profile: str | None = Field(None, max_length=200)
    institute: str = Field(..., max_length=200)

class SGroupAdd(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    short_name: str = Field(..., min_length=1, max_length=100)
    chat_id: int | None = Field(None)
    degree: int = Field(...)
    major: str | None = Field(None, max_length=200)
    major_profile: str | None = Field(None, max_length=200)
    institute: str = Field(..., max_length=200)

class SGroupUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    short_name: str | None = Field(None, min_length=1, max_length=100)
    chat_id: int | None = Field(None)
    degree: int | None = Field(None)
    major: str | None = Field(None, max_length=200)
    major_profile: str | None = Field(None, max_length=200)
    institute: str | None = Field(..., max_length=200)
