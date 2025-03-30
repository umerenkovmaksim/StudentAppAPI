from pydantic import BaseModel, ConfigDict, EmailStr, Field


class SStudentConfirmation(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    student_id: int | None
    telegram_id: int | None
    email: EmailStr
    first_name: str | None
    last_name: str | None
    code: str
    attempts: int

class SStudentConfirmationCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    student_id: int | None = Field(None)
    telegram_id: int | None = Field(None)
    email: EmailStr = Field(...)
    first_name: str | None = Field(None)
    last_name: str | None = Field(None)

class SStudentConfirmationCheck(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    email: EmailStr = Field(...)
    code: str = Field(...)

class SGroupLeadershipCheck(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: int = Field(...)
    group_id: int = Field(...)
