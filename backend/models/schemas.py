from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal
from datetime import datetime

# 🔐 USER LOGIN
class LoginRequest(BaseModel):
    name: str = Field(..., min_length=3)
    password: str = Field(..., min_length=6)


# 🔔 REMINDER
class ReminderCreate(BaseModel):
    user_id: int
    message: str = Field(..., min_length=3, max_length=200)
    remind_at: datetime
    recurrence: Optional[str] = Field(default="none")


class ReminderUpdate(BaseModel):
    user_id: int
    reminder_id: int
    remind_at: datetime


# 👤 USER
class UserCreate(BaseModel):
    name: str = Field(..., min_length=3)
    password: str = Field(..., min_length=6)
    role: Literal["OWNER", "USER"] = "USER"
    disability_type: str | None = None
    language_pref: str | None = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError("Name cannot be empty")
        return v


# 👤 PROFILE (FIXED - no wrong validator)
class ProfileCreate(BaseModel):
    user_id: int
    name: str
    preferences: Optional[dict] = None
    health_info: Optional[dict] = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError("Name cannot be empty")
        return v

# 🧠 CONVERSATION
class ConversationCreate(BaseModel):
    user_id: int
    text: str = Field(..., min_length=1)
    intent: str
    response: str
    sentiment: Optional[str]

from pydantic import BaseModel

class ChatRequest(BaseModel):

    user_id: int
    text: str = Field(..., min_length=1)