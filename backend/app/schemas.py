from pydantic import BaseModel, Field
from typing import Any

class AnswerInput(BaseModel):
    question_id: int
    response: dict[str, Any] = Field(default_factory=dict)
    time_seconds: int = Field(default=0, ge=0, le=7200)

class DailyTestSubmit(BaseModel):
    answers: list[AnswerInput] = Field(min_length=7, max_length=7)
