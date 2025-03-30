from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SFeedback(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    title: str
    text: str
    created_at: datetime


class SFeedbackCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: int
    title: str
    text: str
